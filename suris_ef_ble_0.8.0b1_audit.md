> HISTORICAL OFFLINE AUDIT FROM THE INPUT ARCHIVE. This records earlier development checks. See README.md for current author-reported hardware testing and sensor availability. Current status: unofficial, unstable beta.

# Suris EcoFlow BLE 0.8.0b1 — historical audit and results

Date: September 6, 2026. Result: a standalone ZIP defining 48 DELTA 2 Max entities and 29 Extra Battery 1 sensors. The code supplies enabled defaults for its 66 sensors; actual enabled state in an existing installation can differ. Core 2026.8+; offline checks used Home Assistant 2026.9.1 / Python 3.14.6.

**This historical report records the offline build prepared before its initial hardware trial. Live EcoFlow sign-in, BLE authentication, and station operation were mocked in that review environment. The author has since reported testing the integration on a real station; see the current README.**

The uploaded ef_ble 1.1.1 and Suris 0.8.0a6 were compared with the recovered Suris 0.7.5. The exact 0.7.4 archive was not found; statements about 0.7.x refer to the 0.7.5 source. Version 0.7.5 contains 10 custom sensors, X-Boost, and two Car Input selectors. Standard platforms in that version were provided by the parent ef_ble integration.

Changelog: bundled backend 1.1.1; explicit login/User ID choice with mandatory BLE verification; corrected device identity, duplicates, disabled-sensor migration, and dynamic EB1 creation; preserved commands and the Car Input lock; corrected task and subscription cleanup.

## Root causes and fixes

| Observed issue | Cause in 0.8.0a6 | Change in 0.8.0b1 |
|---|---|---|
| Does not ask for User ID | `async_step_user` immediately created an entry when one parent was loaded; `_async_load_stored_user_id` read another integration's Store; manual ID entry was not verified over BLE | Discovery → login/User ID choice → BLE verification → own entry creation; old parent-backed entries require reauthentication |
| Shows the ef_ble device and a repeated Add prompt | Old unique IDs used the parent entry ID or changed to the MAC late; custom device_info used `(ef_ble, address)` and shared connections | The configuration unique ID is the serial number; serial and MAC are checked; Suris owns its identifiers; connections are empty; duplicate discovery returns already_configured |
| Extra Battery device exists without sensors | One-time `_get_extra_battery_entities` call, empty `extra_battery=[]`, and a dependency on kit_info during early initialization | Raw listener is installed before connection; an EB1 BMS heartbeat creates its entities; later detection does not require a reload |
| Incomplete platform inventory | In parent mode, Suris did not create upstream entities; standalone mode depended on a runtime copy of installed ef_ble; the archive's `_vendor` was empty | The ZIP includes the 40 required protocol files; platforms use the complete D2M inventory |
| Some sensors are disabled | Upstream disabled defaults were copied; disabled_by was not migrated | Enabled/visible defaults; a one-time migration clears disabled_by and hidden_by in old owned entries; later user choices are preserved |

## Complete feature comparison

The original audit table was prepared before the build (`audit/BEFORE.md`). The following table records implementation coverage. From parent does not mean an independent implementation in Suris 0.7.5. Enabled entries below describe implementation defaults or the offline fixture, not a guarantee of enabled entities in every installed system.

