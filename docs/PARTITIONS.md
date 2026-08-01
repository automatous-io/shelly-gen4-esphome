# The Partition System

**[README](../README.md)** > **The Partition System** · [Report an issue](../../../issues/new)

This page explains why a standard ESPHome build does not boot on a Shelly Gen4, and how this project's builds do. It is background reading. Nothing on this page needs to be configured or acted on; every build, local or adopted, wires all of it in automatically.

If you have searched for ESPHome or Tasmota on a Gen4 device, you have probably read that it cannot be flashed via web UI. The obstacles were real, but they were never about the chip; both projects run on the ESP32-C6. The stock installer's package format was largely undocumented, so there was no conversion path that did not start with UART. And a stock-standard image does not boot on this hardware because of where Shelly now puts the partition table. Neither problem turned out to be fundamental, and there is no locked bootloader in the way. The flash layout and the delivery format are exactly what this project solves.

## The two layouts

ESP32 flash is a single address space, and the partition table is a small index that records where the app slots and data regions live. Two parties must agree on where the table itself sits: the bootloader, which has the offset compiled in, and anything that writes flash. The ESP-IDF convention places it at 0x8000, and this is the layout ESPHome generates for an 8MB ESP32-C6 build when nothing overrides it:

| Partition | Offset | Size |
|---|---|---|
| bootloader | 0x0 | 32 KB |
| partition table | 0x8000 | 4 KB |
| otadata | 0x9000 | 8 KB |
| phy_init | 0xB000 | 4 KB |
| app0 | 0x10000 | 3.75 MB |
| app1 | 0x3D0000 | 3.75 MB |
| nvs | 0x790000 | 448 KB |

Shelly instead places the table at 0x10000. This is the layout this project ships, the master copy being [`shelly-gen4-stock.csv`](../components/shelly_gen4_partition/shelly-gen4-stock.csv):

| Partition | Offset | Size |
|---|---|---|
| bootloader | 0x0 | 64 KB |
| partition table | 0x10000 | 4 KB |
| otadata | 0x11000 | 8 KB |
| nvs | 0x14000 | 48 KB |
| app_0 | 0x20000 | 3 MB |
| fs_0 | 0x320000 | 896 KB |
| app_1 | 0x400000 | 3 MB |

The partition names are part of the compatibility surface, not cosmetic: the stock installer places OTA package parts by name, so `app_0` with the underscore matters, and `fs_0` stays in the table because the installer requires an fs part in every package it accepts.

The mismatch between the two layouts bites in two independent ways. A default ESPHome bootloader looks for the table at 0x8000 and finds nothing there, so nothing boots. And even a build that knows about 0x10000 must describe the same geography as the stock table, because the conversion process writes parts to addresses the stock firmware looks up in the table it already has.

## How conversion writes flash

The stock web UI installer accepts a zip containing a manifest and a set of parts. [`make-esphome-ota-zip.py`](../scripts/make-esphome-ota-zip.py) builds that zip from an ESPHome build. The otadata, nvs, app, and fs parts are written by partition name, and the running stock firmware resolves those names using the partition table it already has.

The named parts are placed with the old table and read, after reboot, with the new one. If the incoming table described a different layout, the installer would write the app where the old table says `app_0` lives and the new firmware would look for it where the new table says it lives. Keeping the two tables identical makes the handoff safe.

The UART path (`build.py`'s `-uart.bin`) is the same layout with different delivery: bootloader, table, otadata, and app merged into one image at their real offsets and flashed at 0x0 with esptool.

## How every build stays in agreement

Adopted devices rebuild from this repository on machines that have never seen it, so the layout knowledge has to travel with the config. Three pieces carry it.

The CSV above is the master copy. The `shelly_gen4_partition` external component registers that CSV as the build's `partitions.csv`, which makes ESPHome skip generating its own table; the base config pulls the component from this repository on GitHub. A fresh machine gets the table as part of the build. And `CONFIG_PARTITION_TABLE_OFFSET: "0x10000"` in the base config is compiled into the bootloader and app so the firmware looks for the table where it actually is.

The failure modes of removing them are asymmetric. Without the component, the build fails outright: ESPHome sizes its auto-generated layout for a table at 0x8000, and with the table pushed to 0x10000 everything slides 64KB up and the last partition runs 64KB past the end of the 8MB chip. That is a build error on the bench, never damage to a device. Without the offset pin, the firmware builds and installs but the bootloader cannot find the table at boot. Both pieces are load-bearing, which is why the README asks you to leave the base's `esp32:` block, `external_components` entry, and `shelly_gen4_partition:` alone.

## Updates after conversion

ESPHome OTA sends only an app image. The device writes it into whichever 3MB app slot it is not currently running from, then flips otadata to mark the new slot bootable. The practical consequence of the layout is app slots of 3MB instead of the default layout's 3.75MB, and that 3MB is the ceiling for how large a firmware image can grow.

## Related documentation

- [README](../README.md) — project overview, install, and customization
- [Flashing Guide](https://github.com/automatous-io/shelly-1-gen4-matter-thread/blob/main/docs/FLASHING.md) — UART wiring, flash mode, and the full-chip backup procedure, from the Matter over Thread project
- [Reversibility](https://github.com/automatous-io/shelly-1-gen4-matter-thread/blob/main/docs/REVERSIBILITY.md) — warranty, factory keys, and restore test evidence, from the Matter over Thread project
