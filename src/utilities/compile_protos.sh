#!/bin/bash

python -m grpc_tools.protoc -I./protobuff --python_out=./protos --pyi_out=./protos --grpc_python_out=./protos ./protobuff/*
