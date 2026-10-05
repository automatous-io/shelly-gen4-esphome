# Safety Lockout

**[README](../README.md)** > **Safety Lockout** · [Report an issue](../../../issues/new)

An optional package that adds a persistent, independent lockout on top of the
relay models' own protections (see [Customizing § Protections](CUSTOMIZING.md#protections)).
Verified on real hardware on a Shelly Plug US Gen4.

## Contents

- [Why this exists](#why-this-exists)
- [What it adds](#what-it-adds)
- [Supported models](#supported-models)
- [Using it](#using-it)
- [New entities](#new-entities)
- [Substitutions](#substitutions)
- [Limits](#limits)

## Why this exists

The built-in Overpower / Overcurrent / Overvoltage / Overheating faults are
necessary but not sufficient on their own:

- Each fault clears the instant the relay is turned back on — from Home
  Assistant, the native API, **or the physical button** — because they all
  funnel through the same `relay_1` `on_turn_on` handler.
- That handler only re-checks voltage and temperature. Current and power are
  not re-checked, so turning the relay back on right after an overcurrent or
  overpower trip is accepted even if the overload is still present.
- Nothing survives a reboot: a power cycle during or right after a fault
  clears it with no record of what happened.

None of this is a bug in the base protections — they are a fast, local
breaker substitute, not a stateful safety layer, and the two are different
jobs. This package is the second one.

## What it adds

- A persistent `safety_locked` latch (`globals`, `restore_value: true`) that
  survives reboot.
- One shared trip path (`safety_trip` script) fed by all four of the model's
  own fault binary sensors, so any of the four faults engages the same latch.
- A hook on `relay_1`'s own `on_turn_on` that refuses to turn on at all while
  locked, and — if not locked — re-checks current and power (closing the
  bypass the base protections leave open) before allowing the relay on.
- A `Safety Reset` button that only clears the lockout if voltage, current,
  power, and temperature are all currently within a margin below their
  limits; otherwise it logs the refusal and leaves the lockout engaged.
- A boot restore of that reason's own fault flag. The model configs seed every
  fault flag `false` at boot, so on their own a reboot would leave `Safety
  Lockout` engaged and `Safety Reason` naming a fault while the matching
  `Over*` flag read `false`. The flag for the persisted reason is published
  back at boot, after the seed, so the three agree.

## Supported models

`shelly-1pm-gen4`, `shelly-1pm-mini-gen4`, `shelly-plug-us-gen4` — the three
single-relay models with the full BL0942 metering set
(`sensor_voltage`/`sensor_current`/`sensor_power`) and all four fault sensors.

**Not supported yet:**

- `shelly-2pm-gen4` — two independent relays and channels; the single-relay
  hooks in this package would need a per-channel rewrite.
- `shelly-1-gen4`, `shelly-1-mini-gen4` — no power meter, so there is no
  overcurrent/overpower/overvoltage fault to latch onto.
- `shelly-em-mini-gen4` — meters but has no relay to lock out.

PRs extending coverage are welcome; keep the per-channel 2PM case as a
separate, explicit set of ids rather than trying to generalize `relay_1`.

## Using it

Add it to your [adoption stub](ADOPTION.md#adoption-and-the-stub) **after**
the model package, so its `!extend` entries have something to extend:

```yaml
packages:
  model: github://automatous-io/shelly-gen4-esphome/configs/shelly-plug-us-gen4.yaml@v1.6.1
  safety_lockout: github://automatous-io/shelly-gen4-esphome/configs/safety-lockout.yaml@v1.6.1
```

The Plug US has no onboard NTC and reads the ESP32-C6 die temperature instead
of `sensor_temperature`; override both of the following together for it
(the 1PM and 1PM Mini need no override):

```yaml
substitutions:
  safety_temperature_sensor_id: sensor_internal_temperature
  safety_temperature_expr: "id(sensor_internal_temperature).raw_state"
```

Pin both packages to the same tag you use for everything else; `safety-lockout.yaml`
follows the same stable-id and merge rules as the model configs (see
[Customizing § Package merging and stable ids](CUSTOMIZING.md#package-merging-and-stable-ids)).

## New entities

| Entity | Type | Notes |
|---|---|---|
| `Safety Lockout` | binary sensor, `problem`, diagnostic | `safety_locked`, survives reboot |
| `Safety Reason` | text sensor, diagnostic | `None`, `Over-temperature`, `Overcurrent`, `Over-power`, `Overvoltage` |
| `Safety Reset` | button, config | refuses while still unsafe; relay stays off after a successful reset |

## Substitutions

| Substitution | Default | Meaning |
|---|---|---|
| `safety_temperature_sensor_id` | `sensor_temperature` | id of the temperature sensor to read; override for the Plug US |
| `safety_temperature_expr` | `id(sensor_temperature).state` | full C++ expression read in the Safety Reset check; override for the Plug US |
| `safety_max_temperature` | `95` | must match the model's own `max_temperature` |
| `safety_overheat_margin_c` | `10.0` | °C the temperature must be below the limit before a reset is accepted |
| `safety_margin_fraction` | `0.9` | fraction of the current/power limit a reset requires (0.9 = 90%) |

## Limits

This is a software latch running on the same ESP32-C6 as everything else. It
is not a substitute for the breaker in the panel or correctly rated wiring,
and it does not react any faster than the base protections it sits on top
of — it changes what happens *after* a trip, not how quickly one is detected.
A firmware crash, a brownout, or a hardware failure downstream of the relay
contacts is outside what any ESPHome-level latch can catch.
