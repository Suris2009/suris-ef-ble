# Suris EcoFlow BLE 0.8.0b5 — 100% local BLE / No internet required · UNOFFICIAL / UNSTABLE BETA

> [!CAUTION]
> **UNOFFICIAL, UNSTABLE BETA. USE WITH CAUTION AND AT YOUR OWN RISK.**
> No warranties are provided. To the maximum extent permitted by law, authors
> and contributors accept no liability for its use or consequences.
> This is not an EcoFlow release or an official rabits/ha-ef-ble release.

**Main benefit: 100% local BLE operation, without internet or EcoFlow cloud.**
Station telemetry and commands use a direct local Bluetooth connection. Monitoring
and control continue when internet access is unavailable, provided Home Assistant,
Bluetooth, and the station remain available. Cloud sign-in during setup is optional:
you can enter a User ID manually. No separate `ef_ble` installation or running
parent integration is required.

This version prepares 0.8.0b3 for public distribution:

- Adds root and installed license notices, attribution, credits, and a separate disclaimer.
- Compares all 40 vendored library files with upstream v1.1.1, commit
  `ef02d81a2720de256548a5d515af814cc3244ee9`: 34 files remain byte-identical,
  and the six modified files carry prominent modification notices.
- Adds caution notices to the README, installation instructions, and Home Assistant
  setup forms in English and Ukrainian. The integration is labeled Unofficial Beta.
- Updates the version to 0.8.0b5 and supplies metadata for this repository.
- Adds a dedicated `suris_ef_ble_xboost.zip` HACS asset with `manifest.json`
  and all integration files directly at the archive root.
- This is a packaging-only update; integration runtime behavior remains unchanged.
- Preserves BLE, authentication and command logic, entity inventory and identifiers,
  and the turquoise appearance of 0.8.0b3.

**The author has tested the integration on a real EcoFlow DELTA 2 Max station.**
This does not establish coverage of every feature, firmware, or configuration.
Additional automated publication checks passed 20 tests using mocked BLE and cloud
calls on Home Assistant 2026.9.1 / Python 3.14.6. Those automated checks did not
exercise real hardware or a live cloud login. The release remains an unstable beta.

The code defines up to 66 sensors; **not all are necessarily enabled in an
installed integration**. Extra Battery 1 sensors appear after battery detection.

**Before installation, use caution:** back up Home Assistant and keep the previous build.
**During operation, use caution:** verify commands directly on the station and supervise
initial testing. **Car Input 2 is experimental.** Avoid critical loads.
See the [full disclaimer](https://github.com/Suris2009/suris-ef-ble/blob/main/DISCLAIMER.md).

**Thank you to [rabits](https://github.com/rabits), [GnoX](https://github.com/GnoX),
and all creators and contributors of [EcoFlow BLE](https://github.com/rabits/ha-ef-ble)!**
This project builds on their protocol implementation and device support.
Acknowledgment does not imply their endorsement of Suris modifications.

HACS uses the dedicated `suris_ef_ble_xboost.zip` asset. The full source,
license, audit, and verification package is `suris_ef_ble_0.8.0b5.zip`.
Installation instructions are in the
[README](https://github.com/Suris2009/suris-ef-ble#installation-and-update).

**Unofficial / unstable beta. Use with caution and at your own risk.**
