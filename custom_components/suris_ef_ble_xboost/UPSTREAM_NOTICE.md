# Upstream attribution and local modifications

**Suris EcoFlow BLE: 100% local BLE operation. No internet or EcoFlow cloud connection is required during operation.**

Suris EcoFlow BLE 0.8.0b4 is an **unofficial, unstable beta**. It bundles the
DELTA 2 Max dependency closure of [EcoFlow BLE / ha-ef-ble](https://github.com/rabits/ha-ef-ble)
by **rabits and the ha-ef-ble contributors**, under Apache-2.0.
Special thanks to **GnoX**, credited in the upstream v1.1.1 release.

## Verified source

- Upstream release: [v1.1.1](https://github.com/rabits/ha-ef-ble/releases/tag/v1.1.1).
- Immutable commit: `ef02d81a2720de256548a5d515af814cc3244ee9`.
- Original upstream path: `custom_components/ef_ble/eflib/`.
- Local path: `custom_components/suris_ef_ble_xboost/_vendor/eflib/`.
- Verification date: 2026-09-06. All 40 files were compared against that tag.
- 34 files remain byte-identical; six contain the modifications listed below.
- The inherited LICENSE matches the LICENSE at that exact commit byte for byte.
- No standalone NOTICE file was found in that upstream source tree.

The incoming Suris archive records an earlier source archive,
`ef_ble_1.1.1(1).zip`, SHA-256
`d9b609d7f136946cf5e93f946fe327831abd0dd9a9a55f0c91cac12cc3f56716`.
Its recorded upstream file hashes were independently confirmed against v1.1.1.
The earlier component archive itself was not needed for this comparison.

## Modified upstream files

| File within `_vendor/eflib` | Modification |
| --- | --- |
| `__init__.py` | Restrict imports to DELTA 2 Max; retain device-first import order. |
| `devices/__init__.py` | Remove automatic imports of unrelated device models. |
| `connection.py` | Await cancelled connection tasks and track unnamed timers during teardown. |
| `devicebase.py` | Check advertisement length before accessing byte 22. |
| `devices/_delta2_base.py` | Restrict extra-battery kit metadata to slot 1. |
| `listeners.py` | Make unsubscribe idempotent and iterate over a listener snapshot. |

Release 0.8.0b4 adds prominent file-header notices to these six files without
changing their executable code. Each unchanged file retains its original bytes.
The protocol key table, encryption, authentication, packet framing, and device
commands have not been replaced or presented as original Suris inventions.

The repository/release root includes per-file hashes in
`audit/vendored_sources.json` and a complete patch against the immutable upstream
commit in `audit/protocol_changes.diff`. Suris wrapper additions and adaptations
are licensed under Apache-2.0; see NOTICE. Licenses and attribution documents are
also inside the integration folder so manual installation retains them.

This provenance check establishes correspondence with the published upstream
source. It does not certify the origin of every upstream protocol constant,
grant EcoFlow trademark rights, or settle third-party patent/contract claims.
