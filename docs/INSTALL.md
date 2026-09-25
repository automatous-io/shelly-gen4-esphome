# Installing

**[README](../README.md)** > **Installing** · [Report an issue](../../../issues/new)

Two ways in. The stock web UI takes one zip over your existing network and needs no adapter, and UART writes the same image with the device open. Both paths write the same layout; only the delivery differs.

Firmware is currently distributed as source only, so [build](BUILDING.md) the artifacts first. A build produces `automatous-io-<model>-esphome-vX.Y.Z-ota.zip` for the stock web UI and `-uart.bin` for esptool over UART.

## Contents

- [Stock web UI](#stock-web-ui)
- [Check the running slot first](#check-the-running-slot-first)
- [UART](#uart)
- [Backing up stock firmware](#backing-up-stock-firmware)

## Stock web UI

Open the Shelly's stock web page, choose to install firmware from a file, and upload the zip. The stock installer verifies it, writes it, and reboots into ESPHome. Conversion is tested from stock firmware 1.7.5 and 2.0.0.

Then go to [First Boot and Adoption](ADOPTION.md).

## Check the running slot first

The stock installer writes to whichever of its two app slots it is not running from, and the zip only converts a device running from slot 1.

Open the stock web page's device info (or call `Shelly.GetDeviceInfo`) and look at `slot`:

- **`slot` is 1** — upload the zip.
- **`slot` is 0** — install any stock firmware first, the offered update or a file upload of an official build. That lands in slot 1 and makes it active, and the zip converts on the next upload.

Factory firmware ships running from slot 0, and each stock update flips the slot, so a device straight out of the box, or one that has taken an even number of stock updates, needs this step.

A zip uploaded on slot 0 does no harm: the installer logs `Skipping app`, stalls at 87%, writes nothing, and the device stays on stock. The mechanism is in [The Partition System](PARTITIONS.md#the-slot-rule).

## UART

```bash
# with the device open, in flash mode, and disconnected from mains
esptool --chip esp32c6 --port <PORT> read-flash 0x0 ALL shelly-<model>-gen4-stock-<MAC>.bin
esptool --chip esp32c6 --port <PORT> write-flash 0x0 automatous-io-shelly-<model>-gen4-esphome-vX.Y.Z-uart.bin
```

The UART wiring, flash mode, and pinout are covered in shelly-1-gen4-matter-thread's [Flashing Guide](https://github.com/automatous-io/shelly-1-gen4-matter-thread/blob/main/docs/FLASHING.md), and apply here unchanged.

## Backing up stock firmware

The web UI cannot back up the stock firmware. If you want the option to return to stock, take the full-chip UART backup above first, before writing anything.

A restored backup returns the device to a fully functional factory state including Shelly Cloud. That path is documented and tested in shelly-1-gen4-matter-thread's [Reversibility](https://github.com/automatous-io/shelly-1-gen4-matter-thread/blob/main/docs/REVERSIBILITY.md) page.

## Related documentation

- [README](../README.md) — project overview and supported devices
- [First Boot and Adoption](ADOPTION.md) — Wi-Fi setup, Home Assistant, and the adoption stub
- [Building](BUILDING.md) — producing the zip and the UART binary
- [The Partition System](PARTITIONS.md) — the stock flash layout and the web UI slot rule
