from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Transaction(_message.Message):
    __slots__ = ("transaction_name", "amount", "date")
    TRANSACTION_NAME_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    transaction_name: str
    amount: float
    date: str
    def __init__(self, transaction_name: _Optional[str] = ..., amount: _Optional[float] = ..., date: _Optional[str] = ...) -> None: ...

class TransactionAddRequest(_message.Message):
    __slots__ = ("transaction",)
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    transaction: Transaction
    def __init__(self, transaction: _Optional[_Union[Transaction, _Mapping]] = ...) -> None: ...

class TransactionAddReply(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: int
    def __init__(self, status: _Optional[int] = ...) -> None: ...

class TransactionGetRequest(_message.Message):
    __slots__ = ("start_date", "end_date")
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    start_date: str
    end_date: str
    def __init__(self, start_date: _Optional[str] = ..., end_date: _Optional[str] = ...) -> None: ...

class TransactionGetReply(_message.Message):
    __slots__ = ("status", "transactions")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    status: int
    transactions: _containers.RepeatedCompositeFieldContainer[Transaction]
    def __init__(self, status: _Optional[int] = ..., transactions: _Optional[_Iterable[_Union[Transaction, _Mapping]]] = ...) -> None: ...
