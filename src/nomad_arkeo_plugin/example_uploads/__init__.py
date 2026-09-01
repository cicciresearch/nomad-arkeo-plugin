from nomad.config.models.plugins import ExampleUploadEntryPoint

example_upload_entry_point = ExampleUploadEntryPoint(
    title="ARKEO Stability Example",
    category="Examples",
    description="Sample CICCI Research ARKEO Stability Parameters, Tracking and JV files.",
    resources=["example_uploads/getting_started/*"],
)
