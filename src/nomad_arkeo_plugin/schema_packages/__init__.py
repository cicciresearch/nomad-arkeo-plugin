from nomad.config.models.plugins import SchemaPackageEntryPoint


class ArkeoSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from .schema_package import m_package
        return m_package


schema_package_entry_point = ArkeoSchemaPackageEntryPoint(
    name="ARKEO measurement schema",
    description="Schema definitions for CICCI Research ARKEO photovoltaic measurements.",
)
