> ИСТОРИЧЕСКИЙ АУДИТ ИЗ ВХОДНОГО АРХИВА. Не подтверждает испытания 0.8.0b4 на оборудовании. Текущий статус: неофициальная нестабильная бета.

# Аудит до сборки

Источники: загруженные ef_ble 1.1.1 и Suris 0.8.0a6; найденная Suris 0.7.5. Точный архив 0.7.4 не найден. Таблица получена из исходников, не из предполагаемого количества.

| Функция/entity | ef_ble 1.1.1 | Suris 0.7.x (0.7.5) | текущая 0.8.0a6 | итог (требование реализации) |
|---|---|---|---|---|
| sensor.battery_level | battery() | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.battery_level_main | battery() | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.input_power | power(precision=0) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.output_power | power(precision=0) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.remaining_time_charging | duration(enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.remaining_time_discharging | duration(enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.battery_voltage | port_voltage('Battery', state_attribute_fields=['max_cell_voltage', 'min_cell_voltage']) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.ac_input_power | power(precision=2) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.ac_input_voltage | voltage(precision=1, enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.ac_input_current | current(precision=2, enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.ac_output_power | power(precision=2) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.ac_output_voltage | voltage(precision=2, enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.ac_output_current | current(precision=2, enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.dc_output_power | power(precision=2) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.usba_output_power | power() | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.usba2_output_power | power() | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.usbc_output_power | power() | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.usbc2_output_power | power() | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.qc_usb1_output_power | power() | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.qc_usb2_output_power | power() | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.cell_temperature | temperature(enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.max_cell_voltage | voltage(precision=3, enabled=False, entity_category=EntityCategory.DIAGNOSTIC) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.min_cell_voltage | voltage(precision=3, enabled=False, entity_category=EntityCategory.DIAGNOSTIC) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.dc12v_output_voltage | voltage(precision=2, enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.dc12v_output_current | current(precision=2, enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.dc_input_voltage | voltage(precision=2, enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.dc_input_current | current(precision=2, enabled=False) | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.xt60_1_input_power | power() | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.xt60_2_input_power | power() | От родителя | Только standalone, сохраняет disabled default | Самостоятельно, enabled |
| sensor.battery_1_battery_level | battery(translation_key='battery_level') | От родителя | Одноразовая проверка списка батарей | BMS heartbeat → отдельное устройство, enabled |
| sensor.battery_1_cell_temperature | temperature(translation_key='cell_temperature') | От родителя | Одноразовая проверка списка батарей | BMS heartbeat → отдельное устройство, enabled |
| sensor.battery_1_voltage | port_voltage('Battery', state_attribute_fields=['battery_{n}_max_cell_voltage', 'battery_{n}_min_cell_voltage']) | От родителя | Одноразовая проверка списка батарей | BMS heartbeat → отдельное устройство, enabled |
| sensor.battery_1_max_cell_voltage | voltage(precision=3, enabled=False, entity_category=EntityCategory.DIAGNOSTIC, translation_key='max_cell_voltage') | От родителя | Одноразовая проверка списка батарей | BMS heartbeat → отдельное устройство, enabled |
| sensor.battery_1_min_cell_voltage | voltage(precision=3, enabled=False, entity_category=EntityCategory.DIAGNOSTIC, translation_key='min_cell_voltage') | От родителя | Одноразовая проверка списка батарей | BMS heartbeat → отдельное устройство, enabled |
| usb_ports (enable_usb_ports) | Да | От родителя | Только standalone | Сохранить upstream метод и пакет |
| dc_12v_port (enable_dc_12v_port) | Да | От родителя | Только standalone | Сохранить upstream метод и пакет |
| ac_ports (enable_ac_ports) | Да | От родителя | Только standalone | Сохранить upstream метод и пакет |
| battery_charge_limit_max (set_battery_charge_limit_max) | Да | От родителя | Только standalone | Сохранить upstream метод и пакет |
| battery_charge_limit_min (set_battery_charge_limit_min) | Да | От родителя | Только standalone | Сохранить upstream метод и пакет |
| energy_backup (enable_energy_backup) | Да | От родителя | Только standalone | Сохранить upstream метод и пакет |
| energy_backup_battery_level (set_energy_backup_battery_level) | Да | От родителя | Только standalone | Сохранить upstream метод и пакет |
| ac_charging_speed (set_ac_charging_speed) | Да | От родителя | Только standalone | Сохранить upstream метод и пакет |
| inverter_out_temperature | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| inverter_dc_in_temperature | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| slave_1_power_difference | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| power_difference | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| xt60_2_voltage | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| mppt_1_temperature | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| mppt_2_temperature | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| fan_speed_level | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| main_battery_cycles | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| slave_1_cycles | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| xboost | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| car_input_1_current | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| car_input_2_current | Нет | Да | Да; чужой device identifier | Сохранить unique_id, перенести в своё устройство |
| EB1 input/output watts и остальные BMS-поля | Декодер есть; не все HA entities | Нет отдельных input/output entities в найденной 0.7.5 | Нет | Добавить; неизвестные масштабы подписать raw |
| upstream select/button/binary_sensor/climate для D2M | Нет применимых сущностей | — | — | Не создавать чужие controls |
| Авторизация | Собственный flow | Через родителя | Автовыбор единственного ef_ble; Store/cache; нет BLE-проверки перед create | Явный login/User ID и BLE-проверка |
| BLE backend внутри ZIP | Да | Нет | Пустой _vendor; runtime-copy установленного ef_ble | Полный vendored backend |

## Первопричины

1. config_flow.async_step_user создаёт entry сразу при одном загруженном родителе; _async_load_stored_user_id читает чужой Store. manual сохраняет ID без проверки BLE.
2. 0.7.x unique_id = parent entry ID; a6 поздно меняет его на MAC. Все custom device_info используют (ef_ble, address); vendored HA wrapper также сохраняет ef_ble и Bluetooth connection.
3. Upstream _get_extra_battery_entities вызывается единожды; explicit extra_battery=[] блокирует создание; battery_1_enabled зависит от kit_info, а не от BMS heartbeat.
4. В parent mode alpha вообще не добавляет upstream платформы. В standalone состав зависит от скопированной чужой интеграции.
5. Alpha не заменяет enabled_default у upstream descriptions и не мигрирует disabled_by.
