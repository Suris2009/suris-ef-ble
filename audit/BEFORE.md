> HISTORICAL OFFLINE AUDIT FROM THE INPUT ARCHIVE. This records earlier development checks. See README.md for current author-reported hardware testing and sensor availability. Current status: unofficial, unstable beta.

# Pre-build audit

Sources: uploaded ef_ble 1.1.1 and Suris 0.8.0a6; recovered Suris 0.7.5. The exact 0.7.4 archive was not found. The table was derived from source code rather than an assumed entity count.

| Feature/entity | ef_ble 1.1.1 | Suris 0.7.x (0.7.5) | current 0.8.0a6 | target implementation requirement |
|---|---|---|---|---|
| sensor.battery_level | battery() | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.battery_level_main | battery() | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.input_power | power(precision=0) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.output_power | power(precision=0) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.remaining_time_charging | duration(enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.remaining_time_discharging | duration(enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.battery_voltage | port_voltage('Battery', state_attribute_fields=['max_cell_voltage', 'min_cell_voltage']) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.ac_input_power | power(precision=2) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.ac_input_voltage | voltage(precision=1, enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.ac_input_current | current(precision=2, enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.ac_output_power | power(precision=2) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.ac_output_voltage | voltage(precision=2, enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.ac_output_current | current(precision=2, enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.dc_output_power | power(precision=2) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.usba_output_power | power() | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.usba2_output_power | power() | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.usbc_output_power | power() | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.usbc2_output_power | power() | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.qc_usb1_output_power | power() | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.qc_usb2_output_power | power() | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.cell_temperature | temperature(enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.max_cell_voltage | voltage(precision=3, enabled=False, entity_category=EntityCategory.DIAGNOSTIC) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.min_cell_voltage | voltage(precision=3, enabled=False, entity_category=EntityCategory.DIAGNOSTIC) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.dc12v_output_voltage | voltage(precision=2, enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.dc12v_output_current | current(precision=2, enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.dc_input_voltage | voltage(precision=2, enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.dc_input_current | current(precision=2, enabled=False) | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.xt60_1_input_power | power() | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.xt60_2_input_power | power() | From parent | Standalone only; retains disabled default | Independent; enabled default |
| sensor.battery_1_battery_level | battery(translation_key='battery_level') | From parent | One-time battery-list check | BMS heartbeat → separate device; enabled default |
| sensor.battery_1_cell_temperature | temperature(translation_key='cell_temperature') | From parent | One-time battery-list check | BMS heartbeat → separate device; enabled default |
| sensor.battery_1_voltage | port_voltage('Battery', state_attribute_fields=['battery_{n}_max_cell_voltage', 'battery_{n}_min_cell_voltage']) | From parent | One-time battery-list check | BMS heartbeat → separate device; enabled default |
| sensor.battery_1_max_cell_voltage | voltage(precision=3, enabled=False, entity_category=EntityCategory.DIAGNOSTIC, translation_key='max_cell_voltage') | From parent | One-time battery-list check | BMS heartbeat → separate device; enabled default |
| sensor.battery_1_min_cell_voltage | voltage(precision=3, enabled=False, entity_category=EntityCategory.DIAGNOSTIC, translation_key='min_cell_voltage') | From parent | One-time battery-list check | BMS heartbeat → separate device; enabled default |
| usb_ports (enable_usb_ports) | Yes | From parent | Standalone only | Preserve upstream method and packet |
| dc_12v_port (enable_dc_12v_port) | Yes | From parent | Standalone only | Preserve upstream method and packet |
| ac_ports (enable_ac_ports) | Yes | From parent | Standalone only | Preserve upstream method and packet |
| battery_charge_limit_max (set_battery_charge_limit_max) | Yes | From parent | Standalone only | Preserve upstream method and packet |
| battery_charge_limit_min (set_battery_charge_limit_min) | Yes | From parent | Standalone only | Preserve upstream method and packet |
| energy_backup (enable_energy_backup) | Yes | From parent | Standalone only | Preserve upstream method and packet |
| energy_backup_battery_level (set_energy_backup_battery_level) | Yes | From parent | Standalone only | Preserve upstream method and packet |
| ac_charging_speed (set_ac_charging_speed) | Yes | From parent | Standalone only | Preserve upstream method and packet |
| inverter_out_temperature | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| inverter_dc_in_temperature | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| slave_1_power_difference | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| power_difference | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| xt60_2_voltage | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| mppt_1_temperature | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| mppt_2_temperature | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| fan_speed_level | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| main_battery_cycles | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| slave_1_cycles | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| xboost | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| car_input_1_current | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| car_input_2_current | No | Yes | Yes; another integration's device identifier | Preserve unique_id; move to an owned device |
| EB1 input/output watts and remaining BMS fields | Decoder exists; incomplete HA entity coverage | No separate input/output entities in the recovered 0.7.5 | No | Add; label unknown scales as raw |
| Upstream select/button/binary_sensor/climate for D2M | No applicable entities | — | — | Do not add controls for other models |
| Authentication | Own configuration flow | Through parent | Automatically selects the only ef_ble entry; Store/cache; no BLE verification before creation | Explicit login/User ID choice and BLE verification |
| BLE backend inside ZIP | Yes | No | Empty _vendor; runtime copy of installed ef_ble | Complete vendored backend |

## Root causes

1. config_flow.async_step_user creates an entry immediately when only one parent is loaded; _async_load_stored_user_id reads another integration's Store. Manual entry saves the ID without BLE verification.
2. In 0.7.x, unique_id is the parent entry ID; a6 changes it to the MAC late. All custom device_info values use (ef_ble, address); the vendored HA wrapper also retains ef_ble and a Bluetooth connection.
3. Upstream _get_extra_battery_entities is called only once; explicit extra_battery=[] blocks creation; battery_1_enabled depends on kit_info rather than a BMS heartbeat.
4. In parent mode, the alpha does not add upstream platforms. In standalone mode, the inventory depends on the copied external integration.
5. The alpha does not override enabled_default in upstream descriptions and does not migrate disabled_by.
