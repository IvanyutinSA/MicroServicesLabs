import asyncio

import grpc
import graphene

from src.middleware.jwt_controller import JWTController

from src.transaction_service.server import transactions_db

import src.user_service.protos.user_service_pb2_grpc as user_service_pb2_grpc
import src.user_service.protos.user_service_pb2 as user_service_pb2

import src.transaction_service.protos.transaction_service_pb2 as transaction_service_pb2
import src.transaction_service.protos.transaction_service_pb2_grpc as transaction_service_pb2_grpc

from src.user_service.server import users

jwt_controller = JWTController()


class User(graphene.ObjectType):
    username = graphene.String()
    role = graphene.String()


class Transaction(graphene.ObjectType):
    owner_name = graphene.String()
    transaction_name = graphene.String()
    amount = graphene.Int()
    date = graphene.String()


class TransactionInput(graphene.InputObjectType):
    owner_name = graphene.String(required=True)
    transaction_name = graphene.String(required=True)
    amount = graphene.Int(required=True)
    date = graphene.String(required=True)


class AddTransaction(graphene.Mutation):
    class Arguments:
        transaction = TransactionInput(required=True)

    status = graphene.Int()

    def mutate(root, info, transaction):
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)

            transaction = transaction_service_pb2.Transaction(
                    owner_name=transaction.owner_name,
                    transaction_name=transaction.transaction_name,
                    amount=transaction.amount,
                    date=transaction.date)
            request = transaction_service_pb2.TransactionAddRequest(
                    transaction=transaction)
            reply = stub.TransactionAdd(request)
            return AddTransaction(status=reply.status)


class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        role = graphene.String(required=True)

    status = graphene.Int(required=True)

    def mutate(root, info, username, password, role):
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)

            request = user_service_pb2.RegisterRequest(
                    user_name=username,
                    password=password,
                    role=role)
            reply = stub.Register(request)

            return RegisterUser(status=reply.status)


class Mutation(graphene.ObjectType):
    add_transaction = AddTransaction.Field()
    register = RegisterUser.Field()


class Subscription(graphene.ObjectType):
    transaction_added = graphene.String()

    async def subscribe_transaction_added(root, info):
        transactions_len = len(transactions_db)
        for i in range(5):
            diff = len(transactions_db) - transactions_len
            transactions_len = len(transactions_db)
            for j in range(1, diff+1):
                yield transactions_db[-j]['transaction_name']
            await asyncio.sleep(6)


class Query(graphene.ObjectType):
    user = graphene.Field(User, username=graphene.String(required=True))
    transactions = graphene.Field(
            graphene.List(Transaction, required=True),
            owner_name=graphene.String(required=True),
            start_date=graphene.String(required=True),
            end_date=graphene.String(required=True))

    def resolve_user(root, info, username):
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)

            request = user_service_pb2.UserGetInformationRequest(
                    user_name=username)
            reply = stub.UserGetInformation(request)

            if reply.status:
                return None

            return User(username=reply.user_name, role=reply.role)

    def resolve_transactions(root, info, owner_name, start_date, end_date):
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)

            request = transaction_service_pb2.TransactionGetRequest(
                    owner_name=owner_name,
                    start_date=start_date,
                    end_date=end_date)
            reply = stub.TransactionGet(request)
            if reply.status:
                return []
            transactions = [Transaction(owner_name=transaction.owner_name,
                                        transaction_name=transaction.transaction_name,
                                        amount=transaction.amount,
                                        date=transaction.date)
                            for transaction in reply.transactions]
            return transactions


def build_schema():
    schema = graphene.Schema(Query,
                             mutation=Mutation,
                             subscription=Subscription)
    return schema
