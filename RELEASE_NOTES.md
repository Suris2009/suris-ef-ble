# Suris EcoFlow BLE 0.8.1b3 — 100% local BLE / No internet required · UNOFFICIAL BETA

This is a local test build pending a physical DELTA 2 Max beeper test.

> [!CAUTION]
> **UNOFFICIAL, UNSTABLE BETA. USE WITH CAUTION AND AT YOUR OWN RISK.**
> No warranties are provided. To the maximum extent permitted by law, authors
> and contributors accept no liability for its use or consequences.

This project is developed exclusively for the author's own Home Assistant
installation and EcoFlow equipment. It is published as-is for transparency and
reference, without any promise of support or compatibility with other installations.

## Changes since 0.8.1b2

- Added a **Sound** switch for the DELTA 2 Max beeper. Its state comes from
  the PD heartbeat quiet-mode value; the command sends the corresponding PD
  quiet-mode packet over the existing authenticated BLE connection.
- The existing sensors, switches, controls, BLE connection, and entity IDs are
  preserved. This is a beta pending a physical on/off test on DELTA 2 Max.

## Testing status

In an isolated Python 3.14.7 environment with the pinned Home Assistant
dependencies, **36 tests passed**. The new regression test checks the switch
state, packet bytes, and disconnected behavior. This does not establish that
the station accepts the command. The release workflow also validates JSON,
Python syntax, installed license notices, and the HACS archive layout.

The author previously tested the retained BLE recovery behavior on an
**EcoFlow DELTA 2 Max running firmware V1.0.0.204**. After approximately 20 hours
powered off, the station connected within 1–2 seconds after power-on without a
manual integration reload, and all sensors worked. The new numeric fields have
not yet been checked on a phone connected to a live Home Assistant installation.

## Installation assets

- HACS: `suris_ef_ble_xboost.zip`
- Full source, license, audit, and verification package: `suris_ef_ble_0.8.1b3.zip`

Back up Home Assistant and keep version 0.8.0 available for rollback. Close the
EcoFlow app while testing because the station supports only one active BLE client.

**Thank you to [rabits](https://github.com/rabits), [GnoX](https://github.com/GnoX),
and every creator and contributor of [EcoFlow BLE / ha-ef-ble](https://github.com/rabits/ha-ef-ble).**
Their protocol implementation and device support make this project possible.
Acknowledgment does not imply endorsement of Suris modifications.

**Unofficial integration. Use with caution and at your own risk.**
