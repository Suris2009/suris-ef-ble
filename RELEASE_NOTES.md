# Suris EcoFlow BLE 0.8.1b1 — 100% local BLE / No internet required · UNOFFICIAL BETA

> [!CAUTION]
> **UNOFFICIAL, UNSTABLE BETA. USE WITH CAUTION AND AT YOUR OWN RISK.**
> No warranties are provided. To the maximum extent permitted by law, authors
> and contributors accept no liability for its use or consequences.

This project is developed exclusively for the author's own Home Assistant
installation and EcoFlow equipment. It is published as-is for transparency and
reference, without any promise of support or compatibility with other installations.

## Changes since 0.8.0

- Added an **AC Charging** switch for pausing and resuming grid charging without
  changing the configured charging power.
- Changed **AC Charging Speed** to a slider with a fixed **200–2400 W** range and
  **100 W** steps, matching the EcoFlow app for the author's DELTA 2 Max.
- Values below 200 W and values between the 100 W steps are rejected. There is no
  option to unlock lower values.
- Retained the BLE recovery behavior introduced in 0.8.0b6 and released in 0.8.0.
- Kept existing sensor entity IDs, XT60 selectors, and Extra Battery 1 behavior.

The AC charging pause command is a focused backport from
[EcoFlow BLE / ha-ef-ble 1.1.2](https://github.com/rabits/ha-ef-ble/releases/tag/v1.1.2),
implemented upstream in [PR #475](https://github.com/rabits/ha-ef-ble/pull/475)
by [GnoX](https://github.com/GnoX). The bundled dependency closure otherwise
remains based on the audited ha-ef-ble 1.1.1 source.

## Testing status

The author previously tested the retained BLE recovery behavior on an
**EcoFlow DELTA 2 Max running firmware V1.0.0.204**. After approximately 20 hours
powered off, the station connected within 1–2 seconds after power-on without a
manual integration reload, and all sensors worked.

The new AC charging controls have automated protocol and entity tests but have
not yet been physically verified on the station. Verify the selected value and
charging state directly on the DELTA 2 Max during the first test.

Automated verification details are included in `audit/tests_0.8.1b1.txt` and
`audit/checks_0.8.1b1.json`: **35 tests passed** on Home Assistant Core 2026.9.1
and Python 3.14.7.

## Installation assets

- HACS: `suris_ef_ble_xboost.zip`
- Full source, license, audit, and verification package: `suris_ef_ble_0.8.1b1.zip`

Back up Home Assistant and keep version 0.8.0 available for rollback. Close the
EcoFlow app while testing because the station supports only one active BLE client.

**Thank you to [rabits](https://github.com/rabits), [GnoX](https://github.com/GnoX),
and every creator and contributor of [EcoFlow BLE / ha-ef-ble](https://github.com/rabits/ha-ef-ble).**
Their protocol implementation and device support make this project possible.
Acknowledgment does not imply endorsement of Suris modifications.

**Unofficial integration. Use with caution and at your own risk.**
