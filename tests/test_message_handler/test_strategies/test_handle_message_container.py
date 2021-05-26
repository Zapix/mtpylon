# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from mtpylon.types import long
from mtpylon.messages import EncryptedMessage
from mtpylon.service_schema.constructors import (
    MessageContainer,
    Message,
    MsgsAck,
)
from mtpylon.serialization import CallableFunc
from mtpylon.message_handler.strategies.handle_message_container import (
    handle_message_container
)

from tests.simpleschema import set_task


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'message',
    [
        pytest.param(
            EncryptedMessage(
                message_id=long(0x51e57ac42770964a),
                session_id=long(1),
                salt=long(2),
                seq_no=0,
                message_data=MessageContainer(
                    messages=[
                        Message(
                            msg_id=long(0x5e0b700a00000000),
                            seqno=7,
                            bytes=20,
                            body=MsgsAck(
                                msg_ids=[
                                    long(1621416313)
                                ]
                            ),
                        ),
                        Message(
                            msg_id=long(0x60a4d9830000001c),
                            seqno=9,
                            bytes=16,
                            body=CallableFunc(
                                func=set_task,
                                params={'content': 'hello world'}
                            )
                        ),
                    ]

                )
            ),
            id='message container',
        )
    ],
)
async def test_handle_message_container(message):
    strategy_selector = MagicMock(return_value=AsyncMock())

    create_task = MagicMock()

    sender = MagicMock()
    request = MagicMock()

    with patch(
        'mtpylon.message_handler.strategies.handle_message_container.create_task',  # noqa
        create_task
    ):
        await handle_message_container(
            strategy_selector,
            [],
            sender,
            request,
            message
        )
        assert strategy_selector.called
        assert strategy_selector.call_count == 2

        assert create_task.called
        assert create_task.call_count == 2
