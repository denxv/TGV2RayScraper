from core.context import (
    ChannelUpdateContext,
    ConfigExtractionContext,
    HttpContext,
    IOContext,
    PipelineRuntimeContext,
    RuntimeContext,
)
from tests.unit.core.constants.common import (
    CHANNELS_BATCH_DEFAULT,
    CHANNELS_CONCURRENCY_DEFAULT,
    CONFIGS_BATCH_DEFAULT,
    DEFAULT_PATH_CHANNELS,
    DEFAULT_PATH_CONFIGS_CLEAN,
    DEFAULT_PATH_CONFIGS_EXPORT,
    DEFAULT_PATH_CONFIGS_IMPORT,
    DEFAULT_PATH_CONFIGS_RAW,
    DEFAULT_PATH_URLS,
    HTTP_RETRIES_DEFAULT,
    HTTP_RETRY_DELAY_DEFAULT,
)


class TestClient:
    pass


def test_http_context_defaults() -> None:
    ctx = HttpContext(
        client=TestClient(),
    )

    assert ctx.retries == HTTP_RETRIES_DEFAULT
    assert ctx.retry_delay == HTTP_RETRY_DELAY_DEFAULT


def test_io_context_defaults() -> None:
    ctx = IOContext()

    assert ctx.channels_path == DEFAULT_PATH_CHANNELS
    assert ctx.configs_clean_path == DEFAULT_PATH_CONFIGS_CLEAN
    assert ctx.configs_export_path == DEFAULT_PATH_CONFIGS_EXPORT
    assert ctx.configs_import_path == DEFAULT_PATH_CONFIGS_IMPORT
    assert ctx.configs_raw_path == DEFAULT_PATH_CONFIGS_RAW
    assert ctx.urls_path == DEFAULT_PATH_URLS


def test_pipeline_channel_update_defaults() -> None:
    ctx = ChannelUpdateContext()

    assert ctx.batch_size == CHANNELS_BATCH_DEFAULT


def test_pipeline_config_extraction_defaults() -> None:
    ctx = ConfigExtractionContext()

    assert ctx.batch_size == CONFIGS_BATCH_DEFAULT
    assert ctx.max_concurrent_channels == CHANNELS_CONCURRENCY_DEFAULT


def test_runtime_context_builds() -> None:
    ctx = RuntimeContext(
        http=HttpContext(
            client=TestClient(),
        ),
        io=IOContext(),
        pipeline=PipelineRuntimeContext(
            channel_update=ChannelUpdateContext(),
            config_extraction=ConfigExtractionContext(),
        ),
    )

    max_channels = ctx.pipeline.config_extraction.max_concurrent_channels

    assert ctx.http.client is not None
    assert ctx.io.channels_path == DEFAULT_PATH_CHANNELS
    assert max_channels == CHANNELS_CONCURRENCY_DEFAULT
