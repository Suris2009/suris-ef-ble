# SPDX-License-Identifier: Apache-2.0
# Derived from rabits/ha-ef-ble v1.1.1; upstream authorship is retained.
# Modified by Suris contributors; notice updated 2026-09-06.
# Changes: Restrict imports to DELTA 2 Max; retain device-first import order.
# Release 0.8.0b4 adds this notice only; executable code is unchanged.
"""EcoFlow BLE 1.1.1. Suris modification: import only the D2M backend."""

# Preserve upstream's device-first import order (props has a DeviceBase back-reference).
from .devices.delta2_max import Device as Device
