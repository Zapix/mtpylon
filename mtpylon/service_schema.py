# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Any, List, Annotated, Union

from .utils import long, int128, int256
from .schema import Schema


@dataclass
class ResPQ:
    nonce: int128
    server_nonce: int128
    pq: bytes
    server_public_key_fingerprints: List[long]

    class Meta:
        name = 'resPQ'
        order = (
            'nonce',
            'server_nonce',
            'pq',
            'server_public_key_fingerprints'
        )


@dataclass
class PQInnerData:
    pq: bytes
    p: bytes
    q: bytes
    nonce: int128
    server_nonce: int128
    new_nonce: int256

    class Meta:
        name = 'p_q_inner_data'
        order = (
            'pq',
            'p',
            'q',
            'nonce',
            'server_nonce',
            'new_nonce'
        )


@dataclass
class PQInnerDataDC:
    pq: bytes
    p: bytes
    q: bytes
    nonce: int128
    server_nonce: int128
    new_nonce: int256
    dc: int

    class Meta:
        name = 'p_q_inner_data_dc'
        order = (
            'pq',
            'p',
            'q',
            'nonce',
            'server_nonce',
            'new_nonce',
            'dc'
        )


@dataclass
class PQInnerDataTemp:
    pq: bytes
    p: bytes
    q: bytes
    nonce: int128
    server_nonce: int128
    new_nonce: int256
    expires_in: int

    class Meta:
        name = 'p_q_inner_data_temp'
        order = (
            'pq',
            'p',
            'q',
            'nonce',
            'server_nonce',
            'new_nonce',
            'expires_in',
        )


@dataclass
class PQInnerDataTempDC:
    pq: bytes
    p: bytes
    q: bytes
    nonce: int128
    server_nonce: int128
    new_nonce: int256
    expires_in: int
    dc: int

    class Meta:
        name = 'p_q_inner_data_temp_dc'
        order = (
            'pq',
            'p',
            'q',
            'nonce',
            'server_nonce',
            'new_nonce',
            'dc',
            'expires_in',
        )


P_Q_inner_data = Annotated[
    Union[
        PQInnerData,
        PQInnerDataDC,
        PQInnerDataTemp,
        PQInnerDataTempDC,
    ],
    'P_Q_inner_data'
]


@dataclass
class ServerDHParamsFail:
    nonce: int128
    server_nonce: int128
    new_nonce_hash: int128

    class Meta:
        name = 'server_DH_params_fail'
        order = (
            'nonce',
            'server_nonce',
            'new_nonce_hash'
        )


@dataclass
class ServerDHParamsOk:
    nonce: int128
    server_nonce: int128
    encrypted_answer: bytes

    class Meta:
        name = 'server_DH_params_ok'
        order = (
            'nonce',
            'server_nonce',
            'encrypted_answer'
        )


Server_DH_Params = Annotated[
    Union[ServerDHParamsFail, ServerDHParamsOk],
    'Server_DH_Params'
]


@dataclass
class Server_DH_inner_data:
    nonce: int128
    server_nonce: int128
    g: int
    dh_prime: bytes
    g_a: bytes
    server_time: int

    class Meta:
        name = 'server_DH_inner_data'
        order = (
            'nonce',
            'server_nonce',
            'g',
            'dh_prime',
            'g_a',
            'server_time'
        )


@dataclass
class Client_DH_Inner_Data:
    nonce: int128
    server_nonce: int128
    retry_id: long
    g_b: bytes

    class Meta:
        name = 'client_DH_inner_data'
        order = (
            'nonce',
            'server_nonce',
            'retry_id',
            'g_b',
        )


@dataclass
class DHGenOk:
    nonce: int128
    server_nonce: int128
    new_nonce_hash1: int128

    class Meta:
        name = 'dh_gen_ok'
        order = (
            'nonce',
            'server_nonce',
            'new_nonce_hash1'
        )


@dataclass
class DHGenRetry:
    nonce: int128
    server_nonce: int128
    new_nonce_hash2: int128

    class Meta:
        name = 'dh_gen_retry'
        order = (
            'nonce',
            'server_nonce',
            'new_nonce_hash2'
        )


