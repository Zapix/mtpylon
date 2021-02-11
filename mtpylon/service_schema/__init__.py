# -*- coding: utf-8 -*-
from ..schema import Schema
from .constructors import (
    ResPQ,
    P_Q_inner_data,
    Server_DH_Params,
    Server_DH_inner_data,
    Client_DH_Inner_Data,
    Set_client_DH_params_answer,
    RpcResult,
    RpcError,
    RpcDropAnswer,
    FutureSalt,
    FutureSalts,
    Pong,
    NewSession,
    Message,
    MessageContainer,
    MessageCopy,
    MsgsAck,
    BadMsgNotification,
    MsgResendReq,
    MsgsStateReq,
    MsgsStateInfo,
    MsgsAllInfo,
    MsgDetailedInfo,
    BindAuthKeyInner,
    DestroyAuthKeyRes,
    DestroySessionRes
)
from .req_pq import req_pq
from .req_pq_multi import req_pq_multi
from .req_DH_params import req_DH_params
from .set_client_DH_params import set_client_DH_params
from .rpc_drop_answer import rpc_drop_answer
from .get_future_salts import get_future_salts
from .ping import ping

service_schema = Schema(
    constructors=[
        ResPQ,
        P_Q_inner_data,
        Server_DH_Params,
        Server_DH_inner_data,
        Client_DH_Inner_Data,
        Set_client_DH_params_answer,
        RpcResult,
        RpcError,
        RpcDropAnswer,
        FutureSalt,
        FutureSalts,
        Pong,
        NewSession,
        Message,
        MessageContainer,
        MessageCopy,
        MsgsAck,
        BadMsgNotification,
        MsgResendReq,
        MsgsStateReq,
        MsgsStateInfo,
        MsgsAllInfo,
        MsgDetailedInfo,
        BindAuthKeyInner,
        DestroyAuthKeyRes,
        DestroySessionRes,
    ],
    functions=[
        req_pq,
        req_pq_multi,
        req_DH_params,
        set_client_DH_params,
        rpc_drop_answer,
        get_future_salts,
        ping,
    ]
)
