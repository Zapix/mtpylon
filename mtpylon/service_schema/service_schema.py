# -*- coding: utf-8 -*-
from mtpylon import Schema
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
from .functions import (
    req_pq,
    req_pq_multi,
    req_DH_params,
    set_client_DH_params,
    rpc_drop_answer,
    get_future_salts,
    ping,
    ping_delay_disconnect,
    destroy_auth_key,
    destroy_session
)

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
        ping_delay_disconnect,
        destroy_auth_key,
        destroy_session
    ]
)
