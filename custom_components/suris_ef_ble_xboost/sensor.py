# SPDX-License-Identifier: Apache-2.0
# Suris additions/adaptations, 2026. See NOTICE for upstream attribution.
# This is an independently modified, unofficial integration.
"""Complete D2M inventory and all decoded BMS1 fields, enabled by default."""
from dataclasses import dataclass, fields
import math

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.core import callback

from ._vendor.eflib.model import DirectBmsMDeltaHeartbeatPack
from .entity import SurisEntity
from .registry import async_ensure_battery_device


@dataclass(frozen=True)
class SensorSpec:
    key: str
    name: str
    kind: str = "raw"
    message: str | None = None
    field: str | None = None
    scale: int = 1
    precision: int | None = None
    custom: bool = False
    battery: bool = False


MAIN_SENSORS = (
    SensorSpec("battery_level", "Battery Level", "battery"),
    SensorSpec("battery_level_main", "Main Battery Level", "battery"),
    SensorSpec("input_power", "Input Power", "power"),
    SensorSpec("output_power", "Output Power", "power"),
    SensorSpec("remaining_time_charging", "Charge Time Remaining", "duration"),
    SensorSpec("remaining_time_discharging", "Discharge Time Remaining", "duration"),
    SensorSpec("battery_voltage", "Battery Voltage", "voltage"),
    SensorSpec("ac_input_power", "AC Input Power", "power"),
    SensorSpec("ac_input_voltage", "AC Input Voltage", "voltage"),
    SensorSpec("ac_input_current", "AC Input Current", "current"),
    SensorSpec("ac_output_power", "AC Output Power", "power"),
    SensorSpec("ac_output_voltage", "AC Output Voltage", "voltage"),
    SensorSpec("ac_output_current", "AC Output Current", "current"),
    SensorSpec("dc_output_power", "DC Output Power", "power"),
    SensorSpec("usba_output_power", "USB A (1) Output Power", "power"),
    SensorSpec("usba2_output_power", "USB A (2) Output Power", "power"),
    SensorSpec("usbc_output_power", "USB C (1) Output Power", "power"),
    SensorSpec("usbc2_output_power", "USB C (2) Output Power", "power"),
    SensorSpec("qc_usb1_output_power", "USB A QC (1) Output Power", "power"),
    SensorSpec("qc_usb2_output_power", "USB A QC (2) Output Power", "power"),
    SensorSpec("cell_temperature", "Cell Temperature", "temperature"),
    SensorSpec("max_cell_voltage", "Max Cell Voltage", "voltage", precision=3),
    SensorSpec("min_cell_voltage", "Min Cell Voltage", "voltage", precision=3),
    SensorSpec("dc12v_output_voltage", "DC 12V Output Voltage", "voltage"),
    SensorSpec("dc12v_output_current", "DC 12V Output Current", "current"),
    SensorSpec("dc_input_voltage", "DC Input Voltage", "voltage"),
    SensorSpec("dc_input_current", "DC Input Current", "current"),
    SensorSpec("xt60_1_input_power", "XT60 (1) Input Power", "power"),
    SensorSpec("xt60_2_input_power", "XT60 (2) Input Power", "power"),
    SensorSpec("inverter_out_temperature", "Inverter Out Temperature", "temperature", "DirectInvDeltaHeartbeatPack", "out_temp", custom=True),
    SensorSpec("inverter_dc_in_temperature", "Inverter DC In Temperature", "temperature", "DirectInvDeltaHeartbeatPack", "dc_in_temp", custom=True),
    SensorSpec("power_difference", "BLE Power Difference", "power", "Mr350PdHeartbeatDelta2Max", "difference", custom=True),
    SensorSpec("xt60_2_voltage", "XT60 (2) Voltage", "voltage", "Mr350MpptHeart", "pv2_in_vol", 1000, 2, custom=True),
    SensorSpec("mppt_1_temperature", "MPPT Temperature 1", "temperature", "Mr350MpptHeart", "mppt_temp", custom=True),
    SensorSpec("mppt_2_temperature", "MPPT Temperature 2", "temperature", "Mr350MpptHeart", "pv2_mppt_temp", custom=True),
    SensorSpec("fan_speed_level", "Fan Speed Level", "raw", "DirectInvDeltaHeartbeatPack", "fan_state", custom=True),
    SensorSpec("main_battery_cycles", "Main Battery Cycles", "cycles", "_BmsHeartbeatBatteryMain", "cycles", custom=True),
)

