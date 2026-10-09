# Changelog

**[README](README.md)** · [Report an issue](../../issues/new)

All notable changes to this project are recorded here. The project version is
repo-wide: every model shares it, and `project.name` in Home Assistant identifies
which device a build is for. Each release lists the models it actually affects, so
a rebuild that only bumps the version string is easy to tell apart from a real change.

---

## 1.5.1

**Fixes a build failure coming with ESPHome 2026.10.0.** Affects the six relay models: the 1,
1PM, 1 Mini, 1PM Mini, 2PM, and Plug US. The EM Mini is unchanged apart from the version string.

- The overheat check read the temperature through `raw_state`, which ESPHome deprecated and
  removes in 2026.10.0. On 2026.9 it compiled with a warning; on 2026.10.0 it would not compile.
- It now reads the same value with `get_raw_state()`. Behavior is unchanged.
- Adopted devices pick this up on their next rebuild.
- Reported by [@Gionames](https://github.com/Gionames) in [#29](../../issues/29).
- All seven models build on ESPHome 2026.8.2 and on 2026.10.0b2. Verified on the 1 and
  the 2PM (both channels), which cover the die sensor and the NTC: each relay turns on and
  stays on with no Overheating fault at normal temperature.

---

## 1.5.0

**Overpower, overcurrent, overvoltage, and overheating protection.** Affects the six relay
models: the 1, 1PM, 1 Mini, 1PM Mini, 2PM, and Plug US. The EM Mini is unchanged apart from
the version string.

- The relay turns off when a reading goes over its limit, and a problem binary sensor shows
  which: `Overpower`, `Overcurrent`, `Overvoltage`, or `Overheating`. The fault stays on until
  the relay is turned back on.
- New `Max Power`, `Max Current`, and `Max Voltage` number entities on the 1PM, 1PM Mini, 2PM,
  and Plug US. Each defaults to the device's rating, which is also its ceiling; set power
  and current to the load on the circuit. On the 2PM, power and current are per channel.
- Overheating trips at 95 °C, Shelly's documented limit, on every relay model. It reads the
  NTC where there is one and the ESP32-C6 die temperature on the 1 and Plug US.
- Limits per model and the substitutions are in
  [Customizing](docs/CUSTOMIZING.md#protections). The base's Internal Temperature sensor now
  has the id `sensor_internal_temperature`.
- Adopted devices pick this up on their next rebuild.
- Requested by [@stargazer992](https://github.com/stargazer992) in [#23](../../issues/23).
- Verified on all six. Overheating trips and blocks turn-on on every model. On the Plug US,
  Overpower, Overcurrent, and Overvoltage tripped on a 140 W load test. Overvoltage also tripped on
  the 1PM, 1PM Mini, and 2PM, and the 2PM's channels tripped independently. The Plug's stock
  defaults, read from two units, are its 1800 W / 15 A / 150 V.

---

## 1.4.2

**Fixes Momentary pulses being cut short.** Affects the six relay models: the 1, 1PM, 1 Mini,
1PM Mini, 2PM, and Plug US. The EM Mini is unchanged apart from the version string.

- In Momentary mode, turning the relay back on before its pulse ended let the earlier pulse's
  timer turn it off early, so the new pulse was cut short. A garage door opener can miss a
  pulse that short.
- Every pulse now runs its full length, and turning the relay off mid-pulse cancels the
  pending turn-off. On the 2PM each channel keeps its own timer.
- Adopted devices pick this up on their next rebuild.
- Reported by [@stargazer992](https://github.com/stargazer992) in [#23](../../issues/23).
- Verified on the 2PM (both channels), 1 Mini, 1PM, and Plug US. On the 1 Mini and 1PM the
  cut-short pulse was reproduced on 1.4.1 first. The 1 and 1PM Mini use the same relay code.

---

## 1.4.1

**Fixes the fallback hotspot on 1.4.0.** Affects all seven models; update from 1.4.0.

- On 1.4.0 the Bluetooth scan ran continuously from boot and starved the fallback hotspot.
  Joining it failed as if the password were wrong, so a fresh conversion could not be set up,
  and a device that lost Wi-Fi could not be reached through its hotspot.
- The scan now runs only while Wi-Fi is connected. It starts when Wi-Fi connects, stops when
  it drops, and the hotspot has the radio to itself. The `Bluetooth Proxy` switch works as
  before.
- A 1.4.0 device stuck on its hotspot recovers once the Wi-Fi it knows is back in range; update
  it to 1.4.1 from there.
- Dropping the proxy from a build now also removes two Wi-Fi triggers; see
  [Customizing](docs/CUSTOMIZING.md#package-merging-and-stable-ids).
- Verified on the Plug US: a fresh web UI conversion joins the hotspot first try, a device that
  lost Wi-Fi opens its hotspot and captive portal, and the proxy resumes when Wi-Fi returns.

---

## 1.4.0

**Bluetooth proxy on every model.** The ESP32-C6's Bluetooth radio, unused until now, relays
nearby Bluetooth devices to Home Assistant. Affects all seven models.

- Home Assistant discovers each device as a Bluetooth adapter and routes every Bluetooth
  device through whichever adapter hears it best. Active mode, so Home Assistant can also
  connect through the proxy to devices that need a connection, like locks.
- New `Bluetooth Proxy` switch, on by default and restored after a restart. Off stops the
  scan and shuts the Bluetooth stack down at runtime, returning about 55 KB of memory, with
  no rebuild. To drop the proxy from a build entirely, see
  [Customizing](docs/CUSTOMIZING.md#package-merging-and-stable-ids).
- New `Free Memory` and `Largest Free Memory Block` diagnostic sensors on every model.
- The proxy adds about 600 KB to the app image, which still uses under 55% of the app slot.
- Adopted devices pick this up on their next rebuild.
- New stable ids: `ble_tracker` and `bluetooth_proxy_switch`. Existing ids, substitution
  names, and package URLs are unchanged.
- Verified on all seven models: the device shows as a Bluetooth adapter, the switch stops and
  restarts advertisements in real time, and metering, the RTC, and the relays are unaffected.

---

## 1.3.0

**Shelly EM Mini Gen4 — new, working on hardware.**

- Added [`configs/shelly-em-mini-gen4.yaml`](configs/shelly-em-mini-gen4.yaml): button, status
  LED, BL0942 power meter on the included CT clamp, the NTC, and the battery-backed RTC. The
  web UI zip carries the stock app code `MiniEMG4`.
- Found every pin on the device: button GPIO22, status LED GPIO5, BL0942 TX GPIO20 / RX GPIO19,
  NTC GPIO4, the 1PM Mini's map without the relay and switch input, plus the RTC on I2C at
  GPIO10/GPIO11. See the [GPIO Map](docs/GPIO.md#shelly-em-mini-gen4).
- The meter is calibrated against a reference meter (`voltage_reference` 14491.65075,
  `current_reference` 251625.18057).
- The EM Mini's stock flash layout has smaller app and fs slots than the rest of the line, so
  the shared partition table is rejected by its installer. `shelly_gen4_partition` takes a
  `layout:` option, `standard` by default and `em_mini` for this model, and the zip carries the
  matching 768 KB fs part. See [The Partition System](docs/PARTITIONS.md#the-em-mini-layout).
- The RTC (PCF8563-compatible, 0x51) is read at boot. The clock is valid before Wi-Fi
  connects, and Home Assistant's time is written back to it on every sync. `RTC Time` shows
  what the chip holds, or `not set` after it lost power.
- Stock firmware holds the LED pad, so the config releases GPIO5 at boot.
- `build.py` builds the checkout's own partition component rather than the copy on `main`.
- Other models are unchanged apart from the version string.

---

## 1.2.0

**Shelly Plug US Gen4 — new, working on hardware.**

- Added [`configs/shelly-plug-us-gen4.yaml`](configs/shelly-plug-us-gen4.yaml): relay, button,
  BL0942 power meter, the 12-pixel RGB LED ring, and the LTR-329 light sensor. The web UI zip
  carries the stock app code `PlugUSG4`.
- Found every pin on the device, since no public map exists: relay GPIO4, button GPIO7, LED
  ring GPIO6, BL0942 TX GPIO18 / RX GPIO19, light sensor on I2C at GPIO10/GPIO11. See the
  [GPIO Map](docs/GPIO.md#shelly-plug-us-gen4).
- The meter is calibrated against a reference meter (`voltage_reference` 25169.82830,
  `current_reference` 248840.32040). The BL0942's RX line needs a pull-up on this board.
- `Relay Linking`, `Relay Mode`, and `Pulse Length` as on the relays. Linking applies to the
  button, the Plug's only input: `Unlinked` reports presses without toggling the relay.
- `LED Ring` is a Home Assistant light with color and brightness, and restores its last state
  after a restart. `Ring Mode` matches stock's LED modes: `Power` (default) colors it green to
  red by load up to `ring_max_power`, `Relay State` shows green on and red off, and `Manual`
  leaves it to Home Assistant.
- The ring blinks blue while Wi-Fi or the API is down, at the same rhythm as the status LED on
  the other models, then returns to what it was showing.
- `Illuminance` in lux, calibrated against a light meter (`illuminance_scale` 2.9), and
  `Illumination` as `dark`, `twilight`, or `bright` like stock, with `dark_threshold` (5 lx) and
  `bright_threshold` (100 lx) substitutions.
- Stock firmware holds the relay pad, so the config releases GPIO4 at boot, as on the Minis.
- Other models are unchanged apart from the version string.

---

## 1.1.0

**Detached mode.** The switch input can be unlinked from the relay. The terminal
reports to Home Assistant without driving the output. Affects all five models.

- New `Relay Linking` select per switch input, `Linked` (default) or `Unlinked`, with a
  `relay_linking` substitution for the starting value. The 2PM has one per channel and
  they are independent.
- Unlinked suppresses only the relay toggle; the Switch Input binary sensor reports as
  usual, which is what makes it useful as an automation trigger. The onboard button still
  toggles the relay either way, matching stock.
- New stable ids: `relay_linking_select`, plus `relay_2_linking_select` on the 2PM.
  Existing ids, substitution names, and package URLs are unchanged.
- Verified on the 1 Mini, 1PM, and 2PM. The 1 and 1PM Mini share an identical input
  block with the 1 Mini.
- Contributed by @giannello (#11).

---

## 1.0.0

**First stable release.** No functional change to any model; every config is the 0.0.8 build
with a new version string.

- Five models verified on real hardware: Shelly 1 Gen4, 1PM Gen4, 1 Mini Gen4, 1PM Mini
  Gen4, and 2PM Gen4. The 1PM, 1PM Mini, and 2PM meters are calibrated against a reference
  meter with the constants shipped as substitutions.
- From this release the stable ids (`relay_1`, `relay_mode_select`, `pulse_select`,
  `btn_factory_reset`, and the per-model sensor and relay 2 ids), the substitution names, and
  the package URLs under `configs/` only change with a major version. Adopted stubs tracking
  `main` keep building.
- Still limited: every measurement was made at 120V/60Hz on one unit per model. The BL0942
  models need `line_frequency: "50Hz"` in the stub outside North America; the calibration
  constants should hold at 230V since the chips are linear, but that is unconfirmed. The NTC
  beta value is an estimate on every model. No thermal cutoff on the relay yet.

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

- Added [Calibrating the Power Meter](docs/CALIBRATION.md) to the documentation,
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
