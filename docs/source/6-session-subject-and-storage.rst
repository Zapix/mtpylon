.. _mtpylon_session_subject_and_storage:

Session Subject and Storage
===========================


Session storage is a place where we keep created and registered `session_id`s.
`session id` is a long value that generate by client. More info about session
in `Mtproto Sesssion <https://core.telegram.org/mtproto/description#session>`_


Mtpylon allows to store and observe existing session. Also customer
could create it's own session observer that requires for them

.. _mtpylon_session_storage:

Session Storage
---------------

Session storage is a place where we store info about existing clients sessions.
Session storage has serveral methods that helps to work with sessions:

 * `create_session(session_id: long)`  - creates current session
 * `has_session(session_id: long)` - returns has we got current session or not
 * `destroy_session(session_id: long)` - destroys current session

To create own storage developer should implement
`mtpylon.sessions.session_storage_protocol.SessionStorageProtocol`:

.. code-block:: python

  class SessionStorageProtocol(Protocol):

      async def create_session(self, session_id: long):  # pragma: nocover
          """
          Saves info about new session(session_id)
          """
          ...

      async def has_session(self, session_id: long) -> bool:  # pragma: nocover
          """
          Checks has session_id been stored or not
          """
          ...

      async def destroy_session(self, session_id: long):  # pragma: nocover
          """
          Removes info about stored
          """
          ...

.. _mtpylon_session_subject:

Session Subject
---------------

Mtpylon use session storage as state of session subject. session subject -
is an instance that allows to communicate with different parts of application
and inform is session has been created or destroyed.

session subject available methods:

 * `subscribe(observer: SessionObserverProtocol)` - subscribe observer to
   receive :ref:`mtpylon_session_events`

 * `unsubscribe(observer: SessionObserverProtocol)` - unsubscribe observer from
   session subject

 * `create_session(session_id: long)` - creates session in session storage
   and notify session observers that new session has been created

 * `has_session(session_id: long)` - checks has session in storage or not

 * `destroy_session(session_id: long)` - destroy session in storage and notify
   all observers about destroyed session


.. _mtpylon_session_events:

Session events
--------------

Observers could be notified about created or destroyed sessions with
`mtpylon.sessions.session_event.SessionEvent`

Session event is an object with params:

 * `type` - type of event. Could be `created` or `destroyed`

 * `session_id` - number of session that has been created or destroyed


.. _mtpylon_session_observer:

Session Observer
----------------

To create different resources that could interact with session data we need
to implement session observer protocol:
`mtpylon.sessions.session_observer_protocol.SessionObserverProtocol`

.. code-block:: python

  class SessionObserverProtocol:

      async def update(self, event: SessionEvent):  # pragma: nocover
          ...