@dataclass
class DHGenFail:
    nonce: int128
    server_nonce: int128
    new_nonce_hash3: int128

    class Meta:
        name = 'dh_gen_fail'
        order = (
            'nonce',
            'server_nonce',
            'new_nonce_hash3'
        )


Set_client_DH_params_answer = Annotated[
    Union[
        DHGenOk,
        DHGenRetry,
        DHGenFail
    ],
    'Set_client_DH_params_answer'
]


@dataclass
class RpcResult:
    req_msg_id: long
    result: Any

    class Meta:
        name = 'rpc_result'
        order = ('req_msg_id', 'result')


@dataclass
class RpcError:
    error_code: int
    error_message: str

    class Meta:
        name = 'rpc_error'
        order = ('error_code', 'error_message')


@dataclass
class RpcAnswerUnknown:
    class Meta:
        name = 'rpc_answer_unknown'


@dataclass
class RpcAnswerDroppedRunning:
    class Meta:
        name = 'rpc_answer_dropped_running'


@dataclass
class RpcAnswerDropped:
    msg_id: long
    seq_no: int
    bytes: int

    class Meta:
        name = 'rpc_answer_dropped'
        order = ('msg_id', 'seq_no', 'bytes')


RpcDropAnswer = Annotated[
    Union[
        RpcAnswerUnknown,
        RpcAnswerDroppedRunning,
        RpcAnswerDropped,
    ],
    'RpcDropAnswer'
]


@dataclass
class FutureSalt:
    valid_since: int
    valid_until: int
    salt: long

    class Meta:
        name = 'future_salt'
        order = ('valid_since', 'valid_until', 'salt')


@dataclass
class FutureSalts:
    req_msg_id: long
    now: int
    salts: List[FutureSalt]

    class Meta:
        name = 'future_salts'
        order = ('req_msg_id', 'now', 'salts')


@dataclass
class Pong:
    msg_id: long
    ping_id: long

    class Meta:
        name = 'pong'
        order = ('msg_id', 'ping_id')


@dataclass
class NewSession:
    first_msg_id: long
    unique_id: long
    server_salt: long

    class Meta:
        name = 'new_session_created'
        order = (
            'first_msg_id',
            'unique_id',
            'server_salt',
        )


@dataclass
class Message:
    msg_id: long
    seqno: int
    bytes: int
    body: Any

    class Meta:
        name = 'message'
        order = (
            'msg_id',
            'seqno',
            'bytes',
            'body',
        )


@dataclass
class MessageContainer:
    messages: List[Message]

    class Meta:
        name = 'msg_container'
        order = ('messages',)


@dataclass
class MessageCopy:
    orig_message: Message

    class Meta:
        name = 'msg_copy'
        order = ('orig_message',)


@dataclass
class MsgsAck:
    msg_ids: List[long]

    class Meta:
        name = 'msgs_ack'
        order = ('msg_ids',)


@dataclass
class BadMessageNotification:
    bad_msg_id: long
    bad_msg_seqno: int
    error_code: int

    class Meta:
        name = 'bad_msg_notification'
        order = (
            'bad_msg_id',
            'bad_msg_seqno',
            'error_code',
        )


@dataclass
class BadServerSalt:
    bad_msg_id: long
    bad_msg_seqno: int
    error_code: int
    new_server_salt: long

    class Meta:
        name = 'bad_server_salt'
        order = (
            'bad_msg_id',
            'bad_msg_seqno',
            'error_code',
            'new_server_salt',
        )


BadMsgNotification = Annotated[
    Union[
        BadMessageNotification,
        BadServerSalt
    ],
    'BadMsgNotification'
]


@dataclass
class MessageResendReq:
    msg_ids: List[long]

    class Meta:
        name = 'msg_resend_req'
        order = ('msg_ids',)


@dataclass
class MessageResendAnsReq:
    msg_ids: List[long]

    class Meta:
        name = 'msg_resend_ans_req'
        order = ('msg_ids', )


MsgResendReq = Annotated[
    Union[
        MessageResendReq,
        MessageResendAnsReq
    ],
    'MsgResendReq'
]


@dataclass
class MsgsStateReq:
    msg_ids: List[long]

    class Meta:
        name = 'msgs_state_req'
        order = ('msg_ids', )


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
    ],
    functions=[]
)
