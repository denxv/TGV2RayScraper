from argparse import (
    Namespace,
)
from collections.abc import (
    Callable,
    Generator,
    Iterable,
    Iterator,
    Sequence,
    Sized,
)
from pathlib import (
    Path,
)
from re import (
    Pattern,
)
from typing import (
    Literal,
    ParamSpec,
    TypeAlias,
    TypedDict,
    TypeVar,
    Union,
)

from httpx import (
    AsyncClient,
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
    "CompiledRegex",
    "ComplexValue",
    "ConditionStr",
    "ConfigField",
    "ConfigFields",
    "DefaultPostID",
    "FileMode",
    "FilePath",
    "FilePaths",
    "FloatStr",
    "FormatStr",
    "Generator",
    "Iterable",
    "Iterator",
    "Literal",
    "MaxValue",
    "MessageStr",
    "MinValue",
    "NormalizedParamsStr",
    "NumberValue",
    "P",
    "Padding",
    "ParamSpec",
    "ParamsStr",
    "PostID",
    "PostIDAndRawLines",
    "PostIndex",
    "ProtocolName",
    "Record",
    "RecordPredicate",
    "RegexPattern",
    "RegexTarget",
    "ScalarValue",
    "ScriptConfig",
    "ScriptName",
    "ScriptNames",
    "Sequence",
    "Sized",
    "SortKey",
    "SortKeys",
    "T",
    "TemplateStr",
    "TypeAlias",
    "TypeVar",
    "TypedDict",
    "Union",
    "V2RayConfig",
    "V2RayConfigRaw",
    "V2RayConfigRawIterator",
    "V2RayConfigs",
    "V2RayConfigsRaw",
    "V2RayPatternsByProtocol",
    "V2RayRawLines",
]

P = ParamSpec("P")
T = TypeVar("T")


class ChannelInfo(TypedDict):
    count: int
    current_id: int
    last_id: int
    state: int


class ScriptConfig(TypedDict):
    flags: "CLIFlags"


ArgsNamespace: TypeAlias = Namespace
AsyncHTTPClient: TypeAlias = AsyncClient
CompiledRegex: TypeAlias = Pattern[str]

AbsPath: TypeAlias = str
AttrName: TypeAlias = str
B64String: TypeAlias = str
BatchSize: TypeAlias = int
ChannelName: TypeAlias = str
CLIFlag: TypeAlias = str
CLIParam: TypeAlias = str
ConditionStr: TypeAlias = str
ConfigField: TypeAlias = str
DefaultPostID: TypeAlias = int
FloatStr: TypeAlias = str
FormatStr: TypeAlias = str
MessageStr: TypeAlias = str
NormalizedParamsStr: TypeAlias = str
ParamsStr: TypeAlias = str
PostID: TypeAlias = int
PostIndex: TypeAlias = int
ProtocolName: TypeAlias = str
RegexPattern: TypeAlias = str
RegexTarget: TypeAlias = object
ScriptName: TypeAlias = str
TemplateStr: TypeAlias = str
URL: TypeAlias = str

ChannelsDict: TypeAlias = dict["ChannelName", "ChannelInfo"]
V2RayConfig: TypeAlias = dict[str, Union[int, str, dict[str, str]]]
V2RayConfigRaw: TypeAlias = dict[str, str]
V2RayPatternsByProtocol: TypeAlias = dict[
    "ProtocolName",
    tuple["CompiledRegex", ...],
]

CLIParams: TypeAlias = list["CLIParam"]
ChannelNames: TypeAlias = list["ChannelName"]
ConfigFields: TypeAlias = list["ConfigField"]
FilePaths: TypeAlias = list["FilePath"]
ScriptNames: TypeAlias = list["ScriptName"]
V2RayConfigs: TypeAlias = list["V2RayConfig"]
V2RayConfigsRaw: TypeAlias = list["V2RayConfigRaw"]
V2RayRawLines: TypeAlias = list[str]

ChannelsAndNames: TypeAlias = tuple["ChannelsDict", "ChannelNames"]
Padding: TypeAlias = tuple[int, int, int, int]
PostIDAndRawLines: TypeAlias = tuple["PostID", "V2RayRawLines"]
SortKey: TypeAlias = tuple[int, "ScalarValue"]
SortKeys: TypeAlias = tuple["SortKey", ...]

CLIFlags: TypeAlias = Sequence["CLIFlag"]
FileMode: TypeAlias = Literal["a", "w"]
RecordPredicate: TypeAlias = Callable[["Record"], bool]
V2RayConfigRawIterator: TypeAlias = Iterator["V2RayConfigRaw"]

ComplexValue: TypeAlias = Union[
    dict[str, str],
    list[str],
    tuple[str, ...],
    "ScalarValue",
]
FilePath: TypeAlias = Union[str, Path]
MaxValue: TypeAlias = Union[float, int]
MinValue: TypeAlias = Union[float, int]
NumberValue: TypeAlias = Union[float, int, str]
Record: TypeAlias = Union["ChannelInfo", "V2RayConfig"]
ScalarValue: TypeAlias = Union[int, str, None]
