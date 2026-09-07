# Suris EcoFlow BLE 0.8.0b6 — 100% local BLE / No internet required · UNOFFICIAL / UNSTABLE BETA

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

This build makes two changes to BLE connection recovery:

- While the entry is in `SETUP_RETRY`, a new connectable advertisement matching
  its serial number and address requests one early retry through Home Assistant.
  The listener survives failed setup and does not replay old cached advertisements.
  Repeated advertisements do not cause repeated reloads. A new disappearance and
  reappearance, reported by Home Assistant Bluetooth, permits another early retry.
  Loaded, disabled, authenticating, unloading, and failed-authentication entries
  are not restarted by the listener. It stops with Home Assistant.
- If BLE connection fails before platform setup starts, cleanup skips platform
  unloading. This prevents misleading `Config entry was never loaded!` errors
  while retaining connection and runtime cleanup.

Home Assistant retains responsibility for ordinary retries and connection teardown.
The change uses its existing scanner, with no polling timer or active scan request.
It requires the adapter or proxy to receive advertisements from the station.
XT60 controls, authentication, device commands, sensor behavior, entity identifiers,
translations, appearance, and the vendored protocol library are unchanged.

**Verification: 34 tests passed on Home Assistant 2026.9.1 / Python 3.14.6.**
The 20 existing tests and 14 recovery cases cover cached versus fresh discovery,
duplicate advertisements, entry-state guards, a second outage, shutdown, and setup
cleanup. Recovery cases use real HA Bluetooth and entry APIs with synthetic radio
events and simulated connections. The new changes have not been tested on a real
station; no live cloud login was performed. Earlier physical testing reported by
the author does not validate this build's new behavior. Results are included in
`audit/tests_0.8.0b6.txt` and `audit/checks_0.8.0b6.json`.

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
license, audit, and verification package is `suris_ef_ble_0.8.0b6.zip`.
Installation instructions are in the
[README](https://github.com/Suris2009/suris-ef-ble#installation-and-update).

**Unofficial / unstable beta. Use with caution and at your own risk.**
