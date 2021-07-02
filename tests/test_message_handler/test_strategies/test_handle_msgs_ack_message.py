# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, AsyncMock

import pytest

from mtpylon.types import long
from mtpylon.constants import ACKNOWLEDGEMENT_STORE_RESOURCE_NAME
from mtpylon.messages import EncryptedMessage
from mtpylon.service_schema.constructors import MsgsAck
from mtpylon.message_handler.strategies.handle_msgs_ack_message import (
    handle_msgs_ack
)
from mtpylon.contextvars import auth_key_var, session_id_var
from mtpylon.crypto import AuthKey


msg_id = long(0x51e57ac42770964a)
server_salt = long(16009147158398906513)
session_id = long(11520911270507767959)

auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa
auth_key = AuthKey(auth_key_data)


@pytest.mark.parametrize(
    'message',
    [
        pytest.param(
            EncryptedMessage(
                message_id=msg_id,
                session_id=session_id,
                salt=server_salt,
                seq_no=0,
                message_data=MsgsAck(
                    msg_ids=[
                        long(0x51e57ac42770964a),
                        long(0x60a4d9830000001c),
                    ],
                ),
            ),
            id='msgs ack'
        ),
    ]
)
@pytest.mark.asyncio
async def tests_handle_msgs_ack(message):
    auth_key_var.set(auth_key)
    session_id_var.set(session_id)

    middlewares = []
    sender = MagicMock()

    acknowledgement_store = MagicMock(
        delete_message=AsyncMock()
    )

    request = MagicMock()
    request.app = {
        ACKNOWLEDGEMENT_STORE_RESOURCE_NAME: acknowledgement_store
    }

    await handle_msgs_ack(
        middlewares,
        sender,
        request,
        message
    )

    acknowledgement_store.delete_message.assert_called()
    assert acknowledgement_store.delete_message.call_count == 2
