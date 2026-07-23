#!/usr/bin/env python3
#
# Copyright 2026 AUTOMATOUS.IO
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Build Shelly Web UI OTA zip(s) from an ESPHome (esp-idf) build.

Standalone zip for a single model:

    python3 scripts/make-esphome-ota-zip.py --hardware shelly-1-gen4 --version 1.0.0 \\
        --build-dir configs/.esphome/build/shelly-1-gen4/.pioenvs/shelly-1-gen4

The build must be compiled for the Shelly layout the zip installs into; partition table at
--pt-addr (0x10000 for stock) and app_0 at 0x20000, i.e. the ESPHome config carries
partitions: (the stock csv) and CONFIG_PARTITION_TABLE_OFFSET=0x10000. A default 0x8000
build will likely install but not boot under the stock installer.
"""
import argparse, datetime, hashlib, json, os, sys, tempfile, zipfile

HARDWARE = {
    "shelly-1-gen4":      {"app_code": "S1G4",    "compatible": "S1G4*"},
    "shelly-1pm-gen4":    {"app_code": "S1PMG4",  "compatible": "S1PMG4*"},
    "shelly-1-mini-gen4": {"app_code": "Mini1G4", "compatible": "Mini1G4*"},
}
PLATFORM     = "esp32c6"
MANIFEST_VER = "99.0.0"
BOOT_MIN     = "99.0.0"
NVS_SIZE     = 0xC000
FS_SIZE      = 0xE0000
ENCRYPT      = False

# esp-idf and PlatformIO name these differently; accept either.
CANDIDATES = {
    "bootloader":      ["bootloader.bin", "bootloader/bootloader.bin"],
    "partition-table": ["partitions.bin", "partition-table.bin",
                        "partition_table/partition-table.bin"],
    "otadata":         ["ota_data_initial.bin"],
    "app":             ["firmware.bin", "firmware.ota.bin"],
}


def find(build_dir, names):
    for name in names:
        path = os.path.join(build_dir, name)
        if os.path.isfile(path):
            return path
    return None


def digest(path):
    data = open(path, "rb").read()
    return len(data), hashlib.sha256(data).hexdigest()


def write_zip(out_dir, tmp, hardware, app_code, compatible, paths, pt_addr, boot_min, version):
    def part(member, **extra):
        size, sha = digest(paths[member])
        return {"src": member, "size": size, "cs_sha256": sha, **extra}

    now = datetime.datetime.now(datetime.timezone.utc)
    stem = f"automatous-io-{hardware}-esphome-v{version}-ota"
    manifest = {
        "name": app_code,
        "platform": PLATFORM,
        "version": MANIFEST_VER,
        "build_id": now.strftime("%Y%m%d-%H%M%S") + f"/{stem}",
        "build_timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "parts": {
            "boot":    part("bootloader.bin", type="boot", addr=0x0, min_version=boot_min, encrypt=ENCRYPT),
            "pt":      part("partition-table.bin", type="pt", addr=pt_addr, encrypt=ENCRYPT),
            "otadata": part("otadata.bin", type="otadata", ptn="otadata", encrypt=ENCRYPT),
            "nvs":     {"type": "nvs", "size": NVS_SIZE, "fill": 255, "ptn": "nvs"},
            "app":     part("app.bin", type="app", ptn="app_0", encrypt=ENCRYPT),
            "fs":      part("fs.img", type="fs", ptn="fs_0", fs_size=FS_SIZE, encrypt=ENCRYPT),
        },
        "compatible": compatible,
    }
    manifest_path = os.path.join(tmp, f"manifest-{hardware}.json")
    json.dump(manifest, open(manifest_path, "w"), indent=2)

    zip_out = os.path.join(out_dir, f"{stem}.zip")
    order = ["manifest.json", "bootloader.bin", "partition-table.bin",
             "otadata.bin", "app.bin", "fs.img"]
    src_for = {**paths, "manifest.json": manifest_path}
    with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_STORED) as z:
        for member in order:
            z.write(src_for[member], arcname=member)
    return zip_out


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--hardware", choices=sorted(HARDWARE),
                        help="Shelly hardware to stamp the zip for")
    parser.add_argument("--all-hardware", action="store_true",
                        help="emit one zip per hardware code from the same build (universal image)")
    parser.add_argument("--version", required=True, help="firmware version for the filename, e.g. 1.0.0")
    parser.add_argument("--build-dir", help="ESPHome pioenvs build dir to auto-discover parts in")
    parser.add_argument("--bootloader", help="path to bootloader.bin (overrides --build-dir)")
    parser.add_argument("--partition-table", help="path to the partition table bin (overrides --build-dir)")
    parser.add_argument("--app", help="path to the app bin (overrides --build-dir)")
    parser.add_argument("--otadata", help="path to ota_data_initial.bin (blank otadata generated if absent)")
    parser.add_argument("--pt-addr", default="0x10000", help="partition table offset (default 0x10000)")
    parser.add_argument("--boot-min", default=BOOT_MIN,
                        help="boot part min_version: 99.0.0 forces our bootloader in, "
                             "0.0.0 keeps the stock bootloader (default 99.0.0)")
    parser.add_argument("--app-code", help="override the manifest 'name' (single --hardware only)")
    parser.add_argument("--compatible", help="override the manifest 'compatible' (single --hardware only)")
    args = parser.parse_args()

    if bool(args.hardware) == bool(args.all_hardware):
        parser.error("pass exactly one of --hardware <code> or --all-hardware")
    if args.all_hardware and (args.app_code or args.compatible):
        parser.error("--app-code/--compatible only apply to a single --hardware")

    pt_addr = int(args.pt_addr, 0)

    bd = os.path.abspath(args.build_dir) if args.build_dir else None
    resolved = {
        "bootloader":      args.bootloader      or (bd and find(bd, CANDIDATES["bootloader"])),
        "partition-table": args.partition_table or (bd and find(bd, CANDIDATES["partition-table"])),
        "app":             args.app             or (bd and find(bd, CANDIDATES["app"])),
    }
    otadata = args.otadata or (bd and find(bd, CANDIDATES["otadata"]))
    missing = [k for k, v in resolved.items() if not v or not os.path.isfile(v)]
    if missing:
        sys.exit(f"could not locate: {', '.join(missing)} — pass --build-dir or the explicit paths")

    targets = sorted(HARDWARE) if args.all_hardware else [args.hardware]

    with tempfile.TemporaryDirectory() as tmp:
        fs_img = os.path.join(tmp, "fs.img")
        open(fs_img, "wb").write(b"\xff" * FS_SIZE)
        if not otadata:
            otadata = os.path.join(tmp, "otadata.bin")
            open(otadata, "wb").write(b"\xff" * 0x2000)

        paths = {
            "bootloader.bin":      resolved["bootloader"],
            "partition-table.bin": resolved["partition-table"],
            "otadata.bin":         otadata,
            "app.bin":             resolved["app"],
            "fs.img":              fs_img,
        }

        for hw in targets:
            codes = HARDWARE[hw]
            app_code = args.app_code or codes["app_code"]
            compatible = args.compatible or codes["compatible"]
            zip_out = write_zip(os.getcwd(), tmp, hw, app_code, compatible,
                                paths, pt_addr, args.boot_min, args.version)
            keeps = args.boot_min == "0.0.0"
            print(f"Created {os.path.basename(zip_out)} "
                  f"({os.path.getsize(zip_out) / 1024 / 1024:.1f} MB) — name={app_code}, "
                  f"pt@{hex(pt_addr)}, "
                  + ("keeps stock bootloader" if keeps else "replaces stock bootloader"))


if __name__ == "__main__":
    main()
