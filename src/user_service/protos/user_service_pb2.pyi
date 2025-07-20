from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterRequest(_message.Message):
    __slots__ = ("user_name", "password")
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    user_name: str
    password: str
    def __init__(self, user_name: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class RegisterReply(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: int
    def __init__(self, status: _Optional[int] = ...) -> None: ...

class AuthenticateRequest(_message.Message):
    __slots__ = ("user_name", "password")
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    user_name: str
    password: str
    def __init__(self, user_name: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class AuthenticateReply(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: int
    def __init__(self, status: _Optional[int] = ...) -> None: ...

class GetUserInformationRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class GetUserInformationReply(_message.Message):
    __slots__ = ("status", "user_name")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    status: int
    user_name: str
    def __init__(self, status: _Optional[int] = ..., user_name: _Optional[str] = ...) -> None: ...
