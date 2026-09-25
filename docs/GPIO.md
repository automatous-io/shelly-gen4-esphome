# GPIO Map

**[README](../README.md)** > **GPIO Map** · [Report an issue](../../../issues/new)

The Gen4 devices are built on the ESP-Shelly-C68F, a Shelly module that carries an Espressif ESP32-C6 with 8MB of flash. The module is common across the Gen4 line, but the pins Shelly wires to the relay, button, switch input, status LED, and meter differ by device.

Every pin on this page was verified on real hardware. The same map is kept in [shelly-1-gen4-matter-thread](https://github.com/automatous-io/shelly-1-gen4-matter-thread/blob/main/docs/GPIO.md).

## Contents

- [Shelly 1 Gen4](#shelly-1-gen4)
- [Shelly 1PM Gen4](#shelly-1pm-gen4)
- [Shelly 1 Mini Gen4](#shelly-1-mini-gen4)
- [Shelly 1PM Mini Gen4](#shelly-1pm-mini-gen4)
- [Shelly 2PM Gen4](#shelly-2pm-gen4)

## Shelly 1 Gen4

Hardware Revision: v0.1.2

Verified: May 2026

| Function | GPIO |
|---|---|
| Relay | GPIO5 |
| Switch input | GPIO10 |
| Button (onboard) | GPIO4, active-low |
| Status LED | GPIO15, active-low |

The relay, switch input, button, and status LED are all confirmed on real hardware. This map was established in [shelly-1-gen4-matter-thread](https://github.com/automatous-io/shelly-1-gen4-matter-thread/blob/main/docs/GPIO.md).

## Shelly 1PM Gen4

Hardware Revision: v0.1.2

Verified: June 2026

| Function | GPIO |
|---|---|
| Relay | GPIO4 |
| Switch input | GPIO10 |
| Button (onboard) | GPIO1, active-low |
| Status LED | GPIO11, active-low |
| Power meter (BL0942) | TX GPIO6, RX GPIO7, UART1, 9600 baud |
| NTC | GPIO3 |

The relay, switch input, button, status LED, BL0942 power meter, and NTC are all confirmed on real hardware. The starting map was the community [Shelly 1PM Gen 4 page](https://devices.esphome.io/devices/shelly-1pm-gen-4/) on ESPHome Devices. The BL0942 runs at 9600 baud, not the chip's 4800 default, and the status LED is on GPIO11.

## Shelly 1 Mini Gen4

Hardware Revision: v0.1.2

Verified: September 2026

| Function | GPIO |
|---|---|
| Relay | GPIO10 |
| Switch input | GPIO12 |
| Button (onboard) | GPIO22, active-low |
| Status LED | GPIO5, active-low |
| NTC | GPIO4 |

The relay, switch input, button, status LED, and NTC are all confirmed on real hardware. The map is the 1PM Mini's without the meter, taken from shelly-1-gen4-matter-thread's [GPIO reference](https://github.com/automatous-io/shelly-1-gen4-matter-thread/blob/main/docs/GPIO.md).

Stock firmware holds the relay and LED pads on this board too (see the [1PM Mini](#shelly-1pm-mini-gen4) below). The hold register read GPIO5 and GPIO10 on the first boot after a web UI conversion from stock 2.0.0, so the config releases both at boot.

## Shelly 1PM Mini Gen4

Hardware Revision: v0.1.1

Verified: September 2026

| Function | GPIO |
|---|---|
| Relay | GPIO10 |
| Switch input | GPIO12 |
| Button (onboard) | GPIO22, active-low |
| Status LED | GPIO5, active-low |
| Power meter (BL0942) | TX GPIO20, RX GPIO19, UART1, 9600 baud |
| NTC | GPIO4 |

The relay, switch input, button, status LED, BL0942 power meter, and NTC are all confirmed on real hardware. No public pin map exists for this board, so every pin was found on the device. The relay (GPIO10), status LED (GPIO5), switch input (GPIO12), button (GPIO22), and NTC (GPIO4) match the 1 Mini Gen4, but the BL0942 is on TX GPIO20 / RX GPIO19 rather than the 1PM's GPIO6/GPIO7.

This board also showed that stock firmware leaves the ESP32-C6's pad hold enabled on the relay and LED pins. A held pad ignores every write until the device loses power, and a web UI conversion only ever soft-resets, so the relay and LED sat frozen until the hold register was read. The config releases both holds at boot.

## Shelly 2PM Gen4

Hardware Revision: v0.1.2

Verified: September 2026

| Function | GPIO |
|---|---|
| Relay 1 (O1) | GPIO5 |
| Relay 2 (O2) | GPIO3 |
| Switch input 1 (S1) | GPIO11 |
| Switch input 2 (S2) | GPIO10 |
| Button (onboard) | GPIO12, active-low |
| Status LED | GPIO18, active-low |
| Power meter (ADE7953) | SDA GPIO6, SCL GPIO7, IRQ GPIO1, I2C |
| NTC | GPIO4 |

Both relays, both switch inputs, the button, status LED, NTC, and ADE7953 power meter are all confirmed on real hardware, with the meter calibrated per channel.

This map deserves a note because the public sources disagree with each other and with the board. The [ESPHome Devices page](https://devices.esphome.io/devices/shelly-plus-2pm-gen-4/) contradicts its own YAML, the [Tasmota template](https://templates.blakadder.com/shelly_2PM_gen4.html) has the status LED on GPIO2 and the ESPHome page has it on GPIO0, and it is actually on GPIO18, found by probing every free pin. [`configs/shelly-2pm-gen4.yaml`](../configs/shelly-2pm-gen4.yaml) records which source each pin came from.

## Related documentation

- [README](../README.md) — project overview and supported devices
- [Calibrating the Power Meter](CALIBRATION.md) — the metering constants measured on these boards
- [The Partition System](PARTITIONS.md) — the stock flash layout and the web UI slot rule
- [Changelog](../CHANGELOG.md) — per-model release notes
