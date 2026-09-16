# Changelog

**[README](README.md)** · [Report an issue](../../issues/new)

All notable changes to this project are recorded here. The project version is
repo-wide: every model shares it, and `project.name` in Home Assistant identifies
which device a build is for. Each release lists the models it actually affects, so
a rebuild that only bumps the version string is easy to tell apart from a real change.

Versions stay on 0.0.x while the project is in beta.

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
