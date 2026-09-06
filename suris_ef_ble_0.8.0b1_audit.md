> ИСТОРИЧЕСКИЙ АУДИТ ИЗ ВХОДНОГО АРХИВА. Не подтверждает испытания 0.8.0b4 на оборудовании. Текущий статус: неофициальная нестабильная бета.

# Suris EcoFlow BLE 0.8.0b1 — аудит и результат

Дата: 6 сентября 2026. Итог: автономный ZIP, 48 сущностей DELTA 2 Max + 29 датчиков Extra Battery 1. Все 66 датчиков включены по умолчанию. Core 2026.8+; offline-проверки — Home Assistant 2026.9.1 / Python 3.14.6.

**Это проверенная offline сборка для первого аппаратного запуска. Живой вход в EcoFlow, BLE-аутентификация и работа на твоей станции в этой среде не выполнялись.**

Сравнены загруженные ef_ble 1.1.1 и Suris 0.8.0a6, а также найденная Suris 0.7.5. Точный архив 0.7.4 не найден; выводы о 0.7.x относятся к исходникам 0.7.5. Исходники 0.7.5 содержат 10 custom sensors, X-Boost и два Car Input select. Штатные платформы в этой версии обслуживал родительский ef_ble.

Короткий changelog: встроен backend 1.1.1; введён явный login/User ID с обязательной BLE-проверкой; исправлены идентичность устройств, дубли, миграция отключённых датчиков и динамическое создание EB1; сохранены команды и Car Input lock; исправлена очистка задач и подписок.

## Первопричины и исправления

| Наблюдаемая ошибка | Причина в 0.8.0a6 | Изменение в 0.8.0b1 |
|---|---|---|
| Не спрашивает User ID | `async_step_user` сразу создавал entry при единственном загруженном родителе; `_async_load_stored_user_id` читал чужой Store; ручной ID не проверялся по BLE | Discovery → выбор login/User ID → BLE-проверка → создание собственного entry; старый parent-backed entry требует reauth |
| Показывает устройство ef_ble и повторное «Добавить» | Старые unique ID были ID родительского entry либо поздно менялись на MAC; custom device_info использовал `(ef_ble, address)` и общие connections | Unique ID настройки равен SN; проверяются SN и MAC; собственные identifiers Suris; connections пустые; дубль discovery завершается already_configured |
| Устройство EB есть, датчиков нет | Одноразовый вызов `_get_extra_battery_entities`, пустой `extra_battery=[]`, зависимость от kit_info при ранней инициализации | Raw listener установлен до подключения; BMS heartbeat EB1 создаёт сразу все её сущности; позднее появление не требует reload |
| Неполный набор платформ | В parent mode upstream-сущности не создавались Suris; standalone зависел от runtime-копии установленного ef_ble; `_vendor` архива был пуст | Нужные 40 файлов протокола находятся внутри ZIP; платформы создаются из полного перечня D2M |
| Часть датчиков disabled | Копировались disabled defaults upstream; миграции disabled_by не было | Все датчики enabled/visible; одноразовая миграция старых собственных записей очищает disabled_by и hidden_by |

## Полный diff функций

Таблица исходного аудита была составлена до сборки (`audit/BEFORE.md` в ZIP). Ниже — фактическое покрытие итоговой реализации. «От родителя» не означает автономную реализацию в Suris 0.7.5.

