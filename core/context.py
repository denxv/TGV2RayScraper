from dataclasses import (
    dataclass,
)

from core.constants.common import (
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
from core.typing import (
    AsyncHTTPClient,
    BatchSize,
    FilePath,
)


@dataclass
class ChannelUpdateContext:
    batch_size: BatchSize = CHANNELS_BATCH_DEFAULT


@dataclass
class ConfigExtractionContext:
    batch_size: BatchSize = CONFIGS_BATCH_DEFAULT
    max_concurrent_channels: int = CHANNELS_CONCURRENCY_DEFAULT


@dataclass
class HttpContext:
    client: AsyncHTTPClient
    retries: int = HTTP_RETRIES_DEFAULT
    retry_delay: float = HTTP_RETRY_DELAY_DEFAULT


@dataclass
class IOContext:
    channels_path: FilePath = DEFAULT_PATH_CHANNELS
    configs_clean_path: FilePath = DEFAULT_PATH_CONFIGS_CLEAN
    configs_export_path: FilePath = DEFAULT_PATH_CONFIGS_EXPORT
    configs_import_path: FilePath = DEFAULT_PATH_CONFIGS_IMPORT
    configs_raw_path: FilePath = DEFAULT_PATH_CONFIGS_RAW
    urls_path: FilePath = DEFAULT_PATH_URLS


@dataclass
class PipelineRuntimeContext:
    channel_update: ChannelUpdateContext
    config_extraction: ConfigExtractionContext


@dataclass
class RuntimeContext:
    http: HttpContext
    io: IOContext
    pipeline: PipelineRuntimeContext