| Feature/entity | ef_ble 1.1.1 | Suris 0.7.x (0.7.5) | current 0.8.0a6 | resulting 0.8.0b1 |
|---|---|---|---|---|
| sensor.`battery_level` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`battery_level_main` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`input_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`output_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`remaining_time_charging` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`remaining_time_discharging` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`battery_voltage` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`ac_input_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`ac_input_voltage` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`ac_input_current` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`ac_output_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`ac_output_voltage` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`ac_output_current` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`dc_output_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`usba_output_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`usba2_output_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`usbc_output_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`usbc2_output_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`qc_usb1_output_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`qc_usb2_output_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`cell_temperature` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`max_cell_voltage` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`min_cell_voltage` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`dc12v_output_voltage` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`dc12v_output_current` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`dc_input_voltage` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`dc_input_current` | Yes; disabled default | From parent | Standalone only | Present; enabled default |
| sensor.`xt60_1_input_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`xt60_2_input_power` | Yes | From parent | Standalone only | Present; enabled default |
| sensor.`inverter_out_temperature` | No | Yes | Yes; another integration's device identifier | Preserved; own device; enabled default |
| sensor.`inverter_dc_in_temperature` | No | Yes | Yes; another integration's device identifier | Preserved; own device; enabled default |
| sensor.`power_difference` | No | Yes | Yes; another integration's device identifier | Preserved; own device; enabled default |
| sensor.`xt60_2_voltage` | No | Yes | Yes; another integration's device identifier | Preserved; own device; enabled default |
| sensor.`mppt_1_temperature` | No | Yes | Yes; another integration's device identifier | Preserved; own device; enabled default |
| sensor.`mppt_2_temperature` | No | Yes | Yes; another integration's device identifier | Preserved; own device; enabled default |
| sensor.`fan_speed_level` | No | Yes | Yes; another integration's device identifier | Preserved; own device; enabled default |
| sensor.`main_battery_cycles` | No | Yes | Yes; another integration's device identifier | Preserved; own device; enabled default |
| sensor.`battery_1_num` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_type` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_cell_id` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_err_code` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_sys_ver` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_soc` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_voltage` | Yes | From parent | Early battery-list check only | Present; EB1; enabled default |
| sensor.`battery_1_amp` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_temp` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_open_bms_idx` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_design_cap` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_remain_cap` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_full_cap` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`slave_1_cycles` | No | Yes | Yes; on the main device entry | Present; EB1; enabled default |
| sensor.`battery_1_soh` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_max_cell_voltage` | Yes | From parent | Early battery-list check only | Present; EB1; enabled default |
| sensor.`battery_1_min_cell_voltage` | Yes | From parent | Early battery-list check only | Present; EB1; enabled default |
| sensor.`battery_1_cell_temperature` | Yes | From parent | Early battery-list check only | Present; EB1; enabled default |
| sensor.`battery_1_min_cell_temp` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_max_mos_temp` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_min_mos_temp` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_bms_fault` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_bq_sys_stat_reg` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_tag_chg_amp` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_battery_level` | Yes | From parent | Early battery-list check only | Present; EB1; enabled default |
| sensor.`battery_1_input_power` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_output_power` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`battery_1_remain_time` | Decoded field; no separate entity | No separate entity | No separate entity | Present; EB1; enabled default |
| sensor.`slave_1_power_difference` | No | Yes | Yes; on the main device entry | Present; EB1; enabled default |
| switch.`ac_ports` | Yes | From parent | Standalone only | Original command method preserved |
| switch.`dc_12v_port` | Yes | From parent | Standalone only | Original command method preserved |
| switch.`usb_ports` | Yes | From parent | Standalone only | Original command method preserved |
| switch.`energy_backup` | Yes | From parent | Standalone only | Original command method preserved |
| switch.`xboost` | No | Yes | Yes | Packet preserved; own backend |
| number.`battery_charge_limit_max` | Yes | From parent | Standalone only | Original method and dynamic limits preserved |
| number.`battery_charge_limit_min` | Yes | From parent | Standalone only | Original method and dynamic limits preserved |
| number.`energy_backup_battery_level` | Yes | From parent | Standalone only | Original method and dynamic limits preserved |
| number.`ac_charging_speed` | Yes | From parent | Standalone only | Original method and dynamic limits preserved |
| select.`car_input_1_current` | No | Yes | Yes | 4/6/8 A; original packet; shared lock |
| select.`car_input_2_current` | No | Yes | Yes | 4/6/8 A; original packet; shared lock; experimental |
| Other upstream select / binary_sensor / button / climate entities for D2M | None applicable | No | No | Other models not added |

Coverage includes all 29 standard main-station sensors, five standard EB1 sensors, four switches, and four number controls for D2M. All 13 extra Suris 0.7.5 entities were preserved. Another 22 BMS fields previously absent from HA were exposed as sensors. The 28 BMS fields plus calculated power difference yield 29 EB1 sensors.

## DELTA 2 Max inventory

Names below are display-name suffixes and stable keys. Home Assistant assigns actual entity IDs according to its existing registry and user renames.

| № | Sensor key | Name | Unit | Source |
|---:|---|---|---|---|
| 1 | `battery_level` | Battery Level | % | `ef_ble 1.1.1: battery_level` |
| 2 | `battery_level_main` | Main Battery Level | % | `ef_ble 1.1.1: battery_level_main` |
| 3 | `input_power` | Input Power | W | `ef_ble 1.1.1: input_power` |
| 4 | `output_power` | Output Power | W | `ef_ble 1.1.1: output_power` |
| 5 | `remaining_time_charging` | Charge Time Remaining | min | `ef_ble 1.1.1: remaining_time_charging` |
| 6 | `remaining_time_discharging` | Discharge Time Remaining | min | `ef_ble 1.1.1: remaining_time_discharging` |
| 7 | `battery_voltage` | Battery Voltage | V | `ef_ble 1.1.1: battery_voltage` |
| 8 | `ac_input_power` | AC Input Power | W | `ef_ble 1.1.1: ac_input_power` |
| 9 | `ac_input_voltage` | AC Input Voltage | V | `ef_ble 1.1.1: ac_input_voltage` |
| 10 | `ac_input_current` | AC Input Current | A | `ef_ble 1.1.1: ac_input_current` |
| 11 | `ac_output_power` | AC Output Power | W | `ef_ble 1.1.1: ac_output_power` |
| 12 | `ac_output_voltage` | AC Output Voltage | V | `ef_ble 1.1.1: ac_output_voltage` |
| 13 | `ac_output_current` | AC Output Current | A | `ef_ble 1.1.1: ac_output_current` |
| 14 | `dc_output_power` | DC Output Power | W | `ef_ble 1.1.1: dc_output_power` |
| 15 | `usba_output_power` | USB A (1) Output Power | W | `ef_ble 1.1.1: usba_output_power` |
| 16 | `usba2_output_power` | USB A (2) Output Power | W | `ef_ble 1.1.1: usba2_output_power` |
| 17 | `usbc_output_power` | USB C (1) Output Power | W | `ef_ble 1.1.1: usbc_output_power` |
| 18 | `usbc2_output_power` | USB C (2) Output Power | W | `ef_ble 1.1.1: usbc2_output_power` |
| 19 | `qc_usb1_output_power` | USB A QC (1) Output Power | W | `ef_ble 1.1.1: qc_usb1_output_power` |
| 20 | `qc_usb2_output_power` | USB A QC (2) Output Power | W | `ef_ble 1.1.1: qc_usb2_output_power` |
| 21 | `cell_temperature` | Cell Temperature | °C | `ef_ble 1.1.1: cell_temperature` |
| 22 | `max_cell_voltage` | Max Cell Voltage | V | `ef_ble 1.1.1: max_cell_voltage` |
| 23 | `min_cell_voltage` | Min Cell Voltage | V | `ef_ble 1.1.1: min_cell_voltage` |
| 24 | `dc12v_output_voltage` | DC 12V Output Voltage | V | `ef_ble 1.1.1: dc12v_output_voltage` |
| 25 | `dc12v_output_current` | DC 12V Output Current | A | `ef_ble 1.1.1: dc12v_output_current` |
| 26 | `dc_input_voltage` | DC Input Voltage | V | `ef_ble 1.1.1: dc_input_voltage` |
| 27 | `dc_input_current` | DC Input Current | A | `ef_ble 1.1.1: dc_input_current` |
| 28 | `xt60_1_input_power` | XT60 (1) Input Power | W | `ef_ble 1.1.1: xt60_1_input_power` |
| 29 | `xt60_2_input_power` | XT60 (2) Input Power | W | `ef_ble 1.1.1: xt60_2_input_power` |
| 30 | `inverter_out_temperature` | Inverter Out Temperature | °C | `DirectInvDeltaHeartbeatPack.out_temp` |
| 31 | `inverter_dc_in_temperature` | Inverter DC In Temperature | °C | `DirectInvDeltaHeartbeatPack.dc_in_temp` |
| 32 | `power_difference` | BLE Power Difference | W | `Mr350PdHeartbeatDelta2Max.difference` |
| 33 | `xt60_2_voltage` | XT60 (2) Voltage | V | `Mr350MpptHeart.pv2_in_vol` |
| 34 | `mppt_1_temperature` | MPPT Temperature 1 | °C | `Mr350MpptHeart.mppt_temp` |
| 35 | `mppt_2_temperature` | MPPT Temperature 2 | °C | `Mr350MpptHeart.pv2_mppt_temp` |
| 36 | `fan_speed_level` | Fan Speed Level | — | `DirectInvDeltaHeartbeatPack.fan_state` |
| 37 | `main_battery_cycles` | Main Battery Cycles | cycles | `_BmsHeartbeatBatteryMain.cycles` |

| Platform | Key | Name | Values / limits |
|---|---|---|---|
| switch | `ac_ports` | AC Ports | on/off |
| switch | `dc_12v_port` | DC 12V Port | on/off |
| switch | `usb_ports` | USB Ports | on/off |
| switch | `energy_backup` | Backup Reserve | on/off |
| switch | `xboost` | X-Boost | on/off |
| number | `battery_charge_limit_max` | Max Charge Limit | Current Min Discharge Limit…100 % |
| number | `battery_charge_limit_min` | Min Discharge Limit | 0…current Max Charge Limit, % |
| number | `energy_backup_battery_level` | Energy Backup Level | Between current min/max limits, %; available with Backup Reserve |
| number | `ac_charging_speed` | AC Charging Speed | 1…max_ac_charging_power, W; original 1800 W fallback |
| select | `car_input_1_current` | Car Input 1 Current | 4 A / 6 A / 8 A |
| select | `car_input_2_current` | Car Input 2 Current | 4 A / 6 A / 8 A; experimental |

## Separate Extra Battery 1 inventory

| № | Sensor key | Name | Unit | BMS field |
|---:|---|---|---|---|
| 1 | `battery_1_num` | BMS Number (raw) | — | `num` |
| 2 | `battery_1_type` | BMS Type (raw) | — | `type_` |
| 3 | `battery_1_cell_id` | Cell ID (raw) | — | `cell_id` |
| 4 | `battery_1_err_code` | BMS Error Code (raw) | — | `err_code` |
| 5 | `battery_1_sys_ver` | BMS Firmware Version (raw) | — | `sys_ver` |
| 6 | `battery_1_soc` | BMS SOC | % | `soc` |
| 7 | `battery_1_voltage` | Battery Voltage | V | `vol` |
| 8 | `battery_1_amp` | BMS Current (raw) | — | `amp` |
| 9 | `battery_1_temp` | BMS Temperature | °C | `temp` |
| 10 | `battery_1_open_bms_idx` | Open BMS Index (raw) | — | `open_bms_idx` |
| 11 | `battery_1_design_cap` | Design Capacity (raw) | — | `design_cap` |
| 12 | `battery_1_remain_cap` | Remaining Capacity (raw) | — | `remain_cap` |
| 13 | `battery_1_full_cap` | Full Capacity (raw) | — | `full_cap` |
| 14 | `slave_1_cycles` | Slave 1 Cycles | cycles | `cycles` |
| 15 | `battery_1_soh` | BMS SOH | % | `soh` |
| 16 | `battery_1_max_cell_voltage` | Max Cell Voltage | V | `max_cell_vol` |
| 17 | `battery_1_min_cell_voltage` | Min Cell Voltage | V | `min_cell_vol` |
| 18 | `battery_1_cell_temperature` | Cell Temperature | °C | `max_cell_temp` |
| 19 | `battery_1_min_cell_temp` | Min Cell Temperature | °C | `min_cell_temp` |
| 20 | `battery_1_max_mos_temp` | Max MOS Temperature | °C | `max_mos_temp` |
| 21 | `battery_1_min_mos_temp` | Min MOS Temperature | °C | `min_mos_temp` |
| 22 | `battery_1_bms_fault` | BMS Fault (raw) | — | `bms_fault` |
| 23 | `battery_1_bq_sys_stat_reg` | BQ System Status (raw) | — | `bq_sys_stat_reg` |
| 24 | `battery_1_tag_chg_amp` | Target Charge Current (raw) | — | `tag_chg_amp` |
| 25 | `battery_1_battery_level` | Battery Level | % | `f32_show_soc` |
| 26 | `battery_1_input_power` | Input Power | W | `input_watts` |
| 27 | `battery_1_output_power` | Output Power | W | `output_watts` |
| 28 | `battery_1_remain_time` | BMS Remaining Time (raw) | — | `remain_time` |
| 29 | `slave_1_power_difference` | BLE Slave 1 Power Difference | W | `difference` |

`(raw)` means the exact value returned by the original decoder. No sign, scale, or unit was invented for current, capacities, time, or codes. These fields have visible and enabled defaults; their actual state in an installation can differ. The meaning of individual raw registers still needs confirmation. Temperature and percentage fields follow the corresponding named BMS fields; their scaling on real firmware was not verified by this offline review.

Both Power Difference entities preserve the working 0.7.5 formula: **Output minus Input**. A positive value means output power exceeds input power. In the original backend, `battery_level` is the aggregate system level and `battery_level_main` is the main battery level. Serial-number and kit_info fields populate device metadata; Extra Battery 2 is not created.

## Authentication, identity, and migration

New setup always offers login or manual User ID entry. Either path creates an entry only after the authenticated BLE state is reached; a failed probe releases the BLE session. Cloud login uses the upstream asynchronous client and AUTO region selection. Only the serial number, BLE address, User ID, own BLE-verification flag, and EB1 bookkeeping are saved. Email and password are retained neither in the entry nor in flow attributes.

Migration transfers only the old Suris entry's own address, serial number, User ID, and battery bookkeeping. A parent-backed entry containing ef_ble_entry_id is not treated as an independently verified ID source and requires reauthentication. An existing independent ID is preserved and checked on connection. If only an old parent ID is available, the serial number is recovered from owned Suris entity unique IDs, followed by BLE discovery; the other integration's entry is not read.

| Entry | Identifier |
|---|---|
| Config entry Suris | Unique ID = DELTA 2 Max serial number |
| Main device | `(suris_ef_ble_xboost, SN)`; empty connections |
| Extra Battery 1 | `(suris_ef_ble_xboost, SN + ":battery_1")`; empty connections |
| Battery link to the main station | Main device entry's `via_device_id` |
| Upstream entities inside Suris | `ef_{SN}_{key}` — previous unique_id preserved; platform = Suris |
| Custom Suris entities | `suris_ef_ble_{key}_{SN}` — previous unique_id preserved |

The ef_ prefix in an old unique_id does not create an ef_ble dependency: HA distinguishes entity-registry records by integration platform. Migration preserves entity_id and, where possible, the owned device_id, moves Slave 1 sensors to EB1, and removes only owned EB2 or empty old devices. Other integrations' ef_ble entries are not edited. The extra battery uses the current `via_device_id`, replacing the previous `via_device` in the [Device Registry API](https://developers.home-assistant.io/blog/2026/08/24/device-registry-follow-up-changes/).

Suris duplicates are merged by serial number or normalized MAC. The duplicate is unloaded first, its owned entities are moved to the primary entry, and then the duplicate entry is removed. The canonical entry prefers its own User ID; duplicate detection is repeated after the BLE await. Pending discovery cards are removed after successful setup.

For old Suris entries, a one-time migration clears disabled_by/hidden_by for sensors, including those previously disabled manually, as explicitly requested during development. Subsequent user disabling is preserved after migration. No diagnostic category is assigned. See [HA rules for disabled entities](https://developers.home-assistant.io/docs/entity_registry_disabled_by/).

## BLE and lifecycle

Each setup/retry creates an owned backend instance. Reconnection uses Home Assistant's retry/reload mechanism; the backend's independent reconnect loop is disabled to prevent competing loops. Connection loss schedules one reload; missing advertisements or timeouts produce ConfigEntryNotReady, and authentication errors produce ConfigEntryAuthFailed. Connection verification is limited to 60 seconds and two backend attempts.

The raw listener is installed before BLE authentication so early BMS data is not lost. A late EB1 BMS packet adds 29 sensors once per setup. Detection is recorded in the owned entry: after reload, a known battery and its entities remain in the registry but are unavailable until a fresh heartbeat. A kit_info packet indicating absence marks EB1 unavailable without deleting its history.

Notifications from another thread are directed to the HA event loop with call_soon_threadsafe; state publication waits until parsing finishes. Unload closes listener/timer subscriptions, cancels and awaits backend tasks, releases BLE, and clears runtime_data. If HA cannot unload platforms, the running runtime is retained. Setup failure and probe cancellation also clean up. No custom synchronous file or network loading is performed in the event loop; cryptography remains the upstream implementation.

Car Input uses a shared asynchronous lock and the original paired 0x47 packet. Both values are cleared when the connection generation changes. Writes are blocked until fresh valid 4/6/8 A values are available for both inputs, because the command sends both limits. Decoding the second limit from the first four bytes of `res` is preserved from Suris 0.7.5. This does not prove physical Car Input 2 behavior.

## Scope of protocol changes

The ZIP contains 40 Python files forming the D2M transitive dependencies from the uploaded ef_ble 1.1.1; 34 are byte-identical. Only six files were changed:

| File within `_vendor/eflib` | Change |
|---|---|
| `__init__.py` | Import only D2M while preserving the required Device import order |
| `devices/__init__.py` | Remove automatic imports of other models |
| `connection.py` | Await task cancellation; track unnamed timers for cleanup |
| `devicebase.py` | Guard access to byte 22 in short BLE advertisements |
| `devices/_delta2_base.py` | Process only the first kit in the battery list |
| `listeners.py` | Idempotent unsubscribe; iterate a listener-list snapshot |

AST comparison of class methods in devicebase.py, _delta2_base.py, and delta2_max.py found 74 identical methods; only `_ScanRecordV2.from_manufacturer_data` and `Delta2Base._update_extra_batteries` differ. Original control methods, parser dispatch, encryption/framing, and authentication logic are preserved. X-Boost and Car Input packets retain their addresses, command IDs, versions, and payload layouts. No unknown raw, reset, or firmware commands were added or sent.

The ZIP includes the Apache-2.0 LICENSE, UPSTREAM_NOTICE.md, per-file SHA-256 hashes, and a full diff of modified vendored files. The protocol source was the uploaded 1.1.1 archive rather than the current GitHub branch. During this earlier build, the license was supplemented from the [upstream repository](https://github.com/rabits/ha-ef-ble/blob/main/LICENSE) because its input component ZIP lacked it; original notices were retained. The later 0.8.0b3 input already included that license, as recorded in LICENSE_REVIEW.md.

## Verification performed

| Level | Result | Practical limit |
|---|---|---|
| Static checks and compilation | 52 Python files compiled; manifest/translation JSON parsed; all 29/29 + 5/5 upstream sensors and 28/28 BMS fields covered; no absolute imports of external ef_ble | Does not prove physical station behavior |
| Real HA classes with mocked BLE/cloud | 20 pytest checks passed on Core 2026.9.1 | Synthetic BLE packets; login networking mocked |
| HA platforms and registries | Real EntityPlatform registered 48 station entities, then 77 after BMS; all enabled/visible in the test fixture; 29 assigned to EB1; no EB2 | HA APIs ran in a test process; this was not a complete cold start of the user's HA system |
| Real HA loader/config-flow manager | Loads custom manifest/config_flow; user → authentication choice → manual ID → create entry; repeated Bluetooth discovery → already_configured | BLE transport and successful authentication were mocked in this test |
| Lifecycle/migration | Setup/unload/failure/cancellation; early/late BMS; cross-thread callbacks; task/timer cleanup; migration, reauthentication, duplicate merging, and previous entity IDs | Radio interference, actual station unavailability, and recovery after a full HA restart require hardware testing |
| Commands | Diff preserves original upstream methods; lock and stale Car Input protection checked with mocked send | This review did not repeat physical tests of previously confirmed commands; Car Input 2 was not confirmed |

The pytest log records five DeprecationWarning messages from the installed Home Assistant HTTP server and third-party backoff. The tests found no deprecated-API warnings caused by Suris; this does not guarantee the absence of future warnings. Current registry APIs use `config_entry_id` and `via_device_id`; HA versions before 2026.8 are not supported by this build. See [Device Registry changes](https://developers.home-assistant.io/blog/2026/07/21/device-registry-single-config-entry/).

Full log: `audit/tests_2026.9.1.txt`. Source of the 20 checks: `verification/test_integration.py`. To repeat them outside a working HA installation, create a separate Python 3.14 environment, install `verification/requirements-tested.txt`, and run `PYTHONPATH=. python -m pytest -q verification/test_integration.py --tb=short` from the extracted ZIP root. Tests require no real credentials.

## Historical installation and initial hardware-test plan

For an update preserving entity IDs, completely replace `/config/custom_components/suris_ef_ble_xboost` with the ZIP folder and restart HA while retaining the Suris configuration entry. An old entry without its own ID prompts for reauthentication. Manual .storage editing is unnecessary. Use the current README for current installation instructions.

The following was the requested clean independent-registration test plan for this earlier build:

1. Remove old ef_ble and Suris configuration entries through Settings → Devices & services. Remove `/config/custom_components/ef_ble`. Install the new Suris folder from the ZIP and restart HA. This clean test removes old entries; the update method preserving entries is described above.
2. Close the EcoFlow app. Add Suris, select the discovered DELTA 2 Max, and choose EcoFlow sign-in or manual User ID entry. Confirm that the choice is displayed.
3. Enter credentials and wait for BLE verification; setup should finish only after success. Confirm that Suris connects without ef_ble installed.
4. Check the 48 defined station entities. After a BMS heartbeat, check for a separate Extra Battery 1 device with 29 sensors linked to the main station. The original clean-test target was 66 enabled sensors; existing installations can contain disabled entities. Fields awaiting their heartbeat may temporarily be unavailable, which is distinct from disabled.

**That concluded the original initial-test plan.** It did not require repeating previously confirmed AC Ports, DC 12V, USB, X-Boost, Backup Reserve, or number-control tests, or using Car Input 2 in the first trial. Long-term stability, real disconnect/reconnect, and cold starts with the station absent had not been established by that offline review. The current README separately records the author's later report of real-station testing.

## Archive contents

`custom_components/suris_ef_ble_xboost/` is the installed component, including `_vendor/eflib`, README, LICENSE, and UPSTREAM_NOTICE. `verification/` contains reproducible checks. `audit/` contains the initial and final inventories, SHA-256 hashes, protocol diff, static checks, and pytest log. Extra folders do not need to be copied into HA.

External ef_ble is not required for imports, credentials, or startup. Home Assistant Bluetooth and the standard Python dependencies in the manifest are still required. The login path contacts the EcoFlow API only during sign-in; manual User ID entry and subsequent operation use BLE.
