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

class Report(_message.Message):
    __slots__ = ("transactions", "total_income", "total_operations")
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_INCOME_FIELD_NUMBER: _ClassVar[int]
    TOTAL_OPERATIONS_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[Transaction]
    total_income: float
    total_operations: int
    def __init__(self, transactions: _Optional[_Iterable[_Union[Transaction, _Mapping]]] = ..., total_income: _Optional[float] = ..., total_operations: _Optional[int] = ...) -> None: ...

class ReportGenerateRequest(_message.Message):
    __slots__ = ("transactions",)
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[Transaction]
    def __init__(self, transactions: _Optional[_Iterable[_Union[Transaction, _Mapping]]] = ...) -> None: ...

class ReportGenerateReply(_message.Message):
    __slots__ = ("status", "report")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REPORT_FIELD_NUMBER: _ClassVar[int]
    status: int
    report: Report
    def __init__(self, status: _Optional[int] = ..., report: _Optional[_Union[Report, _Mapping]] = ...) -> None: ...

class ReportExportRequest(_message.Message):
    __slots__ = ("destination", "report")
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    REPORT_FIELD_NUMBER: _ClassVar[int]
    destination: str
    report: Report
    def __init__(self, destination: _Optional[str] = ..., report: _Optional[_Union[Report, _Mapping]] = ...) -> None: ...

class ReportExportReply(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: int
    def __init__(self, status: _Optional[int] = ...) -> None: ...
