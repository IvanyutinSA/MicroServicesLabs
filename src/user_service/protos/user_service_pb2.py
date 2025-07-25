# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: user_service.proto
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
    'user_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12user_service.proto\"6\n\x0fRegisterRequest\x12\x11\n\tuser_name\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1f\n\rRegisterReply\x12\x0e\n\x06status\x18\x01 \x01(\x05\":\n\x13\x41uthenticateRequest\x12\x11\n\tuser_name\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"#\n\x11\x41uthenticateReply\x12\x0e\n\x06status\x18\x01 \x01(\x05\",\n\x19GetUserInformationRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"<\n\x17GetUserInformationReply\x12\x0e\n\x06status\x18\x01 \x01(\x05\x12\x11\n\tuser_name\x18\x02 \x01(\t2\xc7\x01\n\x0bUserService\x12.\n\x08Register\x12\x10.RegisterRequest\x1a\x0e.RegisterReply\"\x00\x12:\n\x0c\x41uthenticate\x12\x14.AuthenticateRequest\x1a\x12.AuthenticateReply\"\x00\x12L\n\x12GetUserInformation\x12\x1a.GetUserInformationRequest\x1a\x18.GetUserInformationReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REGISTERREQUEST']._serialized_start=22
  _globals['_REGISTERREQUEST']._serialized_end=76
  _globals['_REGISTERREPLY']._serialized_start=78
  _globals['_REGISTERREPLY']._serialized_end=109
  _globals['_AUTHENTICATEREQUEST']._serialized_start=111
  _globals['_AUTHENTICATEREQUEST']._serialized_end=169
  _globals['_AUTHENTICATEREPLY']._serialized_start=171
  _globals['_AUTHENTICATEREPLY']._serialized_end=206
  _globals['_GETUSERINFORMATIONREQUEST']._serialized_start=208
  _globals['_GETUSERINFORMATIONREQUEST']._serialized_end=252
  _globals['_GETUSERINFORMATIONREPLY']._serialized_start=254
  _globals['_GETUSERINFORMATIONREPLY']._serialized_end=314
  _globals['_USERSERVICE']._serialized_start=317
  _globals['_USERSERVICE']._serialized_end=516
# @@protoc_insertion_point(module_scope)
