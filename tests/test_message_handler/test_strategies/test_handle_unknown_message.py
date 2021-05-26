# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from mtpylon import long
from mtpylon.messages import EncryptedMessage
from mtpylon.message_handler.strategies.handle_unknown_message import (
    handle_unknown_message
)


@pytest.mark.asyncio
async def test_handle_unknown_message():
    msg_id = long(0x51e57ac42770964a)

    message = EncryptedMessage(
        message_id=msg_id,
        session_id=long(1),
        salt=long(2),
        seq_no=0,
        message_data='Wrong message data'
    )

    request = MagicMock()
    sender = MagicMock(send_message=AsyncMock())
    logger = MagicMock()

    with patch(
        'mtpylon.message_handler.strategies.handle_unknown_message.logger',
        logger,
    ):
        await handle_unknown_message([], sender, request, message)

    logger.warning.assert_called()
    sender.send_message.assert_not_called()
