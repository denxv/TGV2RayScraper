from argparse import Namespace
from pathlib import Path
from typing import (
    Callable,
    cast,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    ParamSpec,
    Sequence,
    TypeVar,
    TypedDict,
    Tuple,
    Union,
)

from httpx import AsyncClient, Client


class ChannelInfo(TypedDict):
    count: int
    current_id: int
    last_id: int


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
RegexTarget = Union[str, bytes]
URL = str

AbsPath = str
FileMode = Literal["a", "w"]

BatchSize = int
DefaultPostID = int
MaxValue = Union[float, int]
MinValue = Union[float, int]
NumberValue = Union[float, int, str]
PostID = int
PostIndex = int

ChannelName = str
ChannelsDict = Dict[ChannelName, ChannelInfo]
ChannelNames = List[ChannelName]
ChannelsAndNames = Tuple[ChannelsDict, ChannelNames]

CLIFlags = Sequence[CLIFlag]
CLIParams = List[CLIParam]

ConfigField = str
ConfigFields = List[ConfigField]

FilePath = Union[str, Path]
FilePaths = List[FilePath]

SortKey = Tuple[int, Union[int, str, None]]
SortKeys = Tuple[SortKey, ...]

ComplexValue = Union[int, str, None, Dict[str, str], List[str], Tuple[str]]
ScalarValue = Union[int, str, None]

V2RayConfigRaw = Dict[str, str]
V2RayConfigsRaw = List[V2RayConfigRaw]
V2RayConfigRawIterator = Iterator[V2RayConfigRaw]

V2RayConfig = Dict[str, Union[int, str, Dict[str, str]]]
V2RayConfigs = List[V2RayConfig]
ConfigPredicate = Callable[[V2RayConfig], bool]

V2RayRawLines = List[str]
PostIDAndRawLines = Tuple[PostID, V2RayRawLines]
