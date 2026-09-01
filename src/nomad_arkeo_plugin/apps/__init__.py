from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Menu,
    MenuItemHistogram,
    MenuItemTerms,
    MenuSizeEnum,
    SearchQuantities,
)

SCHEMA_QN = "nomad_arkeo_plugin.schema_packages.schema_package.ArkeoStabilityMeasurement"

app_entry_point = AppEntryPoint(
    name="ARKEO Explorer",
    description="Browse and filter structured CICCI Research ARKEO measurements.",
    app=App(
        label="ARKEO",
        path="arkeo",
        category="Measurements",
        breadcrumb="Explore ARKEO",
        search_quantities=SearchQuantities(
            include=[
                f"*#{SCHEMA_QN}",
                "authors.name",
                "datasets.dataset_name",
                "upload_create_time",
                "upload_user.name",
                "entry_id",
                "mainfile",
            ]
        ),
        filters_locked={"section_defs.definition_qualified_name": [SCHEMA_QN]},
        columns=[
            Column(quantity=f"data.cell.device_id#{SCHEMA_QN}", label="Device", selected=True),
            Column(
                quantity=f"data.measurement_start#{SCHEMA_QN}",
                label="Measurement time",
                selected=True,
            ),
            Column(
                quantity=f"data.instrument.product#{SCHEMA_QN}", label="Instrument", selected=True
            ),
            Column(quantity=f"data.instrument.model#{SCHEMA_QN}", label="Model", selected=False),
            Column(
                quantity=f"data.environment.irradiance#{SCHEMA_QN}",
                label="Irradiance",
                unit="mW/cm**2",
                selected=True,
            ),
            Column(
                quantity=f"data.tracking_settings.algorithm#{SCHEMA_QN}",
                label="Tracking",
                selected=True,
            ),
            Column(
                quantity=f"data.tracking_settings.test_duration#{SCHEMA_QN}",
                label="Duration",
                unit="hour",
                selected=True,
            ),
            Column(
                quantity=f"data.jv_results[0].voc#{SCHEMA_QN}",
                label="Voc (FW)",
                unit="V",
                selected=True,
            ),
            Column(
                quantity=f"data.jv_results[0].jsc#{SCHEMA_QN}",
                label="Jsc (FW)",
                unit="mA/cm**2",
                selected=True,
            ),
            Column(
                quantity=f"data.jv_results[0].fill_factor_percent#{SCHEMA_QN}",
                label="FF (FW)",
                selected=True,
            ),
            Column(
                quantity=f"data.jv_results[0].efficiency_percent#{SCHEMA_QN}",
                label="Efficiency (FW)",
                selected=True,
            ),
            Column(quantity="authors.name", label="Author", selected=False),
            Column(quantity="datasets.dataset_name", label="Dataset", selected=False),
        ],
        menu=Menu(
            items=[
                MenuItemTerms(
                    search_quantity=f"data.instrument.manufacturer#{SCHEMA_QN}",
                    title="Manufacturer",
                ),
                MenuItemTerms(
                    search_quantity=f"data.instrument.product#{SCHEMA_QN}", title="Instrument"
                ),
                MenuItemTerms(search_quantity=f"data.instrument.model#{SCHEMA_QN}", title="Model"),
                MenuItemTerms(search_quantity=f"data.cell.device_id#{SCHEMA_QN}", title="Device"),
                MenuItemTerms(
                    search_quantity=f"data.tracking_settings.algorithm#{SCHEMA_QN}",
                    title="Tracking algorithm",
                ),
                Menu(
                    title="Environment",
                    size=MenuSizeEnum.MD,
                    items=[
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity=f"data.environment.irradiance#{SCHEMA_QN}",
                                unit="mW/cm**2",
                            ),
                            title="Irradiance",
                            show_input=True,
                            nbins=30,
                        )
                    ],
                ),
                Menu(
                    title="JV results",
                    size=MenuSizeEnum.MD,
                    items=[
                        MenuItemHistogram(
                            x=Axis(search_quantity=f"data.jv_results.voc#{SCHEMA_QN}", unit="V"),
                            title="Voc",
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity=f"data.jv_results.jsc#{SCHEMA_QN}", unit="mA/cm**2"
                            ),
                            title="Jsc",
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity=f"data.jv_results.fill_factor_percent#{SCHEMA_QN}"
                            ),
                            title="Fill factor (%)",
                            show_input=True,
                            nbins=30,
                        ),
                        MenuItemHistogram(
                            x=Axis(
                                search_quantity=f"data.jv_results.efficiency_percent#{SCHEMA_QN}"
                            ),
                            title="Efficiency (%)",
                            show_input=True,
                            nbins=30,
                        ),
                    ],
                ),
            ]
        ),
    ),
)
