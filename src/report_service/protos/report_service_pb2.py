# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: report_service.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'report_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14report_service.proto\"Z\n\x0cRTransaction\x12\x12\n\nowner_name\x18\x01 \x01(\t\x12\x18\n\x10transaction_name\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x01\x12\x0c\n\x04\x64\x61te\x18\x04 \x01(\t\"]\n\x06Report\x12#\n\x0ctransactions\x18\x01 \x03(\x0b\x32\r.RTransaction\x12\x14\n\x0ctotal_income\x18\x02 \x01(\x01\x12\x18\n\x10total_operations\x18\x03 \x01(\x05\"<\n\x15ReportGenerateRequest\x12#\n\x0ctransactions\x18\x01 \x03(\x0b\x32\r.RTransaction\"N\n\x13ReportGenerateReply\x12\x0e\n\x06status\x18\x01 \x01(\x05\x12\x1c\n\x06report\x18\x02 \x01(\x0b\x32\x07.ReportH\x00\x88\x01\x01\x42\t\n\x07_report\".\n\x13ReportExportRequest\x12\x17\n\x06report\x18\x01 \x01(\x0b\x32\x07.Report\"M\n\x11ReportExportReply\x12\x0e\n\x06status\x18\x01 \x01(\x05\x12\x18\n\x0breport_name\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x0e\n\x0c_report_name2\x8d\x01\n\rReportService\x12@\n\x0eReportGenerate\x12\x16.ReportGenerateRequest\x1a\x14.ReportGenerateReply\"\x00\x12:\n\x0cReportExport\x12\x14.ReportExportRequest\x1a\x12.ReportExportReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'report_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_RTRANSACTION']._serialized_start=24
  _globals['_RTRANSACTION']._serialized_end=114
  _globals['_REPORT']._serialized_start=116
  _globals['_REPORT']._serialized_end=209
  _globals['_REPORTGENERATEREQUEST']._serialized_start=211
  _globals['_REPORTGENERATEREQUEST']._serialized_end=271
  _globals['_REPORTGENERATEREPLY']._serialized_start=273
  _globals['_REPORTGENERATEREPLY']._serialized_end=351
  _globals['_REPORTEXPORTREQUEST']._serialized_start=353
  _globals['_REPORTEXPORTREQUEST']._serialized_end=399
  _globals['_REPORTEXPORTREPLY']._serialized_start=401
  _globals['_REPORTEXPORTREPLY']._serialized_end=478
  _globals['_REPORTSERVICE']._serialized_start=481
  _globals['_REPORTSERVICE']._serialized_end=622
# @@protoc_insertion_point(module_scope)
