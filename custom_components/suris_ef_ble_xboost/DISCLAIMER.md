# Предупреждение и отказ от гарантий / Disclaimer

## Русский

**ЭТО НЕОФИЦИАЛЬНАЯ НЕСТАБИЛЬНАЯ БЕТА-ВЕРСИЯ. ИСПОЛЬЗУЙ ОСТОРОЖНО И НА СВОЙ РИСК.**

Suris EcoFlow BLE — независимый экспериментальный проект. Он не разработан,
не сертифицирован и не одобрен компанией EcoFlow; он также не является официальным
релизом проекта EcoFlow BLE / ha-ef-ble. Благодарность исходным авторам не означает,
что они одобрили, проверили или поддерживают изменения Suris.

Программа предоставляется «КАК ЕСТЬ», без каких-либо явных или подразумеваемых
гарантий, в том числе работоспособности, безопасности, точности показаний,
совместимости, пригодности для конкретной цели и ненарушения прав третьих лиц.
Ни работа на конкретной станции, ни сохранность оборудования и данных не гарантируются.

**В МАКСИМАЛЬНО ДОПУСТИМОЙ ПРИМЕНИМЫМ ЗАКОНОДАТЕЛЬСТВОМ СТЕПЕНИ АВТОРЫ,
ПРАВООБЛАДАТЕЛИ, УЧАСТНИКИ И РАСПРОСТРАНИТЕЛИ НЕ НЕСУТ НИКАКОЙ ОТВЕТСТВЕННОСТИ
ЗА ИСПОЛЬЗОВАНИЕ ИЛИ НЕВОЗМОЖНОСТЬ ИСПОЛЬЗОВАНИЯ ЭТОЙ ПРОГРАММЫ И ЗА ЕГО
ПОСЛЕДСТВИЯ.** Это включает прямой и косвенный ущерб, повреждение станции, батареи
или подключённых устройств, потерю данных, прекращение питания, простой, расходы,
упущенную выгоду и иной вред, даже если о возможности такого вреда было известно.
Пользователь самостоятельно принимает решение об установке, выбирает настройки
и проверяет фактическое поведение оборудования.

Этот текст **не исключает ответственность и права, которые нельзя исключить
или ограничить по закону**, и не обещает абсолютного освобождения от любой
ответственности. Применяются также разделы 7–9 Apache License 2.0 в LICENSE.
Данный документ не вводит дополнительные ограничения на права, предоставленные
Apache-2.0, и не является гарантией юридической допустимости любого применения.

**Осторожно перед установкой:** сохрани полную резервную копию Home Assistant
и прежнюю версию интеграции. Не устанавливай тестовую сборку непосредственно
в систему, от которой зависит безопасная работа критичного оборудования.

**Осторожно при управлении:** команды могут включать и отключать выходы, менять
зарядную мощность и ток. Проверяй результат каждой команды на станции; первые
испытания проводи под наблюдением с некритичной нагрузкой. Показания HA могут
запаздывать, пропадать или быть неверными. Car Input 2 остаётся экспериментальным.
Интеграция не заменяет штатные защиты и инструкции производителя.

**Осторожно после обновления:** изменения прошивки EcoFlow, Bluetooth или Home
Assistant могут нарушить работу. Сначала проверь связь и показания, затем команды
и только после этого автоматизации. При неожиданном поведении прекрати тест
и отключи интеграцию. Не полагайся на эту бета-версию как на единственный способ
управления или защиты электропитания.

Используй только свои устройства и учётную запись либо доступ с разрешения
владельца. Лицензия исходного кода не заменяет условия сервисов EcoFlow,
разрешение на товарные знаки или требования применимого законодательства.
Поддержка, сроки исправлений и будущая совместимость не гарантируются.

## English

**UNOFFICIAL, UNSTABLE BETA. USE WITH CAUTION AND AT YOUR OWN RISK.**

Suris EcoFlow BLE is an independent experimental project. It is not developed,
certified, endorsed, or supported by EcoFlow and is not an official release of
rabits/ha-ef-ble. Credits do not imply upstream approval of Suris modifications.

The software is supplied AS IS, without express or implied warranties,
including safety, reliability, accuracy, compatibility, fitness for a particular
purpose, and non-infringement. Hardware operation and preservation of equipment
and data are not guaranteed.

**TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THE AUTHORS, COPYRIGHT
HOLDERS, CONTRIBUTORS, AND DISTRIBUTORS ACCEPT NO LIABILITY FOR USE OF, INABILITY
TO USE, OR CONSEQUENCES OF USING THIS SOFTWARE**, including direct, indirect,
incidental, or consequential loss, equipment/battery damage, power interruption,
data loss, downtime, expenses, lost profits, or other harm, even if advised of
the possibility. Users choose their settings and verify actual device behavior.

Nothing here excludes non-excludable liability or mandatory legal rights.
Sections 7–9 of Apache-2.0 also apply. This document does not add restrictions to
Apache-2.0 or guarantee legal clearance for every use.

**Before installation:** back up Home Assistant and keep a rollback copy.
**During testing:** supervise operation, use noncritical loads, and check every
command at the station. Commands may change power outputs and charging settings;
telemetry may be stale or wrong. Car Input 2 is experimental.
**After updates:** recheck connectivity, readings, controls, and automations.
Stop testing and disable the integration if behavior is unexpected. Never use
this beta as the sole protection or control for critical power equipment.

Use only devices/accounts you own or are authorized to access. Respect the
manufacturer's instructions and applicable service terms. Code licensing does
not grant trademark rights or manufacturer approval. Support and future
compatibility are not guaranteed.
