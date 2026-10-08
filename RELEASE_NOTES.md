# Suris EcoFlow BLE 0.8.2b1 — 100% local BLE / No internet required · UNOFFICIAL BETA

Compatibility beta based on stable 0.8.1 for Home Assistant 2026.10.
Stable 0.8.1 remains available; this release does not replace the stable channel.

> [!CAUTION]
> **UNOFFICIAL INTEGRATION. USE WITH CAUTION AND AT YOUR OWN RISK.**
> No warranties are provided. To the maximum extent permitted by law, authors
> and contributors accept no liability for its use or consequences.

This project is developed exclusively for the author's own Home Assistant
installation and EcoFlow equipment. It is published as-is for transparency and
reference, without any promise of support or compatibility with other installations.

## Changes since 0.8.1

- Accept `protobuf>=6.30,<8` instead of `protobuf~=6.30`, resolving the
  dependency conflict with protobuf 7.36.0 in Home Assistant 2026.10.0.
- Retain compatibility with Home Assistant 2026.9.4 and protobuf 6.33.6.
- Keep the BLE implementation, sensors, controls, settings and entity IDs from 0.8.1.
- Publish a pre-release with the existing HACS archive layout and installed notices.

## Testing status

All **36 automated tests passed** in each isolated Python 3.14.8 environment:

- Home Assistant 2026.10.0 with protobuf 7.36.0.
- Home Assistant 2026.9.4 with protobuf 6.33.6.

Tests cover HA loading, setup, entity registration, recovery, cleanup, authentication
flow and control packet generation. BLE transport and cloud login are mocked;
physical-station testing of this beta is pending. The release workflow validates
JSON, Python syntax, installed notices and the HACS archive layout.

The author previously tested the retained BLE recovery behavior on an
**EcoFlow DELTA 2 Max running firmware V1.0.0.204**. After approximately 20 hours
powered off, the station connected within 1–2 seconds after power-on without a
manual integration reload, and all sensors worked. The new numeric fields have
not yet been checked on a phone connected to a live Home Assistant installation.

## Installation assets

- HACS: `suris_ef_ble_xboost.zip`
- Full source, license, audit, and verification package: `suris_ef_ble_0.8.2b1.zip`

In HACS enable beta versions and select **v0.8.2b1**, then restart Home Assistant.
Back up Home Assistant and keep version 0.8.1 available for rollback. Close the
EcoFlow app while testing because the station supports only one active BLE client.

**Thank you to [rabits](https://github.com/rabits), [GnoX](https://github.com/GnoX),
and every creator and contributor of [EcoFlow BLE / ha-ef-ble](https://github.com/rabits/ha-ef-ble).**
Their protocol implementation and device support make this project possible.
Acknowledgment does not imply endorsement of Suris modifications.

**Unofficial integration. Use with caution and at your own risk.**
