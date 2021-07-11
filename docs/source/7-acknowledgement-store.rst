.. _mtpylon_acknowledgement_store:


Acknowledgement Store
=====================

To store messages that hasn't received acknowledgement from user we need
place where to store it. AcknowledgementStore is a place for it.
For now mtpylon store it in-memory. Developer could implement it's
own acknowledgement store by implementing protocol:
`mtpylon.acknowledgement_store.acknowledgement_store_protocol.AcknowledgementStoreProtocol`

.. code-block:: python

  class AcknowledgementStoreProtocol(Protocol):
      """
      Protocol to store messages that should be confirmed by acknowledgement.
      """

      async def set_message(
          self,
          auth_key: AuthKey,
          session_id: long,
          message_id: long,
          data: Any
      ):  # pragma: nocover
          """
          Sets message data that should be confirmed by acknowledgement
          """
          ...

      async def get_message_list(
          self,
          auth_key: AuthKey,
          session_id: long,
      ) -> List[AcknowledgementMessage]:  # pragma: nocover
          """
          Gets list of messages that haven't received acknowledgement yet
          """
          ...

      async def delete_message(
          self,
          auth_key: AuthKey,
          session_id: long,
          message_id: long
      ):  # pragma: nocover
          """
          Remove message by message_id from acknowledgement list for connection
          :return:
          """
          ...

      async def create_session_store(
          self,
          auth_key: AuthKey,
          session_id: long
      ):  # pragma: nocover
          """
          Creates store for message acknowledgement for current session
          """

      async def drop_session_store(
          self,
          auth_key: AuthKey,
          session_id: long
      ):  # pragma: nocover
          """
          Drops whole waiting acknowledgement list for dropped session
          """
          ...
