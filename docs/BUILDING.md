# Building

**[README](../README.md)** > **Building** · [Report an issue](../../../issues/new)

Firmware is currently distributed as source only, so a build is the first step of an [install](INSTALL.md). Both artifacts are written to the repository root, stamped with the base config's project version.

## Contents

- [In the dev container](#in-the-dev-container)
- [Without a container](#without-a-container)
- [What a build produces](#what-a-build-produces)
- [Strapping pin warnings](#strapping-pin-warnings)

## In the dev container

The repository ships a [dev container](../.devcontainer) pinned to ESPHome 2026.8.2, the image the Home Assistant add-on is built from. Open the repository in VS Code, choose Reopen in Container, and build from its terminal:

```bash
python3 scripts/build.py shelly-1-gen4
```

ESP-IDF and the toolchain persist in a Docker volume, so only the first build downloads them.

## Without a container

```bash
python3.13 -m venv ~/esphome-venv && source ~/esphome-venv/bin/activate && pip install esphome
python3 scripts/build.py shelly-1-gen4
```

Use Python 3.12 or newer. Current ESPHome requires it, and on an older interpreter pip silently installs a much older ESPHome instead of failing.

A model's build directory under `configs/.esphome/` belongs to whichever environment last built it; delete it before switching between the container and a host venv.

## What a build produces

| Artifact | For |
|---|---|
| `automatous-io-<model>-esphome-vX.Y.Z-ota.zip` | the stock Shelly web UI |
| `automatous-io-<model>-esphome-vX.Y.Z-uart.bin` | esptool over UART |

`--version` overrides the stamped version for test builds. Run `python3 scripts/build.py` with no arguments to list buildable models, then pass one in place of `shelly-1-gen4` above. `esphome compile configs/<model>.yaml` works for a plain compile check.

Builds are verified with ESPHome 2026.7.2 and 2026.8.2.

## Strapping pin warnings

Builds print strapping pin warnings for whichever strapping pins that model wires to a relay, button, or LED — GPIO4, GPIO5, and GPIO15 on the 1 Gen4, GPIO4 on the 1PM, GPIO4 and GPIO5 on the 1PM Mini and the 2PM, plus a USB-Serial-JTAG note for the 1PM Mini's switch input and the 2PM's button, both on GPIO12. They are benign; Shelly's hardware dictates those pins.

## Related documentation

- [README](../README.md) — project overview and supported devices
- [Installing](INSTALL.md) — what to do with the artifacts
- [The Partition System](PARTITIONS.md) — what makes these builds boot on Gen4 hardware
- [GPIO Map](GPIO.md) — the pin assignments behind the strapping warnings
