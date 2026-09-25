# Calibrating the Power Meter

**[README](../README.md)** > **Calibrating the Power Meter** · [Report an issue](../../../issues/new)

Applies to the metering models: the 1PM and 1PM Mini with a BL0942, and the 2PM with an ADE7953. Each ships constants measured on real hardware, so this page is optional. Redo it if you want your unit to match your own reference meter.

## Contents

- [BL0942: the 1PM and 1PM Mini](#bl0942-the-1pm-and-1pm-mini)
- [ADE7953: the 2PM](#ade7953-the-2pm)
- [Why the shipped values are measured, not inherited](#why-the-shipped-values-are-measured-not-inherited)
- [Two things](#two-things)

## BL0942: the 1PM and 1PM Mini

The BL0942 reports raw counts that ESPHome divides by a reference constant per channel, so calibration is one division:

```
new_reference = old_reference × (reported ÷ actual)
```

Read `reported` off the device and `actual` off a reference meter at the same moment, then set the result as a substitution in your stub. Frequency needs no calibration; it comes from zero-crossing timing and is already accurate.

## ADE7953: the 2PM

Each ADE7953 reading gets a multiplier instead, so the fraction flips:

```
new_multiplier = old_multiplier × (actual ÷ reported)
```

Voltage is shared, current and power are per channel, and power comes from the chip's own register rather than from voltage × current, so all five multipliers are measured separately. Calibrate one channel at a time with the load on that output, and keep the sign: both channels read negative on this board. The idle noise floor after scaling is about 0.07A per channel, so the same 100W+ resistive load advice applies. Energy is integrated on the device from power clamped at zero, so a wrong sign shows up on the power sensor but never walks the energy total backwards.

The 2PM corrects the scale in software rather than with the chip's 4x hardware gain. The chip's gain registers only reach 2x, so they cannot close the gap on their own, and on the Power Strip 4 Gen4 the hardware gain setting was found to occasionally revert to 1x after a reset, quartering the readings. Tasmota runs this chip at 1x on Shelly 2PM boards for the same reason. `current_pga_gain` is exposed for experiments, but the shipped multipliers assume `1x`.

## Why the shipped values are measured, not inherited

ESPHome's defaults assume other boards. The 1PM's BL0942 reads about 9% low on voltage and 1% high on current out of the box, and the 1PM Mini's about 8% low and 2% high; the two boards' references land within 1% of each other. The 2PM's ADE7953 reads current and power about 3.7x low with the sign reversed on both channels, because ESPHome's driver was written for the Shelly 2.5 and this board's shunts differ.

Each was measured on one unit against a consumer meter at roughly 140W resistive, so expect to land within a couple of percent rather than exactly on.

## Two things

**Only calibrate voltage and current.** On the BL0942 the driver derives `power_reference` from voltage × current, and `energy_reference` from `power_reference` in turn. The chip's power register tracks V × I closely, so once both channels are correct the derived power lands within a fraction of a percent. Setting `power_reference` by hand disables that derivation and makes power worse. Leave it unset.

**Use a load large enough to measure.** The current channel has a noise floor around 0.05A on the unit tested, which is larger than the entire signal from a 5W lamp. It does not behave as a constant offset at real loads, so do not subtract it; just measure somewhere it does not matter. Use 100W or more of resistive load, an incandescent bulb or a heating element. Anything with a switching supply or a motor has a power factor well below 1 and the two meters will disagree for real reasons rather than calibration ones.

## Related documentation

- [README](../README.md) — project overview and supported devices
- [Customizing](CUSTOMIZING.md#metering-models) — the metering substitutions and their shipped values
- [GPIO Map](GPIO.md) — which meter each model carries and how it is wired
