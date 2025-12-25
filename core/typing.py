from argparse import (
    Namespace,
)
from collections.abc import (
    Callable,
    Iterator,
    Sequence,
)
from pathlib import (
    Path,
)
from typing import (
    Literal,
    ParamSpec,
    TypedDict,
    TypeVar,
)

from httpx import (
    AsyncClient,
    Client,
)

__all__ = [
    "URL",
    "AbsPath",
    "ArgsNamespace",
    "AsyncHTTPClient",
    "AttrName",
    "B64String",
    "BatchSize",
    "CLIFlag",
    "CLIFlags",
    "CLIParam",
    "CLIParams",
    "Callable",
    "ChannelInfo",
    "ChannelName",
    "ChannelNames",
    "ChannelsAndNames",
    "ChannelsDict",
    "ComplexValue",
    "ConditionStr",
    "ConfigField",
    "ConfigFields",
    "ConfigPredicate",
    "DefaultPostID",
    "FileMode",
    "FilePath",
    "FilePaths",
    "FloatStr",
    "MaxValue",
    "MinValue",
    "NormalizedParamsStr",
    "NumberValue",
    "P",
    "ParamsStr",
    "PostID",
    "PostIDAndRawLines",
    "PostIndex",
    "RegexPattern",
    "RegexTarget",
    "ScalarValue",
    "SortKey",
    "SortKeys",
    "SyncHTTPClient",
    "T",
    "V2RayConfig",
    "V2RayConfigRaw",
    "V2RayConfigRawIterator",
    "V2RayConfigs",
    "V2RayConfigsRaw",
    "V2RayRawLines",
]


class ChannelInfo(
    TypedDict,
    total=False,
):
    count: int
    current_id: int
    last_id: int
    state: int


ArgsNamespace = Namespace
AsyncHTTPClient = AsyncClient
SyncHTTPClient = Client

P = ParamSpec("P")
T = TypeVar("T")

AttrName = str
B64String = str
CLIFlag = str
CLIParam = str
ConditionStr = str
FloatStr = str
NormalizedParamsStr = str
ParamsStr = str
RegexPattern = str
RegexTarget = str | bytes
URL = str

BatchSize = int
DefaultPostID = int
MaxValue = float | int
MinValue = float | int
NumberValue = float | int | str
PostID = int
PostIndex = int

ChannelName = str
ChannelsDict = dict[ChannelName, ChannelInfo]
ChannelNames = list[ChannelName]
ChannelsAndNames = tuple[ChannelsDict, ChannelNames]

CLIFlags = Sequence[CLIFlag]
CLIParams = list[CLIParam]

ConfigField = str
ConfigFields = list[ConfigField]

AbsPath = str
FileMode = Literal["a", "w"]
FilePath = str | Path
FilePaths = list[FilePath]

SortKey = tuple[int, int | str | None]
SortKeys = tuple[SortKey, ...]

ComplexValue = int | str | None | dict[str, str] | list[str] | tuple[str]
ScalarValue = int | str | None

V2RayConfigRaw = dict[str, str]
V2RayConfigsRaw = list[V2RayConfigRaw]
V2RayConfigRawIterator = Iterator[V2RayConfigRaw]

V2RayConfig = dict[str, int | str | dict[str, str]]
V2RayConfigs = list[V2RayConfig]
ConfigPredicate = Callable[[V2RayConfig], bool]

V2RayRawLines = list[str]
PostIDAndRawLines = tuple[PostID, V2RayRawLines]
