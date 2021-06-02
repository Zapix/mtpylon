# -*- coding: utf-8 -*-
import logging
from typing import cast, List, Any
from asyncio import create_task

from aiohttp.web import Request

from mtpylon.exceptions import RpcCallError
from mtpylon.contextvars import (
    income_message_var,
    server_salt_var,
    session_id_var,
)
from mtpylon.serialization import CallableFunc
from mtpylon.middlewares import apply_middleware, MiddleWareFunc, Handler
from mtpylon.message_sender import MessageSender
from mtpylon.utils import get_function_name
from mtpylon.service_schema.constructors import RpcError, RpcResult
from mtpylon.income_message import IncomeMessage

from .logging_adapter import MessageLoggerAdapter

logger = logging.getLogger()


def is_rpc_result(result: Any) -> bool:
    return isinstance(result, RpcResult)


async def run_rpc_query_middleware(
    handler: Handler,
    request: Request,
    **params: Any,
) -> Any:
    message = income_message_var.get()

    value = cast(CallableFunc, message.message_data)

    adapter = MessageLoggerAdapter(logger, {'message_id': message.message_id})

    func_name = get_function_name(value.func)

    adapter.info(f'Run rpc call {func_name}')

    try:
        result = await handler(request, **params)
    except RpcCallError as e:
        adapter.error(
            f'Rpc call has been failed with error: {e.error_message}'
        )
        result = RpcError(
            error_code=e.error_code,
            error_message=e.error_message
        )
    except Exception as e:
        adapter.error(f'Rpc call has been failed with unexpected error: {e}')
        result = RpcError(
            error_code=0,
            error_message=str(e)
        )
    else:
        adapter.info('Rpc call has been successfully finished')

    return RpcResult(
        req_msg_id=message.message_id,
        result=result
    )


async def run_rpc_query(
    middlewares: List[MiddleWareFunc],
    sender: MessageSender,
    request: Request,
    message: IncomeMessage,
):
    income_message_var.set(message)

    value = cast(CallableFunc, message.message_data)

    handler = apply_middleware(
        middlewares + [run_rpc_query_middleware],
        value.func
    )

    result = await handler(request, **value.params)

    server_salt = server_salt_var.get()
    session_id = session_id_var.get()

    await sender.send_encrypted_message(
        request,
        server_salt,
        session_id,
        result,
        response=True,
        acknowledgement_required=is_rpc_result(result)
    )


async def handle_rpc_query_message(
    middlewares: List[MiddleWareFunc],
    sender: MessageSender,
    request: Request,
    message: IncomeMessage
):
    create_task(run_rpc_query(middlewares, sender, request, message))
