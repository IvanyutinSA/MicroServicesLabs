# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import transaction_service_pb2 as transaction__service__pb2

GRPC_GENERATED_VERSION = '1.73.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in transaction_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TransactionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TransactionAdd = channel.unary_unary(
                '/TransactionService/TransactionAdd',
                request_serializer=transaction__service__pb2.TransactionAddRequest.SerializeToString,
                response_deserializer=transaction__service__pb2.TransactionAddReply.FromString,
                _registered_method=True)
        self.TransactionGet = channel.unary_unary(
                '/TransactionService/TransactionGet',
                request_serializer=transaction__service__pb2.TransactionGetRequest.SerializeToString,
                response_deserializer=transaction__service__pb2.TransactionGetReply.FromString,
                _registered_method=True)


class TransactionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def TransactionAdd(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TransactionGet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TransactionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'TransactionAdd': grpc.unary_unary_rpc_method_handler(
                    servicer.TransactionAdd,
                    request_deserializer=transaction__service__pb2.TransactionAddRequest.FromString,
                    response_serializer=transaction__service__pb2.TransactionAddReply.SerializeToString,
            ),
            'TransactionGet': grpc.unary_unary_rpc_method_handler(
                    servicer.TransactionGet,
                    request_deserializer=transaction__service__pb2.TransactionGetRequest.FromString,
                    response_serializer=transaction__service__pb2.TransactionGetReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'TransactionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('TransactionService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TransactionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def TransactionAdd(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TransactionService/TransactionAdd',
            transaction__service__pb2.TransactionAddRequest.SerializeToString,
            transaction__service__pb2.TransactionAddReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def TransactionGet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TransactionService/TransactionGet',
            transaction__service__pb2.TransactionGetRequest.SerializeToString,
            transaction__service__pb2.TransactionGetReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
