from argparse import Namespace
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    ParamSpec,
    TypeVar,
    TypedDict,
    Tuple,
    Union,
)

from aiohttp import ClientSession
from requests import Session


class ChannelInfo(TypedDict):
    count: int
    current_id: int
    last_id: int


ArgsNamespace = Namespace
AsyncSession = ClientSession
SyncSession = Session

P = ParamSpec("P")
T = TypeVar("T")

AnyFunc = Callable[P, T]
FuncDecorator = Callable[[AnyFunc[P, T]], AnyFunc[P, T]]
ConfigPredicate = Callable[[Dict[str, Any]], bool]

AttrName = str
B64String = str
CLIFlag = str
CLIParam = str
ConditionStr = str
IntStr = str
NormalizedParamsStr = str
ParamsStr = str
RegexPattern = str
RegexTarget = str
URL = str
FileMode = str
AbsPath = str

BatchSize = int
DefaultPostID = int
IntRangeValue = Union[int, str]
MaxValue = int
MinValue = int
PostID = int
PostIndex = int

ChannelName = str
ChannelsDict = Dict[ChannelName, ChannelInfo]
ChannelNames = List[ChannelName]
ChannelsAndNames = Tuple[ChannelsDict, ChannelNames]

CLIFlags = List[CLIFlag]
CLIParams = List[CLIParam]

ConfigField = str
ConfigFields = List[ConfigField]

FilePath = Union[str, Path]
FilePaths = List[FilePath]

SortKey = Tuple[int, Union[Any, None]]
SortKeys = Tuple[SortKey, ...]

V2RayConfig = Dict[str, Any]
V2RayConfigIterator = Iterator[V2RayConfig]
V2RayConfigs = List[V2RayConfig]

V2RayConfigRaw = str
V2RayConfigsRaw = List[V2RayConfigRaw]
PostIDAndConfigsRaw = Tuple[PostID, V2RayConfigsRaw]
