# Roadmap

**[README](../README.md)** > **Roadmap** · [Report an issue](../../../issues/new)

What is planned, what it depends on, and what is in the way. Nothing here is on a device yet. Each item ships only after it is verified on real hardware, the same rule every supported model went through.

## Contents

- [Safety shutoff](#safety-shutoff)
- [Thread](#thread)

## Safety shutoff

**Status: planned. Nothing upstream is in the way.**

The metering models can cut their own output. Stock firmware does this already — the 1PM Gen4 takes a [maximum power threshold and shuts the output off](https://us.shelly.com/blogs/documentation/shelly-1pm-gen4-device-smart-control) when the draw passes it — and it needs no hardware beyond what is already mapped and calibrated.

The shape it would take:

- A power limit per channel on the metering models, and a temperature limit on every model with an NTC. Substitutions for the build default, plus `number` entities so they are adjustable at runtime without a rebuild.
- The trip latches. The relay goes off and stays off until it is cleared, so flipping the wall switch does not walk straight back into the fault.
- A binary sensor for the tripped state and a button to clear it, so automations can see it and Home Assistant can reset it.
- Per model: the 1PM, 1PM Mini, and 2PM get both halves, the 2PM per channel. The 1 Mini has an NTC but no meter, so it gets the temperature half only. The 1 Gen4 has neither, so it gets nothing.

**What this is not.** `power_update_interval` defaults to 10s and the meters publish on that cadence, so this is a slow overload and thermal guard measured in seconds, not a circuit breaker. It cannot react to a short, and it replaces neither the breaker in the panel nor correctly rated wiring and a correctly sized load. It is a convenience limit, not a protective device.

## Thread

**Status: possible today, unproven on this hardware.**

ESPHome's [openthread component](https://esphome.io/components/openthread/) runs the native Home Assistant API over Thread's IPv6 instead of Wi-Fi, and has supported the ESP32-C6 since ESPHome 2025.6. The ESP-Shelly-C68F carries that 802.15.4 radio, and nothing in an ESPHome build uses it today.

What it needs:

- A Thread border router to bridge the mesh to your network.
- The Thread network's credentials compiled into the build, as the hex TLV dataset your Thread integration hands out.
- Headroom in the app slot. Shelly's layout gives 3MB per slot rather than the default 3.75MB, so a Thread build has to fit that ceiling. See [The Partition System](PARTITIONS.md).

One documented sharp edge: `esphome.ota` does not work while a sleepy end device is polling (`poll_period > 0`). A mains-powered relay has no reason to sleep and would run as a full Thread device, so this should not bite here, but it is the thing to check first if OTA goes quiet.

**This is not Matter.** A device on Thread this way still speaks the ESPHome native API, so Home Assistant works and Apple Home, Google Home, and Alexa do not. For Matter over Thread on the same hardware, that is [shelly-1-gen4-matter-thread](https://github.com/automatous-io/shelly-1-gen4-matter-thread) — different firmware, different tradeoffs, and no ESPHome.

## Related documentation

- [README](../README.md) — project overview and supported devices
- [Customizing](CUSTOMIZING.md) — the substitutions and ids these features would extend
- [Calibrating the Power Meter](CALIBRATION.md) — the metering a safety shutoff would trip on
- [The Partition System](PARTITIONS.md) — the 3MB app slot a Thread build has to fit
- [Changelog](../CHANGELOG.md) — what has actually shipped
