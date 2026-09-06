# Third-party notices

**Suris EcoFlow BLE: 100% local BLE operation. No internet or EcoFlow cloud connection is required during operation.**

## Bundled code

The only third-party source subtree bundled in this distribution is
`custom_components/suris_ef_ble_xboost/_vendor/eflib/`: 40 Python files from
[rabits/ha-ef-ble v1.1.1](https://github.com/rabits/ha-ef-ble/tree/ef02d81a2720de256548a5d515af814cc3244ee9/custom_components/ef_ble/eflib),
Apache-2.0. See LICENSE, NOTICE, and UPSTREAM_NOTICE.md. No upstream author notices
have been removed. Suris wrappers use this library and its entity/control data;
Suris additions and adaptations use Apache-2.0 too.

## Dependencies installed separately

These libraries are referenced, not vendored into this ZIP. Their independent
licenses continue to apply. The versions below identify the isolated test
environment, not a change to the integration's existing requirement ranges.
License labels were read from installed distribution metadata on 2026-09-06.

| Distribution | Inspected version | Declared license | Source |
| --- | --- | --- | --- |
| ecdsa | 0.19.2 | MIT | [python-ecdsa](https://github.com/tlsfuzzer/python-ecdsa) |
| pycryptodome | 3.23.0 | BSD and Public Domain | [PyCryptodome](https://github.com/Legrandin/pycryptodome) |
| protobuf | 6.33.6 | BSD-3-Clause | [Protocol Buffers](https://github.com/protocolbuffers/protobuf) |
| bleak | 3.0.2 | MIT | [Bleak](https://github.com/hbldh/bleak) |
| bleak-retry-connector | 4.7.0 | MIT | [bleak-retry-connector](https://github.com/bluetooth-devices/bleak-retry-connector) |
| homeassistant | 2026.9.1 | Apache-2.0 | [Home Assistant Core](https://github.com/home-assistant/core) |
| aiohttp | 3.14.3 | Apache-2.0 AND MIT | [aiohttp](https://github.com/aio-libs/aiohttp) |
| voluptuous | 0.16.0 | BSD-3-Clause | [Voluptuous](https://github.com/alecthomas/voluptuous) |

This is an inventory of the directly used packages, not a complete SBOM for an
entire Home Assistant installation. Redistributing these dependencies separately
requires preserving their own license texts and notices.

## Branding and other rights

The four supplied PNG files in `brand/` identify the Suris project and are
retained from the submitted 0.8.0b3 archive. No font files, EcoFlow application
packages, firmware images, product photographs, or manuals are bundled.
No independent chain-of-title evidence for the supplied raster artwork was
available; visual inspection alone is not a legal clearance of artwork or fonts.

EcoFlow and DELTA identify the compatible hardware; Bluetooth and Home Assistant
identify the technologies used. All third-party marks remain with their owners.
Apache-2.0 does not grant trademark rights. No EcoFlow approval is claimed.

The inherited `keydata.py` protocol table is byte-identical to upstream v1.1.1.
It is not a secret taken from the user's station. Its presence in an open-source
repository alone does not establish the rights to any underlying third-party
material or resolve reverse-engineering, service-term, or patent questions.
