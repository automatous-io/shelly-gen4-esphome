# Roadmap

**[README](../README.md)** > **Roadmap** · [Report an issue](../../../issues/new)

What is planned, what it depends on, and what is in the way. Nothing here is on a device yet. Each item ships only after it is verified on real hardware, the same rule every supported model went through.

## Contents

- [Thread](#thread)

## Thread

**Status: possible today, unproven on this hardware.**

ESPHome's [openthread component](https://esphome.io/components/openthread/) runs the native Home Assistant API over Thread's IPv6 instead of Wi-Fi, and has supported the ESP32-C6 since ESPHome 2025.6. The ESP-Shelly-C68F carries that 802.15.4 radio, and nothing in an ESPHome build uses it today.

What it needs:

- A Thread border router to bridge the mesh to your network.
- The Thread network's credentials compiled into the build, as the hex TLV dataset your Thread integration hands out.
- Headroom in the app slot. Shelly's layout gives 3MB per slot (2.94MB on the EM Mini) rather than the default 3.75MB, so a Thread build has to fit that ceiling. See [The Partition System](PARTITIONS.md).

One documented sharp edge: `esphome.ota` does not work while a sleepy end device is polling (`poll_period > 0`). A mains-powered relay has no reason to sleep and would run as a full Thread device, so this should not bite here, but it is the thing to check first if OTA goes quiet.

**This is not Matter.** A device on Thread this way still speaks the ESPHome native API, so Home Assistant works and Apple Home, Google Home, and Alexa do not. For Matter over Thread on the same hardware, that is [shelly-1-gen4-matter-thread](https://github.com/automatous-io/shelly-1-gen4-matter-thread) — different firmware, different tradeoffs, and no ESPHome.

## Related documentation

- [README](../README.md) — project overview and supported devices
- [The Partition System](PARTITIONS.md) — the 3MB app slot a Thread build has to fit
- [Changelog](../CHANGELOG.md) — what has actually shipped
