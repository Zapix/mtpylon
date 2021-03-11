AuthKey and AuthKeyManager
==========================



.. _auth_key:

AuthKey
-------

After creating authorization key we will get big `auth_key` number. For more details
please check `definition here <https://core.telegram.org/mtproto/description#authorization-key-auth-key>`
that will be used for encrypting/decrypting messages between client and server.
In mtpylon special class used to simplify work with `auth_key` number `AuthClass`

`AuthKey` stores key number in `value` attribute and has got several properties:

 - `hash` - sha1 hash of auth key as integer

 - `id` - auth key id as 64 lower bits of auth key hash. please check `definition here<https://core.telegram.org/mtproto/description#key-identifier-auth-key-id>`

 - `aux_hash` - aux hash as 64 higher bits of auth key hash please check `definition here<https://core.telegram.org/mtproto/auth_key#dh-key-exchange-complete>`


.. _auth_key_manager:

AuthKeyManager
--------------

AuthKeyManager is a manager that stores authorization keys.
By default auth keys stores in memory but to manager them you'll use
coroutines. Methods to work with auth key manager:

- `set_key(self, value: Union[AuthKey, int])` - coroutine to set authorization key
  accepts auth_key as instance of `AuthKey` class or as 2048-bit interger

- `has_key(self, value: Union[AuthKey, int])` - coroutine to check does
  manager know about `auth_key` by `auth_key_id` or not. Accepts
  instance of `AuthKey` class or integer value as `auth_key_id`

- `get_key(self, value: int)` - coroutine to get instance of `AuthKey` by
  `auth_key_id`. Accepts only integer value. Raises `AuthKeyDoesNotExist`
  exception if `auth_key_id` not found in manager

- `del_key(self, value: Union[AuthKey, int])` - coroutine to delete information
  about authorization key. Accepts instance of `AuthKey` or integer as
  `auth_key_id`. Raises `AuthKeyDoesNotExist`
  exception if `auth_key_id` not found in manager


Example of usage:


.. code-block:: python

    from mtpylon.crypto import AuthKey, AuthKeyManager

    auth_key = 0x32234234 # 2048-bit integer value
    auth_hash = 0x189e4dd9d40b7e7b5c160c4b0313e843b05b5983 # sha1 of auth_key
    auth_key_id = 0x0313e843b05b5983  # 64 lower bits of auth_hash
    auth_aux_hash = 0x189e4dd9d40b7e7b  # 64 higher bits of auth_hash

    manager = AuthKeyManager()
    manager.set_key(auth_key)

    auth_key_data = await manager.get_key(auth_key_id)

    assert auth_key_data.id == auth_key_id
    assert auth_key_data.value == auth_key
    assert auth_key_data.hash == auth_hash
    assert auth_key_data.aux_hash == auth_aux_hash




.. _auth_key_manger_protocol:

AuthKeyManagerProtocol
----------------------

Probably you want to store auth_key not in memory but in redis store or other
key value store. To create you own auth manager you should just implements
their protocol:


.. code-block:: python


    class AuthKeyManagerProtocol(Protocol):

        async def set_key(self, value: Union[AuthKey, int]):  # pragma: nocover
            """
            Sets new available authentication key. This method
            takes instance of AuthKey class or auth_key as integer
            It'll be async function coz we could use separated service to store
            authorization keys
            """
            ...

        async def has_key(
                self,
                value: Union[AuthKey, int]
        ) -> bool:  # pragma: nocover
            """
            Checks is this AuthKey store in manager or not. This method
            takes intance of AuthKey class or integer as auth_key_id.
            It'll be async function coz we could use separated service to store
            authorization keys
            """
            ...

        async def get_key(self, value: int) -> AuthKey:  # pragma: nocover
            """
            Gets auth key data by its id.
            It'll be async function coz we could separated service to store
            authorization keys

            Raises: AuthKeyDoesNotExist if key doesn't store in manager
            """
            ...

        async def del_key(self, value: Union[AuthKey, int]):
            """
            Delete auth key from manager by it's id, value or AuthKey instance
            It'll be async function coz we could use separated service to store
            authorization keys

            Raises:  AuthKeyDoesNotExist if key doesn't store in manager
            """
