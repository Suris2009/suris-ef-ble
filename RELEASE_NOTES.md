# Suris EcoFlow BLE 0.8.1b2 — 100% local BLE / No internet required · UNOFFICIAL BETA

> [!CAUTION]
> **UNOFFICIAL, UNSTABLE BETA. USE WITH CAUTION AND AT YOUR OWN RISK.**
> No warranties are provided. To the maximum extent permitted by law, authors
> and contributors accept no liability for its use or consequences.

This project is developed exclusively for the author's own Home Assistant
installation and EcoFlow equipment. It is published as-is for transparency and
reference, without any promise of support or compatibility with other installations.

## Changes since 0.8.1b1

- Replaced sliders with numeric entry fields for **AC Charging Speed**,
  **Max Charge Limit**, and **Min Discharge Limit** to make precise entry easier
  on phones.
- **Energy Backup Level** retains its existing display mode and behavior.
- AC charging power remains **200–2400 W** in **100 W steps**. Values outside
  that range or between steps are rejected. No automatic rounding or limit
  changes were added.
- Existing entity names and unique IDs, BLE connection and recovery behavior,
  sensors, switches, and XT60 selectors are preserved.

## Testing status

The release workflow validates JSON, Python syntax, installed license notices,
and the HACS archive layout. The existing AC control regression test has been
updated to expect numeric entry. The full regression suite has not been rerun
for this display-only change; the 35-test results in `audit/tests_0.8.1b1.txt`
are historical results from 0.8.1b1.

The author previously tested the retained BLE recovery behavior on an
**EcoFlow DELTA 2 Max running firmware V1.0.0.204**. After approximately 20 hours
powered off, the station connected within 1–2 seconds after power-on without a
manual integration reload, and all sensors worked. The new numeric fields have
not yet been checked on a phone connected to a live Home Assistant installation.

## Installation assets

- HACS: `suris_ef_ble_xboost.zip`
- Full source, license, audit, and verification package: `suris_ef_ble_0.8.1b2.zip`

Back up Home Assistant and keep version 0.8.0 available for rollback. Close the
EcoFlow app while testing because the station supports only one active BLE client.

**Thank you to [rabits](https://github.com/rabits), [GnoX](https://github.com/GnoX),
and every creator and contributor of [EcoFlow BLE / ha-ef-ble](https://github.com/rabits/ha-ef-ble).**
Their protocol implementation and device support make this project possible.
Acknowledgment does not imply endorsement of Suris modifications.

**Unofficial integration. Use with caution and at your own risk.**