| Функция/entity | ef_ble 1.1.1 | Suris 0.7.x (0.7.5) | текущая 0.8.0a6 | итог 0.8.0b1 |
|---|---|---|---|---|
| sensor.`battery_level` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`battery_level_main` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`input_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`output_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`remaining_time_charging` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`remaining_time_discharging` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`battery_voltage` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`ac_input_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`ac_input_voltage` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`ac_input_current` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`ac_output_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`ac_output_voltage` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`ac_output_current` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`dc_output_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`usba_output_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`usba2_output_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`usbc_output_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`usbc2_output_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`qc_usb1_output_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`qc_usb2_output_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`cell_temperature` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`max_cell_voltage` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`min_cell_voltage` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`dc12v_output_voltage` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`dc12v_output_current` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`dc_input_voltage` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`dc_input_current` | Да; disabled default | От родителя | Только standalone | Есть, enabled |
| sensor.`xt60_1_input_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`xt60_2_input_power` | Да | От родителя | Только standalone | Есть, enabled |
| sensor.`inverter_out_temperature` | Нет | Да | Да, чужой device identifier | Сохранён, собственное устройство, enabled |
| sensor.`inverter_dc_in_temperature` | Нет | Да | Да, чужой device identifier | Сохранён, собственное устройство, enabled |
| sensor.`power_difference` | Нет | Да | Да, чужой device identifier | Сохранён, собственное устройство, enabled |
| sensor.`xt60_2_voltage` | Нет | Да | Да, чужой device identifier | Сохранён, собственное устройство, enabled |
| sensor.`mppt_1_temperature` | Нет | Да | Да, чужой device identifier | Сохранён, собственное устройство, enabled |
| sensor.`mppt_2_temperature` | Нет | Да | Да, чужой device identifier | Сохранён, собственное устройство, enabled |
| sensor.`fan_speed_level` | Нет | Да | Да, чужой device identifier | Сохранён, собственное устройство, enabled |
| sensor.`main_battery_cycles` | Нет | Да | Да, чужой device identifier | Сохранён, собственное устройство, enabled |
| sensor.`battery_1_num` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_type` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_cell_id` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_err_code` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_sys_ver` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_soc` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_voltage` | Да | От родителя | Только ранняя проверка списка EB | Есть, EB1, enabled |
| sensor.`battery_1_amp` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_temp` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_open_bms_idx` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_design_cap` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_remain_cap` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_full_cap` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`slave_1_cycles` | Нет | Да | Да, на основной записи устройства | Есть, EB1, enabled |
| sensor.`battery_1_soh` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_max_cell_voltage` | Да | От родителя | Только ранняя проверка списка EB | Есть, EB1, enabled |
| sensor.`battery_1_min_cell_voltage` | Да | От родителя | Только ранняя проверка списка EB | Есть, EB1, enabled |
| sensor.`battery_1_cell_temperature` | Да | От родителя | Только ранняя проверка списка EB | Есть, EB1, enabled |
| sensor.`battery_1_min_cell_temp` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_max_mos_temp` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_min_mos_temp` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_bms_fault` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_bq_sys_stat_reg` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_tag_chg_amp` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_battery_level` | Да | От родителя | Только ранняя проверка списка EB | Есть, EB1, enabled |
| sensor.`battery_1_input_power` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_output_power` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`battery_1_remain_time` | Поле декодера; отдельной entity нет | Нет отдельной entity | Нет отдельной entity | Есть, EB1, enabled |
| sensor.`slave_1_power_difference` | Нет | Да | Да, на основной записи устройства | Есть, EB1, enabled |
| switch.`ac_ports` | Да | От родителя | Только standalone | Исходный метод команды сохранён |
| switch.`dc_12v_port` | Да | От родителя | Только standalone | Исходный метод команды сохранён |
| switch.`usb_ports` | Да | От родителя | Только standalone | Исходный метод команды сохранён |
| switch.`energy_backup` | Да | От родителя | Только standalone | Исходный метод команды сохранён |
| switch.`xboost` | Нет | Да | Да | Пакет сохранён; свой backend |
| number.`battery_charge_limit_max` | Да | От родителя | Только standalone | Исходный метод и динамические пределы сохранены |
| number.`battery_charge_limit_min` | Да | От родителя | Только standalone | Исходный метод и динамические пределы сохранены |
| number.`energy_backup_battery_level` | Да | От родителя | Только standalone | Исходный метод и динамические пределы сохранены |
| number.`ac_charging_speed` | Да | От родителя | Только standalone | Исходный метод и динамические пределы сохранены |
| select.`car_input_1_current` | Нет | Да | Да | 4/6/8 A, исходный пакет, общий lock |
| select.`car_input_2_current` | Нет | Да | Да | 4/6/8 A, исходный пакет, общий lock; экспериментальный |
| Другие upstream select / binary_sensor / button / climate для D2M | Нет применимых | Нет | Нет | Чужие модели не добавлены |

Итого покрыты все 29 штатных датчиков основной станции, 5 штатных датчиков EB1, 4 switches и 4 numbers D2M. Все 13 дополнительных сущностей Suris 0.7.5 сохранены. Дополнительно 22 ранее не выставленных в HA поля BMS получили собственные датчики. 28 полей BMS + расчёт разницы мощности дают 29 датчиков EB1.

## Перечень DELTA 2 Max

Имена ниже — суффиксы отображаемых имён и стабильные ключи. Фактические entity_id назначает Home Assistant с учётом уже существующего реестра и пользовательских переименований.

| № | Ключ sensor | Имя | Единица | Источник |
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

| Платформа | Ключ | Имя | Значения / пределы |
|---|---|---|---|
| switch | `ac_ports` | AC Ports | on/off |
| switch | `dc_12v_port` | DC 12V Port | on/off |
| switch | `usb_ports` | USB Ports | on/off |
| switch | `energy_backup` | Backup Reserve | on/off |
| switch | `xboost` | X-Boost | on/off |
| number | `battery_charge_limit_max` | Max Charge Limit | Текущий Min Discharge Limit…100 % |
| number | `battery_charge_limit_min` | Min Discharge Limit | 0…текущий Max Charge Limit, % |
| number | `energy_backup_battery_level` | Energy Backup Level | Между текущими min/max лимитами, %; доступен при Backup Reserve |
| number | `ac_charging_speed` | AC Charging Speed | 1…max_ac_charging_power, W; исходный fallback 1800 W |
| select | `car_input_1_current` | Car Input 1 Current | 4 A / 6 A / 8 A |
| select | `car_input_2_current` | Car Input 2 Current | 4 A / 6 A / 8 A; экспериментальный |

## Отдельный перечень Extra Battery 1

| № | Ключ sensor | Имя | Единица | Поле BMS |
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

`(raw)` означает ровно значение, выданное исходным декодером. Для тока, ёмкостей, времени и кодов не придуманы знак, масштаб или единица. Эти поля видимы и включены; смысл отдельных raw-регистров ещё требует подтверждения. Температурные и процентные поля используют семантику соответствующих именованных BMS-полей; масштаб на реальной прошивке здесь не проверен.

Для обеих сущностей Power Difference сохранена формула рабочей 0.7.5: **Output − Input**. Положительное значение означает превышение выходной мощности над входной. `battery_level` — агрегированный уровень системы, `battery_level_main` — основной батареи, согласно исходному backend. Поля serial number и kit_info используются в метаданных устройства; Extra Battery 2 не создаётся.

## Авторизация, идентичность и миграция

Новая настройка всегда предлагает login либо ручной User ID. В обоих случаях entry создаётся только после authenticated BLE-состояния; неудачный probe освобождает BLE-сеанс. Cloud login использует async-клиент upstream и определение региона AUTO. Сохраняются только SN, BLE address, User ID, признак собственного BLE-подтверждения и служебное состояние EB1. Email/пароль не сохраняются ни в entry, ни в атрибутах flow.

Миграция старого Suris entry переносит только собственные адрес/SN/User ID и служебное состояние батареи. Parent-backed запись со ссылкой ef_ble_entry_id не считается источником собственного подтверждённого ID и вызывает reauth. Старый самостоятельный ID сохраняется и проверяется при подключении. Если доступен только старый ID родителя, SN восстанавливается из unique_id собственных Suris entities, затем ищется BLE-объявление; чужой entry не читается.

| Запись | Идентификатор |
|---|---|
| Config entry Suris | Unique ID = серийный номер DELTA 2 Max |
| Основное устройство | `(suris_ef_ble_xboost, SN)`; connections пустые |
| Extra Battery 1 | `(suris_ef_ble_xboost, SN + ":battery_1")`; connections пустые |
| Связь батареи с основной станцией | `via_device_id` основной записи устройства |
| Upstream-сущности внутри Suris | `ef_{SN}_{key}` — прежний unique_id сохранён; platform = Suris |
| Custom Suris-сущности | `suris_ef_ble_{key}_{SN}` — прежний unique_id сохранён |

Префикс ef_ в старом unique_id не создаёт зависимости от ef_ble: HA различает entity registry по платформе интеграции. Миграция сохраняет entity_id и по возможности собственный device_id, переносит Slave 1 sensors на EB1, удаляет только собственные EB2/опустевшие старые устройства. Чужие записи ef_ble не редактируются. Связь дополнительной физической батареи использует современный `via_device_id`, заменяющий прежний `via_device` в актуальном API [Device Registry](https://developers.home-assistant.io/blog/2026/08/24/device-registry-follow-up-changes/).

Дубли Suris объединяются по SN или нормализованному MAC. Сначала выгружается дубликат, его собственные entities перемещаются в основную запись, затем удаляется дублирующий entry. Каноническая запись предпочитает собственный User ID; повторная проверка дубликата выполняется после BLE await. Pending discovery карточки убираются после успешного setup.

В старых Suris записях одноразово снимаются disabled_by/hidden_by у всех sensors, включая вручную отключённые ранее — согласно явному требованию задания. После миграции последующие пользовательские отключения сохраняются. Категория diagnostic не назначается. [Правила HA для disabled entities](https://developers.home-assistant.io/docs/entity_registry_disabled_by/).

## BLE и lifecycle

При каждом setup/retry создаётся собственный экземпляр backend. Повторные подключения обслуживает механизм retry/reload Home Assistant: встроенный независимый reconnect backend отключён, чтобы не было двух конкурирующих циклов. Потеря соединения планирует один reload; отсутствие объявления или таймаут возвращает ConfigEntryNotReady, ошибка авторизации — ConfigEntryAuthFailed. Проверка подключения ограничена 60 секундами и двумя попытками backend.

Raw listener подключён до BLE-auth, поэтому ранний BMS не теряется. Поздний BMS EB1 добавляет 29 датчиков один раз за setup. Факт обнаружения сохраняется в собственном entry: после reload уже известная батарея и её entities остаются в реестре, но unavailable до свежего heartbeat. Пакет kit_info с признаком отсутствия отключает доступность EB1, а не удаляет её историю.

Уведомления направляются в loop HA через call_soon_threadsafe при вызове из другого потока; публикация состояния откладывается до завершения парсинга. Unload закрывает listener/timer subscriptions, отменяет и дожидается backend tasks, освобождает BLE, обнуляет runtime_data. Если HA не может выгрузить платформы, действующий runtime сохраняется. Setup failure и отмена probe проходят очистку. Собственная синхронная файловая/сетевая загрузка в event loop отсутствует; криптография остаётся реализацией исходного backend.

Car Input использует общий async lock и исходный парный пакет 0x47. После смены поколения соединения оба значения очищаются. До получения свежих допустимых 4/6/8 A для обоих входов запись запрещена: команда отправляет оба лимита. Расшифровка второго лимита из первых четырёх байтов `res` сохранена из Suris 0.7.5. Физическая работа Car Input 2 этим не доказана.

## Границы изменений протокола

Встроены 40 Python-файлов транзитивных зависимостей D2M из загруженного ef_ble 1.1.1; 34 побайтово совпадают. Изменены только шесть файлов:

| Файл внутри `_vendor/eflib` | Изменение |
|---|---|
| `__init__.py` | Импорт только D2M с сохранением нужного порядка импорта Device |
| `devices/__init__.py` | Убран автоматический импорт остальных моделей |
| `connection.py` | Ожидание отмены задач; учёт безымянных таймеров для очистки |
| `devicebase.py` | Защита доступа к байту 22 короткого BLE advertisement |
| `devices/_delta2_base.py` | Обработка только первого kit в списке батарей |
| `listeners.py` | Идемпотентная отписка; обход снимка списка listeners |

AST-diff методов классов в devicebase.py, _delta2_base.py и delta2_max.py: 74 методов полностью совпадают; отличаются только `_ScanRecordV2.from_manufacturer_data` и `Delta2Base._update_extra_batteries`. Все исходные методы управления, parser dispatch, encryption/framing и auth-логика сохранены. Пакеты X-Boost и Car Input сохраняют прежние адреса, command ID, версию и структуру payload. Сырые неизвестные команды, reset и firmware-команды не добавлялись и не отправлялись.

В ZIP присутствуют Apache-2.0 LICENSE, UPSTREAM_NOTICE.md, per-file SHA-256 и полный diff изменённых vendored файлов. Источник протокола — загруженный архив 1.1.1, не текущая ветка GitHub. Лицензия дополнена из [репозитория upstream](https://github.com/rabits/ha-ef-ble/blob/main/LICENSE), поскольку в исходном component ZIP её не было; исходные notices сохранены.

## Что проверено

| Уровень | Результат | Практический предел |
|---|---|---|
| Статика и compile | 52 Python-файла скомпилированы; JSON manifest/переводов читаются; 29/29 + 5/5 upstream sensors и 28/28 BMS-полей покрыты; абсолютных импортов внешнего ef_ble нет | Не доказывает поведение физической станции |
| Реальные классы HA, mock BLE/cloud | 20 pytest-проверок на Core 2026.9.1 прошли | BLE-пакеты синтетические, сеть login заменена mock |
| Платформы и реестры HA | Реальный EntityPlatform зарегистрировал 48 entities станции, затем 77 после BMS; все enabled/visible; 29 привязаны к EB1; EB2 отсутствует | Это запуск API HA в тестовом процессе, не полный холодный старт пользовательского HA |
| Реальный loader/config flow manager HA | Загрузка custom manifest/config_flow; user → выбор auth → manual ID → create entry; повторный bluetooth discovery → already_configured | Передача BLE и успешный auth в этом тесте подменены |
| Lifecycle/migration | Setup/unload/failure/cancellation; ранний/поздний BMS; callbacks из другого потока; очистка задач/таймеров; миграция, reauth, duplicate merge и прежние entity_id | Радиопомехи, реальная недоступность станции и восстановление после полного restart HA требуют аппаратного запуска |
| Команды | Исходные upstream методы сохранены по diff; lock/защита stale Car Input проверены с mock send | Физические повторные тесты уже подтверждённых команд не выполнялись; Car Input 2 не подтверждён |

В логе pytest пять DeprecationWarning из установленного Home Assistant HTTP server и стороннего backoff. В тестах предупреждений об устаревшем API, вызванных Suris, не выявлено; это не обещание отсутствия любых будущих предупреждений. Использованы актуальные registry APIs с `config_entry_id` и `via_device_id`; старые версии HA до 2026.8 не поддерживаются этой сборкой. [Изменения Device Registry](https://developers.home-assistant.io/blog/2026/07/21/device-registry-single-config-entry/).

Полный лог — `audit/tests_2026.9.1.txt`. Исходники 20 проверок — `verification/test_integration.py`. Для повторения вне рабочего HA создай отдельное окружение Python 3.14, установи `verification/requirements-tested.txt` и из корня распакованного ZIP выполни `PYTHONPATH=. python -m pytest -q verification/test_integration.py --tb=short`. Реальные credentials тестам не нужны.

## Установка и только первый аппаратный тест

Для обновления с сохранением entity_id полностью замени папку `/config/custom_components/suris_ef_ble_xboost` папкой из ZIP и перезапусти HA, сохранив Suris config entry. Если старая запись не имеет собственного ID, интерфейс попросит reauth. Ручное редактирование .storage не требуется.

Для запрошенной проверки чистой автономной регистрации:

1. Удали старые config entries ef_ble и Suris через «Настройки → Устройства и службы». Удали `/config/custom_components/ef_ble`. Установи новую папку Suris из ZIP и перезапусти HA. При чистом тесте старые записи удаляются; вариант обновления с сохранением записей описан выше.
2. Закрой EcoFlow app. Добавь Suris, выбери обнаруженную DELTA 2 Max, затем «Войти в EcoFlow» или «У меня есть User ID». Проверь, что этот выбор действительно показан.
3. Введи данные и дождись BLE-проверки: только её успех должен завершить настройку. Убедись, что Suris подключена при отсутствии ef_ble.
4. Проверь 48 сущностей станции. После BMS heartbeat проверь отдельное устройство Extra Battery 1 с 29 датчиками и связью с основной станцией. Все 66 датчиков должны быть enabled. Не получившие свой heartbeat поля могут временно быть unavailable; это отличается от disabled.

**На этом первый тест заканчивается.** Повторно проверять уже подтверждённые AC Ports, DC 12V, USB, X-Boost, Backup Reserve и number controls не нужно. Car Input 2 в первом тесте не трогаем. Отдельные проверки длительной устойчивости, настоящего disconnect/reconnect и холодного старта с отсутствующей станцией пока остаются неподтверждёнными на железе.

## Состав архива

`custom_components/suris_ef_ble_xboost/` — устанавливаемый компонент вместе с `_vendor/eflib`, README, LICENSE и UPSTREAM_NOTICE. `verification/` — воспроизводимые проверки. `audit/` — исходный и итоговый inventory, SHA-256, protocol diff, static checks и pytest log. Дополнительные папки в HA копировать не требуется.

Внешний ef_ble не требуется ни для импорта, ни для credentials, ни для запуска. Штатный Bluetooth Home Assistant и стандартные Python-зависимости из manifest остаются необходимыми. Login-путь обращается к EcoFlow API только при вводе login; ручной User ID и дальнейшая работа используют BLE.
