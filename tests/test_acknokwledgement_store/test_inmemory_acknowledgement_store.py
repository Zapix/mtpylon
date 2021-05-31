# -*- coding: utf-8 -*-
import pytest

from mtpylon.types import long
from mtpylon.acknowledgement_store import InmemoryAcknowledgementStore
from mtpylon.acknowledgement_store.types import AuthSessionHash
from mtpylon.crypto import AuthKey

from tests.echoschema import Reply

auth_key_data = 19173138450442901591212846731489158386637947003706705793697466005840359118325984130331040988945126053253996441948760332982664467588522441280332705742850565768210808401324268532424996018690635427668017180714026266980907736921933287244346526265760362799421836958089132713806536144155052702458589251084836839798895173633060038337086228492970997360899822298102887831495037141025890442863060204588167094562664112338589266018632963871940922732022252873979144345421549843044971414444544589457542139689588733663359139549339618779617218500603713731236381263744006515913607287705083142719869116507454233793160540351518647758028  # noqa


@pytest.fixture
def acknowledgement_store():
    return InmemoryAcknowledgementStore()


@pytest.fixture
def auth_key():
    return AuthKey(auth_key_data)


@pytest.fixture
def session_id():
    return long(11520911270507767959)


@pytest.mark.asyncio
async def test_create_session_store(
    acknowledgement_store,
    auth_key,
    session_id
):
    await acknowledgement_store.create_session_store(
        auth_key=auth_key,
        session_id=session_id
    )

    auth_session_hash = AuthSessionHash(
        auth_key=auth_key,
        session_id=session_id
    )

    assert auth_session_hash in acknowledgement_store._store


@pytest.mark.asyncio
async def test_set_message(acknowledgement_store, auth_key, session_id):
    msg_id = long(123123)
    data = Reply(
        rand_id=1,
        content='reply'
    )

    await acknowledgement_store.set_message(
        auth_key,
        session_id,
        msg_id,
        data
    )

    auth_session_hash = AuthSessionHash(
        auth_key=auth_key,
        session_id=session_id
    )

    assert auth_session_hash in acknowledgement_store._store
    assert msg_id in acknowledgement_store._store[auth_session_hash]
    assert acknowledgement_store._store[auth_session_hash][msg_id] == data


@pytest.mark.asyncio
async def test_get_message_list(acknowledgement_store, auth_key, session_id):
    msg_id = long(123120)
    data = Reply(
        rand_id=1,
        content='reply'
    )
    await acknowledgement_store.set_message(
        auth_key,
        session_id,
        msg_id,
        data
    )

    another_msg_id = long(123121)
    another_data = Reply(
        rand_id=2,
        content='another'
    )
    await acknowledgement_store.set_message(
        auth_key,
        session_id,
        another_msg_id,
        another_data
    )

    message_list = await acknowledgement_store.get_message_list(
        auth_key,
        session_id
    )

    assert len(message_list) == 2

    message_id_list = [item.message_id for item in message_list]
    assert msg_id in message_id_list
    assert another_msg_id in message_id_list


@pytest.mark.asyncio
async def test_delete_message(acknowledgement_store, auth_key, session_id):
    msg_id = long(123120)
    data = Reply(
        rand_id=1,
        content='reply'
    )
    await acknowledgement_store.set_message(
        auth_key,
        session_id,
        msg_id,
        data
    )

    another_msg_id = long(123121)
    another_data = Reply(
        rand_id=2,
        content='another'
    )
    await acknowledgement_store.set_message(
        auth_key,
        session_id,
        another_msg_id,
        another_data
    )

    await acknowledgement_store.delete_message(
        auth_key,
        session_id,
        msg_id
    )

    message_list = await acknowledgement_store.get_message_list(
        auth_key,
        session_id,
    )

    assert len(message_list) == 1


@pytest.mark.asyncio
async def test_drop_session(acknowledgement_store, auth_key, session_id):
    msg_id = long(123120)
    data = Reply(
        rand_id=1,
        content='reply'
    )
    await acknowledgement_store.set_message(
        auth_key,
        session_id,
        msg_id,
        data
    )

    another_msg_id = long(123121)
    another_data = Reply(
        rand_id=2,
        content='another'
    )
    await acknowledgement_store.set_message(
        auth_key,
        session_id,
        another_msg_id,
        another_data
    )

    await acknowledgement_store.drop_session_store(auth_key, session_id)

    auth_session_hash = AuthSessionHash(
        auth_key=auth_key,
        session_id=session_id
    )

    assert auth_session_hash not in acknowledgement_store._store

    message_list = await acknowledgement_store.get_message_list(
        auth_key,
        session_id
    )

    assert len(message_list) == 0
