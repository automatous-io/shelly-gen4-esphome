# Customizing

**[README](../README.md)** > **Customizing** · [Report an issue](../../../issues/new)

Your [adoption stub](ADOPTION.md#adoption-and-the-stub) is where customization lives. Substitutions are the main knobs; beyond them, standard ESPHome package merging reaches into anything the config declares.

## Contents

- [Substitutions](#substitutions)
- [All models](#all-models)
- [Models with an NTC](#models-with-an-ntc)
- [Metering models](#metering-models)
- [Package merging and stable ids](#package-merging-and-stable-ids)

## Substitutions

Add one to the stub's `substitutions:` block and rebuild, and your value overrides the default on every build after. For example:

```yaml
substitutions:
  name: shelly-1-gen4-52ab8c
  friendly_name: Garage Door
  relay_mode: "Momentary"
  relay_pulse: "1 s"
  relay_restore: "ALWAYS_OFF"
```

Add a substitution to the stub only to change it. A default copied into the stub sticks; the device misses any later change to the default in this repository.

Relay linking, relay mode, and pulse length are also select entities in Home Assistant and on the device page; those three substitutions only set starting values.

## All models

| Substitution | Default | Meaning |
|---|---|---|
| `device_name` | the model, e.g. `shelly-1-gen4` | node name and hostname base |
| `friendly_name` | the model, e.g. `Shelly 1 Gen4` | name shown in Home Assistant |
| `relay_linking` | `Linked` | initial switch input linking, `Linked` or `Unlinked`; stock firmware's detached mode (both channels on the 2PM) |
| `relay_mode` | `Latch` | initial relay mode, `Latch` or `Momentary` (both channels on the 2PM) |
| `relay_pulse` | `500 ms` | initial pulse length in Momentary mode (both channels on the 2PM) |
| `relay_restore` | `RESTORE_DEFAULT_OFF` | relay power-on behavior, also `RESTORE_DEFAULT_ON`, `ALWAYS_OFF`, `ALWAYS_ON` |
| `input_debounce` | `50ms` | switch input debounce filter |
| `log_level` | `INFO` | logger verbosity, `DEBUG` or `VERBOSE` for troubleshooting |
| `ap_password` | `automatous` | fallback hotspot password |
| `factory_reset_hold` | `5s` | button hold time before factory reset |

## Models with an NTC

`shelly-1pm-gen4`, `shelly-1-mini-gen4`, `shelly-1pm-mini-gen4`, `shelly-2pm-gen4`:

| Substitution | Default | Meaning |
|---|---|---|
| `ntc_b_constant` | `3350` | NTC beta value; adjust to calibrate the temperature reading |

## Metering models

`shelly-1pm-gen4`, `shelly-1pm-mini-gen4`, `shelly-2pm-gen4`:

| Substitution | Default | Meaning |
|---|---|---|
| `power_update_interval` | `10s` | how often the power meter publishes |

The 1PM and 1PM Mini (BL0942 meter):

| Substitution | Default | Meaning |
|---|---|---|
| `line_frequency` | `60Hz` | mains frequency, `50Hz` outside North America |
| `voltage_reference` | `14462.09548` on the 1PM, `14553.25051` on the 1PM Mini | BL0942 voltage scaling, measured on each board |
| `current_reference` | `253772.51527` on the 1PM, `255278.38517` on the 1PM Mini | BL0942 current scaling, measured on each board |

The 2PM (ADE7953 meter):

| Substitution | Default | Meaning |
|---|---|---|
| `voltage_multiplier` | `0.9811` | voltage scaling, measured on this board |
| `current_1_multiplier`, `current_2_multiplier` | `3.747`, `3.808` | current scaling per channel, measured on this board |
| `power_1_multiplier`, `power_2_multiplier` | `-3.679`, `-3.718` | power scaling per channel, measured on this board; negative because both channels read reversed |
| `current_pga_gain` | `1x` | ADE7953 current channel hardware gain; leave at `1x`, see [Calibrating the Power Meter](CALIBRATION.md) |

The 2PM has no `line_frequency` setting because the ADE7953 measures mains frequency itself; a 50Hz unit reports 50Hz with nothing to configure. The shipped multipliers were measured at 120V and the chip is linear, so they apply at 230V too.

Changing these to match your own unit is [Calibrating the Power Meter](CALIBRATION.md).

## Package merging and stable ids

Standard ESPHome package merging applies: dictionaries deep-merge with the stub winning, lists append, and `!extend`/`!remove` reach into the package by id. What your stub merges over is exactly your model's config in [`configs/`](../configs) plus the shared [`configs/shelly-gen4-base.yaml`](../configs/shelly-gen4-base.yaml), so read those to see everything there is to change.

Every model uses the same stable ids for the parts it has — `relay_1`, `relay_linking_select`, `relay_mode_select`, `pulse_select`, and `btn_factory_reset`. Models with an NTC add `sensor_temperature`, and metering models add `sensor_voltage` and `sensor_frequency`. The 1PM and 1PM Mini have `sensor_current`, `sensor_power`, `sensor_energy`, and `uart_bl0942`. The 2PM has `relay_2`, `relay_2_linking_select`, `relay_2_mode_select`, `pulse_2_select`, per-channel `sensor_current_1`/`_2`, `sensor_power_1`/`_2`, `sensor_energy_1`/`_2`, and `ade7953_meter` on the `i2c_ade7953` bus:

```yaml
switch:
  - id: !extend relay_1
    icon: mdi:garage
```

Leave the base's `esp32:` block, `external_components` entry, and `shelly_gen4_partition:` alone; they are the [partition wiring](PARTITIONS.md).

## Related documentation

- [README](../README.md) — project overview and supported devices
- [First Boot and Adoption](ADOPTION.md) — where the stub comes from and how it updates
- [Calibrating the Power Meter](CALIBRATION.md) — measuring the metering constants on your own unit
- [The Partition System](PARTITIONS.md) — the blocks to leave alone and why
