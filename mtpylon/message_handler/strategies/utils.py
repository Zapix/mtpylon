# -*- coding: utf-8 -*-
from mtpylon.messages import (
    UnencryptedMessage,
    EncryptedMessage
)
from mtpylon.serialization import CallableFunc
from mtpylon.service_schema import service_schema
from mtpylon.service_schema.functions import (
    req_pq,
    req_pq_multi,
    req_DH_params,
    set_client_DH_params
)
from mtpylon.service_schema.constructors import (
    MessageContainer,
    Message,
    MsgsAck
)
from mtpylon.income_message import IncomeMessage


ALLOWED_UNENCRYPTED_RPC_CALLS = [
    req_pq,
    req_pq_multi,
    req_DH_params,
    set_client_DH_params,
]


def is_unencrypted_message(message: IncomeMessage) -> bool:
    """
    :param message:
    :return:
    """
    if not isinstance(message, UnencryptedMessage):
        return False

    if not isinstance(message.message_data, CallableFunc):
        return False

    func = message.message_data.func

    return func in ALLOWED_UNENCRYPTED_RPC_CALLS


def is_rpc_call_message(message: IncomeMessage) -> bool:
    if not (
        isinstance(message, EncryptedMessage) or
        isinstance(message, Message)
    ):
        return False

    if not isinstance(message.message_data, CallableFunc):
        return False

    func = message.message_data.func

    return func not in service_schema


def is_container_message(message: IncomeMessage) -> bool:
    if not isinstance(message, EncryptedMessage):
        return False

    return isinstance(message.message_data, MessageContainer)


def is_msgs_ack(message: IncomeMessage) -> bool:
    if isinstance(message, UnencryptedMessage):
        return False

    return isinstance(message.message_data, MsgsAck)
