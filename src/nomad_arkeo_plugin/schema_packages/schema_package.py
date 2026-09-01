from __future__ import annotations

import numpy as np
from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.basesections import Measurement, MeasurementResult
from nomad.metainfo import Datetime, Quantity, SchemaPackage, Section, SubSection

m_package = SchemaPackage(name="arkeo_measurements")


class ArkeoInstrument(ArchiveSection):
    m_def = Section(label="ARKEO instrument")
    manufacturer = Quantity(type=str, default="CICCI Research")
    product = Quantity(type=str, default="ARKEO")
    model = Quantity(type=str)
    serial_number = Quantity(type=str)
    software = Quantity(type=str)
    software_version = Quantity(type=str)
    data_format_version = Quantity(type=str)
    identification_method = Quantity(type=str)


class ArkeoChannelSettings(ArchiveSection):
    m_def = Section(label="Channel settings")
    voltage_range = Quantity(type=np.float64, unit="V")
    current_range_label = Quantity(type=str)


class ArkeoCellSettings(ArchiveSection):
    m_def = Section(label="Cell settings")
    device_id = Quantity(type=str)
    device_type = Quantity(type=str)
    cell_area = Quantity(type=np.float64, unit="cm**2")
    inverted = Quantity(type=bool)
    number_of_cells = Quantity(type=int)


class ArkeoEnvironmentSettings(ArchiveSection):
    m_def = Section(label="Environment settings")
    irradiance = Quantity(type=np.float64, unit="mW/cm**2")


class ArkeoJVSettings(ArchiveSection):
    m_def = Section(label="JV settings")
    vmin = Quantity(type=np.float64, unit="V")
    vmax = Quantity(type=np.float64, unit="V")
    voltage_step = Quantity(type=np.float64, unit="mV")
    scan_rate = Quantity(type=np.float64, unit="mV/s")
    scan_order = Quantity(type=str)
    auto_detect_voc = Quantity(type=bool)
    overvoltage_percent = Quantity(type=np.float64)


class ArkeoTrackingSettings(ArchiveSection):
    m_def = Section(label="Stability tracking settings")
    algorithm = Quantity(type=str)
    jv_timing = Quantity(type=str)
    jv_interval = Quantity(type=np.float64, unit="hour")
    test_duration = Quantity(type=np.float64, unit="hour")
    startup_time_raw = Quantity(type=str)
    min_dv = Quantity(type=np.float64, unit="V")


class ArkeoTrackingResult(MeasurementResult):
    m_def = Section(label="MPPT tracking")
    time_axis_kind = Quantity(type=str)
    time_hours = Quantity(type=np.float64, unit="hour", shape=["*"])
    timestamp_text = Quantity(type=str, shape=["*"])
    voltage = Quantity(type=np.float64, unit="V", shape=["*"])
    current_density = Quantity(type=np.float64, unit="mA/cm**2", shape=["*"])
    power_density = Quantity(type=np.float64, unit="mW/cm**2", shape=["*"])


class ArkeoJVResult(MeasurementResult):
    m_def = Section(label="JV result")
    direction = Quantity(type=str)
    voc = Quantity(type=np.float64, unit="V")
    jsc = Quantity(type=np.float64, unit="A/cm**2")
    v_mpp = Quantity(type=np.float64, unit="V")
    j_mpp = Quantity(type=np.float64, unit="A/cm**2")
    p_mpp = Quantity(type=np.float64, unit="W/cm**2")
    series_resistance = Quantity(type=np.float64, unit="ohm")
    shunt_resistance = Quantity(type=np.float64, unit="ohm")
    fill_factor_percent = Quantity(type=np.float64)
    efficiency_percent = Quantity(type=np.float64)
    voltage = Quantity(type=np.float64, unit="V", shape=["*"])
    current_density = Quantity(type=np.float64, unit="A/cm**2", shape=["*"])


class ArkeoStabilitySummary(ArchiveSection):
    m_def = Section(label="Stability summary")
    time_hours = Quantity(type=np.float64, unit="hour", shape=["*"])
    voc_fw = Quantity(type=np.float64, unit="V", shape=["*"])
    jsc_fw = Quantity(type=np.float64, unit="mA/cm**2", shape=["*"])
    v_mpp_fw = Quantity(type=np.float64, unit="V", shape=["*"])
    j_mpp_fw = Quantity(type=np.float64, unit="mA/cm**2", shape=["*"])
    p_mpp_fw = Quantity(type=np.float64, unit="mW/cm**2", shape=["*"])
    series_resistance_fw = Quantity(type=np.float64, unit="ohm", shape=["*"])
    shunt_resistance_fw = Quantity(type=np.float64, unit="ohm", shape=["*"])
    fill_factor_fw = Quantity(type=np.float64, shape=["*"])
    efficiency_fw = Quantity(type=np.float64, shape=["*"])
    voc_rv = Quantity(type=np.float64, unit="V", shape=["*"])
    jsc_rv = Quantity(type=np.float64, unit="mA/cm**2", shape=["*"])
    v_mpp_rv = Quantity(type=np.float64, unit="V", shape=["*"])
    j_mpp_rv = Quantity(type=np.float64, unit="mA/cm**2", shape=["*"])
    p_mpp_rv = Quantity(type=np.float64, unit="mW/cm**2", shape=["*"])
    series_resistance_rv = Quantity(type=np.float64, unit="ohm", shape=["*"])
    shunt_resistance_rv = Quantity(type=np.float64, unit="ohm", shape=["*"])
    fill_factor_rv = Quantity(type=np.float64, shape=["*"])
    efficiency_rv = Quantity(type=np.float64, shape=["*"])


class ArkeoStabilityMeasurement(Measurement, EntryData):
    m_def = Section(label="ARKEO Stability measurement")
    method = Quantity(type=str, default="ARKEO stability (MPPT + JV)")
    measurement_start = Quantity(type=Datetime)
    user = Quantity(type=str)
    note = Quantity(type=str)
    source_files = Quantity(type=str, shape=["*"])
    instrument = SubSection(section_def=ArkeoInstrument)
    channel_settings = SubSection(section_def=ArkeoChannelSettings)
    cell = SubSection(section_def=ArkeoCellSettings)
    environment = SubSection(section_def=ArkeoEnvironmentSettings)
    jv_settings = SubSection(section_def=ArkeoJVSettings)
    tracking_settings = SubSection(section_def=ArkeoTrackingSettings)
    stability_summary = SubSection(section_def=ArkeoStabilitySummary)
    tracking_result = SubSection(section_def=ArkeoTrackingResult)
    jv_results = SubSection(section_def=ArkeoJVResult, repeats=True)


m_package.__init_metainfo__()
