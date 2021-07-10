.. _mtpylon_server_salt_manager:

Server salt manager
==================

Server salt manager is a manager that stores info about available server salt
for auth key. Server salts used to prevent "replay-attacks". Server salts
changes periodically and generates from server. Client could ask
several future server salts, or receive current server salt with
`BadServerSalt` message. Methods to work with server salt manager:

 * `has_salt(auth_key: AuthKey, salt_value: long)` - checks can current
   be used or not

 * `set_salt(auth_key: AuthKey, salt: Salt)`  - sets server salt for auth key

 * `ge_future_salts(auth_key: AuthKey, count: int)` - gets or generates several
   future salts for auth_key

 * `clear(auth_key)` - clear outdates server satls for current passed auth_key



Server salt used as shared resource to check middleware.

If customer wants to implement his own server salt manager - he need implement
`mtpylon.salts.server_salt_manager_protocol.ServerSaltManagerProtocol`


.. code-block:: python

  class ServerSaltManagerProtocol(Protocol):

      async def has_salt(
          self,
          auth_key: AuthKey,
          salt_value: long
      ) -> bool:  # pragma: nocover
          """
          Checks can current salt be used now or not.
          """
          ...

      async def set_salt(
              self,
              auth_key: AuthKey,
              salt: Salt
      ):  # pragma: nocover
          """
          Sets server salt for auth key
          """
          ...

      async def get_future_salts(
          self,
          auth_key: AuthKey,
          count: int = 1
      ) -> List[Salt]:  # pragma: nocover
          """
          Get or generate future salts for current authorization key .
          Maximum future salts that could be return is 64

          Raises:
              ValueError - if negative or more then 64 values should be returned
          """
          ...

      async def clear(
          self,
          auth_key: Optional[AuthKey] = None
      ):  # pragma: nocover
          """
          Clear all outdated server salts
          :param auth_key:
          :return:
          """
          ...
