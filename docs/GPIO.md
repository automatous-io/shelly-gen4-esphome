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

## Related documentation

- [README](../README.md) — project overview, install, and adoption
- [The Partition System](PARTITIONS.md) — the stock flash layout and the web UI slot rule
- [Changelog](../CHANGELOG.md) — per-model release notes
