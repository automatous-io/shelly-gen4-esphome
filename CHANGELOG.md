# Changelog

**[README](README.md)** · [Report an issue](../../issues/new)

All notable changes to this project are recorded here. The project version is
repo-wide: every model shares it, and `project.name` in Home Assistant identifies
which device a build is for. Each release lists the models it actually affects, so
a rebuild that only bumps the version string is easy to tell apart from a real change.

Versions stay on 0.0.x while the project is in beta.

---

## 0.0.8

**Shelly 1 Mini Gen4 — new, working on hardware.**

- Added [`configs/shelly-1-mini-gen4.yaml`](configs/shelly-1-mini-gen4.yaml): relay, switch
  input, button, status LED, and the onboard NTC. Entities, selects, substitutions, and stable
  ids match the 1PM Mini Gen4 minus the meter, so existing `!extend` guidance applies unchanged.
- Confirmed the pin map on real hardware: relay GPIO10, switch GPIO12, button GPIO22, status
  LED GPIO5, NTC GPIO4. It is the 1PM Mini's map without the BL0942, and matches the
  hardware-verified 1 Mini map in shelly-1-gen4-matter-thread's
  [GPIO reference](https://github.com/automatous-io/shelly-1-gen4-matter-thread/blob/main/docs/GPIO.md).
- **Stock firmware holds the relay and LED pads on this board too.** A diagnostic build that
  reads `LP_AON.gpio_hold0` before anything else runs listed exactly GPIO5 and GPIO10 on the
  first boot after a web UI conversion from stock 2.0.0. The config calls `gpio_hold_dis` on
  both at boot, as the 1PM Mini does.
- The NTC uses the 1PM Mini's divider and beta value; it reads a few degrees above the die
  sensor at idle, the same gap as the 1PM Mini.
- Closes [#6](../../issues/6).

**Documentation**

- README: 1 Mini in the supported devices table, its pin map source and the pad hold result,
  and the NTC substitution split out from the metering ones.

**Shelly 1 Gen4, 1PM Gen4, 1PM Mini Gen4, and 2PM Gen4 — no functional change.** Only the
version string in the shared base package moves.

---

## 0.0.7

**Shelly 1PM Mini Gen4 — new, working on hardware.**

- Added [`configs/shelly-1pm-mini-gen4.yaml`](configs/shelly-1pm-mini-gen4.yaml): relay, switch
  input, button, status LED, BL0942 power metering, and the onboard NTC. Entities, selects,
  substitutions, and stable ids match the 1PM Gen4, so existing `!extend` guidance applies unchanged.
- Confirmed the full pin map on real hardware: relay GPIO10, switch GPIO12, button GPIO22,
  status LED GPIO5, NTC GPIO4, BL0942 on TX GPIO20 / RX GPIO19 at 9600 baud.
- No public pin map exists for this board. The relay, switch, button, LED, and NTC turned out
  to match the 1 Mini Gen4. The BL0942 does not follow the 1PM Gen4's GPIO6/GPIO7; it was found
  with a scanner firmware that sends the meter's read command on every free pin pair at each
  baud rate the chip supports and stops at the first checksum-valid reply.
- **Stock firmware leaves ESP32-C6 pad hold enabled on the relay and LED pins.** A held pad
  ignores every write until the device loses power, and a web UI conversion only soft-resets,
  so after conversion the LED sat solid on and no pin moved the relay or LED, including the
  correct ones. Reading the hold register (`LP_AON.gpio_hold0`) listed exactly GPIO5 and GPIO10.
  The config calls `gpio_hold_dis` on both at boot. Whether the other models' stock firmware
  does the same has not been checked; a power cycle clears it either way.
- The whole bring-up was done over the stock web UI and OTA with no UART access: a base-only
  image first to prove conversion, Wi-Fi, and OTA before any pin was configured, then probe
  builds over OTA.
- Calibrated the power meter against a reference meter at a ~139W resistive load. ESPHome's
  stock constants would read about 8.4% low on voltage and 1.7% high on current here. Starting
  from the 1PM Gen4's references instead:

  | Channel | 1PM Gen4 references | After |
  |---|---|---|
  | Voltage | +0.6% | within the reference meter's 1V resolution |
  | Current | about +1% | +0.4% |
  | Power | +1.2% | −0.5% |
  | Frequency | exact | exact |

  The device shows current to two decimals and the reference meter shows whole volts, so the
  After column is approximate. The two boards' references land within 1% of each other.
  `power_reference` is left unset as on the 1PM.
- Added the stock installer hardware code `Mini1PMG4` so `scripts/build.py shelly-1pm-mini-gen4`
  produces the web UI zip and UART image.

**Documentation**

- README: 1PM Mini in the supported devices table, how its pins were found and the pad hold
  finding, BL0942 substitution defaults per board, and credits.

**Shelly 1 Gen4, 1PM Gen4, and 2PM Gen4 — no functional change.** Only the version string in
the shared base package moves.

---

## 0.0.6

**Shelly 2PM Gen4 — new, working on hardware.**

- Added [`configs/shelly-2pm-gen4.yaml`](configs/shelly-2pm-gen4.yaml): two relays with their own
  Latch/Momentary and pulse selects, two switch inputs, button, status LED, ADE7953 two-channel
  power metering over I2C, and the onboard NTC. Relay 1 keeps the shared stable ids (`relay_1`,
  `relay_mode_select`, `pulse_select`); relay 2 adds `relay_2`, `relay_2_mode_select`, `pulse_2_select`.
- Confirmed the full pin map on real hardware: relay 1 GPIO5, relay 2 GPIO3, switch 1 GPIO11,
  switch 2 GPIO10, button GPIO12, status LED GPIO18, NTC GPIO4, ADE7953 on I2C GPIO6/GPIO7.
- The public sources disagree with each other and with the board. The ESPHome Devices page's
  pinout table contradicts its own YAML; the Tasmota template puts the LED on GPIO2 and an
  ADE7953 reset line on GPIO0; the ESPHome page puts the LED on GPIO0. The LED is on GPIO18,
  found by probing every free pin with a switch-per-GPIO firmware, and the meter needs no
  reset line driven.
- Calibrated the meter against a reference meter at a ~143W resistive load, one channel at a
  time. ESPHome's ADE7953 defaults are the Shelly 2.5's, and this board's shunts differ, so out
  of the box it reads current and power about 3.7x low with the sign reversed on both channels.

  | Channel | Before | After |
  |---|---|---|
  | Voltage | +1.9% | calibrated |
  | Current 1 | −73% | −0.8% |
  | Power 1 | −127% (sign reversed) | −0.3% |
  | Current 2 | −73% | −2.3%, then nudged per channel |
  | Power 2 | −127% (sign reversed) | −1.4%, then nudged per channel |

  Scaling is done with per-reading multipliers rather than the chip's 4x hardware gain, which
  another Gen4 ADE7953 board found to revert to 1x after resets. `voltage_multiplier`, per-channel
  current and power multipliers, and `current_pga_gain` are substitutions.
- Energy per channel is integrated from power on the device, since ESPHome reads no energy
  counter from the ADE7953, and kept in flash across reboots. The integrator sees power
  clamped at zero so idle noise or a wrong sign cannot walk the total backwards, which Home
  Assistant would read as a meter reset; the power sensors themselves are not clamped.
- Added the stock installer hardware code `S2PMG4` so `scripts/build.py shelly-2pm-gen4` produces
  the web UI zip and UART image.

**Web UI install: the slot rule.** Applies to every model.

- The stock installer writes to the app slot it is not running from, and the zip only converts a
  device running stock from slot 1. On slot 0 the installer logs `Skipping app`, stalls at 87%,
  and writes nothing. Factory firmware runs from slot 0 and every stock update flips the slot,
  which is why every earlier conversion, all done after one stock update, worked. Found on the
  2PM, which was converted straight from factory firmware. README now says to check `slot` in
  the device info first and install any stock firmware if it reads 0; the mechanism and both log
  signatures are in [docs/PARTITIONS.md](docs/PARTITIONS.md#the-slot-rule).

**Documentation**

- README: 2PM in the supported devices table, the pin-map provenance, substitution tables split
  per meter, ADE7953 calibration arithmetic and why the hardware gain is left alone, Home
  Assistant screenshots under load, the slot check in Install, and credits.

**Shelly 1 Gen4 and 1PM Gen4 — no functional change.** Only the version string in the shared
base package moves.

---

## 0.0.5

**Shelly 1PM Gen4 — new, working on hardware.**

- Added [`configs/shelly-1pm-gen4.yaml`](configs/shelly-1pm-gen4.yaml): relay, switch input,
  button, status LED, BL0942 power metering, and the onboard NTC. Relay behavior, the
  Latch/Momentary selects, and the factory-reset hold match the 1 Gen4, and the stable ids
  are shared so existing `!extend` guidance applies unchanged.
- Confirmed the full pin map on real hardware (hw rev v0.1.2): relay GPIO4, switch GPIO10,
  button GPIO1, status LED GPIO11, BL0942 on GPIO6/GPIO7, NTC GPIO3.
- The BL0942 runs at **9600 baud**, not the chip's 4800 default. A mismatch shows up as
  `BL0942 setup failed!` at boot, which is the mode-register readback failing.
- Calibrated the power meter against a reference meter at a 139W resistive load. ESPHome's
  stock constants assume the BL0942 reference design, and Shelly uses a different voltage
  divider, so this board reads about 9% low on voltage out of the box.

  | Channel | Before | After |
  |---|---|---|
  | Voltage | −8.89% | +0.42% |
  | Current | +1.02% | +0.08% |
  | Power | −7.84% | +0.14% |
  | Frequency | exact | exact |

  `power_reference` and `energy_reference` are left unset: the driver derives both from
  voltage × current, and the derived value beats setting it by hand.

  Measured on one unit against a consumer meter, so another board lands within a couple of
  percent rather than exactly on. Both constants are substitutions and can be overridden
  per device.

**Documentation**

- Added [Calibrating the power meter](README.md#calibrating-the-power-meter) to the README,
  covering the arithmetic, the `power_reference` derivation trap, and why a 100W+ resistive
  load is needed.
- Added Home Assistant screenshots of the 1PM under load.
- Noted the Python 3.12 minimum in Building. On an older interpreter pip installs a much
  older ESPHome that builds through PlatformIO, which rejects any project path containing
  a space.
- Generalized the install, adoption, and build sections away from `shelly-1-gen4` as the
  only worked example.
- Credited ESPHome Devices, which the 1PM config started from.
- Added this changelog.

**Shelly 1 Gen4 — no functional change.** The only edit to the shared base package is the
version string, so a 1 Gen4 rebuilt at 0.0.5 is identical to 0.0.4 apart from the version
it reports.

---

## 0.0.4

Initial public release.

- Shelly 1 Gen4 support ([`configs/shelly-1-gen4.yaml`](configs/shelly-1-gen4.yaml)) on a
  shared Gen4 base package.
- Stock partition layout shipped to every build, including adopted and remote builds, via
  the `shelly_gen4_partition` external component. See [docs/PARTITIONS.md](docs/PARTITIONS.md).
- Build tooling: `scripts/build.py` produces both a stock-web-UI OTA zip and a UART
  full-flash image, stamped from the base config's project version.
- Relay restore mode, input debounce, log level, AP password, and factory-reset hold exposed
  as substitutions.
- README, Home Assistant screenshots, and the partition system writeup.
