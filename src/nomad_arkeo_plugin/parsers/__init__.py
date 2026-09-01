try:
    from nomad.config.models.plugins import ParserEntryPoint
except ModuleNotFoundError:
    # Allows the pure raw-text reader/tests to run without installing NOMAD.
    ParserEntryPoint = None


if ParserEntryPoint is not None:
    class ArkeoParserEntryPoint(ParserEntryPoint):
        def load(self):
            from .parser import ArkeoStabilityParser
            return ArkeoStabilityParser()


    parser_entry_point = ArkeoParserEntryPoint(
        name="ARKEO Stability Parser",
        description="Parser for CICCI Research ARKEO Stability Parameters/Tracking/JV exports.",
        mainfile_name_re=r".*_Stability \(Parameters\)_.*\.txt$",
    )
else:
    parser_entry_point = None
