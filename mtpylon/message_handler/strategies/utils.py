# -*- coding: utf-8 -*-
from mtpylon.messages import MtprotoMessage, UnencryptedMessage, Message
from mtpylon.serialization import CallableFunc
from mtpylon.service_schema import service_schema
from mtpylon.service_schema.functions import (
    req_pq,
    req_pq_multi,
    req_DH_params,
    set_client_DH_params
)


ALLOWED_UNENCRYPTED_RPC_CALLS = [
    req_pq,
    req_pq_multi,
    req_DH_params,
    set_client_DH_params,
]


def is_unencrypted_message(message: MtprotoMessage) -> bool:
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


def is_rpc_call_message(message: MtprotoMessage) -> bool:
    if not isinstance(message, Message):
        return False

    if not isinstance(message.message_data, CallableFunc):
        return False

    func = message.message_data.func

    return func not in service_schema