# No guessed sign, scaling or physical units for fields only named in the decoder.
# Raw fields retain exactly the upstream decoded value, including version/status codes.
_BMS_OVERRIDES = {
    "f32_show_soc": ("battery_1_battery_level", "Battery Level", "battery", 1, 2, False),
    "max_cell_temp": ("battery_1_cell_temperature", "Cell Temperature", "temperature", 1, None, False),
    "vol": ("battery_1_voltage", "Battery Voltage", "voltage", 1000, 2, False),
    "max_cell_vol": ("battery_1_max_cell_voltage", "Max Cell Voltage", "voltage", 1000, 3, False),
    "min_cell_vol": ("battery_1_min_cell_voltage", "Min Cell Voltage", "voltage", 1000, 3, False),
    "cycles": ("slave_1_cycles", "Slave 1 Cycles", "cycles", 1, None, True),
    "input_watts": ("battery_1_input_power", "Input Power", "power", 1, None, False),
    "output_watts": ("battery_1_output_power", "Output Power", "power", 1, None, False),
    "soc": ("battery_1_soc", "BMS SOC", "battery", 1, None, False),
    "soh": ("battery_1_soh", "BMS SOH", "percent", 1, None, False),
    "temp": ("battery_1_temp", "BMS Temperature", "temperature", 1, None, False),
    "min_cell_temp": ("battery_1_min_cell_temp", "Min Cell Temperature", "temperature", 1, None, False),
    "max_mos_temp": ("battery_1_max_mos_temp", "Max MOS Temperature", "temperature", 1, None, False),
    "min_mos_temp": ("battery_1_min_mos_temp", "Min MOS Temperature", "temperature", 1, None, False),
}
_RAW_NAMES = {
    "num": "BMS Number (raw)", "type_": "BMS Type (raw)", "cell_id": "Cell ID (raw)",
    "err_code": "BMS Error Code (raw)", "sys_ver": "BMS Firmware Version (raw)",
    "amp": "BMS Current (raw)", "open_bms_idx": "Open BMS Index (raw)",
    "design_cap": "Design Capacity (raw)", "remain_cap": "Remaining Capacity (raw)",
    "full_cap": "Full Capacity (raw)", "bms_fault": "BMS Fault (raw)",
    "bq_sys_stat_reg": "BQ System Status (raw)", "tag_chg_amp": "Target Charge Current (raw)",
    "remain_time": "BMS Remaining Time (raw)",
}


def _battery_specs():
    result = []
    for field in fields(DirectBmsMDeltaHeartbeatPack):
        key, name, kind, scale, precision, custom = _BMS_OVERRIDES.get(field.name, (
            f"battery_1_{field.name.rstrip('_')}", _RAW_NAMES.get(field.name, field.name), "raw", 1, None, False,
        ))
        result.append(SensorSpec(key, name, kind, "_BmsHeartbeatBattery1", field.name, scale, precision, custom, True))
    result.append(SensorSpec("slave_1_power_difference", "BLE Slave 1 Power Difference", "power", "_BmsHeartbeatBattery1", "difference", custom=True, battery=True))
    return tuple(result)


BATTERY_SENSORS = _battery_specs()
_METADATA = {
    "battery": (SensorDeviceClass.BATTERY, "%"), "percent": (None, "%"),
    "power": (SensorDeviceClass.POWER, "W"), "voltage": (SensorDeviceClass.VOLTAGE, "V"),
    "current": (SensorDeviceClass.CURRENT, "A"), "temperature": (SensorDeviceClass.TEMPERATURE, "°C"),
    "duration": (SensorDeviceClass.DURATION, "min"), "cycles": (None, "cycles"),
}


async def async_setup_entry(hass, entry, async_add_entities):
    runtime = entry.runtime_data
    async_add_entities([SurisSensor(runtime, spec) for spec in MAIN_SENSORS])
    added = False

    @callback
    def add_battery():
        nonlocal added
        if runtime.closed or not runtime.battery_seen:
            return
        async_ensure_battery_device(hass, entry, runtime)
        if not added:
            added = True
            async_add_entities([SurisSensor(runtime, spec) for spec in BATTERY_SENSORS])

    entry.async_on_unload(runtime.subscribe(add_battery))
    add_battery()


class SurisSensor(SurisEntity, SensorEntity):
    def __init__(self, runtime, spec):
        super().__init__(runtime, spec.key, spec.name, battery=spec.battery, custom=spec.custom)
        self.spec = spec
        if metadata := _METADATA.get(spec.kind):
            self._attr_device_class, self._attr_native_unit_of_measurement = metadata
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING if spec.kind == "cycles" else SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = spec.precision

    @property
    def native_value(self):
        spec = self.spec
        if spec.message is None:
            return getattr(self._device, spec.key, None)
        msg = self.runtime.raw.get(spec.message)
        if spec.field == "difference":
            in_field, out_field = ("input_watts", "output_watts") if spec.battery else ("watts_in_sum", "watts_out_sum")
            value_in, value_out = getattr(msg, in_field, None), getattr(msg, out_field, None)
            return None if value_in is None or value_out is None else value_out - value_in
        value = getattr(msg, spec.field, None)
        if value is None or (isinstance(value, float) and not math.isfinite(value)):
            return None
        if spec.field == "fan_state" and value not in (0, 1, 2, 3):
            return None
        if spec.scale != 1:
            value /= spec.scale
        return round(value, spec.precision) if spec.precision is not None else value

    @property
    def available(self):
        return super().available and self.native_value is not None

    @property
    def extra_state_attributes(self):
        if self.key == "battery_voltage":
            return {key: getattr(self._device, key, None) for key in ("max_cell_voltage", "min_cell_voltage")}
        if self.key == "battery_1_voltage":
            return {key: self.runtime.raw_value("_BmsHeartbeatBattery1", field) / 1000
                    for key, field in (("max_cell_voltage", "max_cell_vol"), ("min_cell_voltage", "min_cell_vol"))
                    if self.runtime.raw_value("_BmsHeartbeatBattery1", field) is not None}
        return None
