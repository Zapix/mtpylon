RSA Key Manager
===============

RSA Key Manager is a object that stores info about rsa public/private keys and
their fingerprints that will be used in auth key exchanges.

.. _rsa_fingerprint:

**fingerprint** - is a 8 lower bytes of sha1 hash of rsa public key. `n` and `e`
values represent as tl byte string in big endian format

RSA Key Manager allows to check has we got rsa key pair for fingerprint or not.
Allows to get that pair if it exists. RSA Key Manager could get list of available
public rsa keys as python `bytes`. Also It returns list of available fingerprints


.. _RsaManager_implementation:

MTPylon has got simple RSA Key Manager implementation example of usage:

.. code-block:: python

  from mtpylon.crypto import RsaManager, KeyPair

  rsa_manager = RsaManager([
      KeyPair(
          public='''
          -----BEGIN RSA PUBLIC KEY-----
          -----END RSA PUBLIC KEY-----
          ''',
          private='''
          -----BEGIN RSA PRIVATE KEY-----
          -----END RSA PRIVATE KEY-----
          '''
      ),
      KeyPair(
          public='''
          -----BEGIN RSA PUBLIC KEY-----
          -----END RSA PUBLIC KEY-----
          ''',
          private='''
          -----BEGIN RSA PRIVATE KEY-----
          -----END RSA PRIVATE KEY-----
          '''
      ),
      KeyPair(
          public='''
          -----BEGIN RSA PUBLIC KEY-----
          -----END RSA PUBLIC KEY-----
          ''',
          private='''
          -----BEGIN RSA PRIVATE KEY-----
          -----END RSA PRIVATE KEY-----
          '''
      ),
  ])

  5339281804123932840 in rsa_manager  # checks has rsa manager this fingerprint

  rsa_manager[5339281804123932840]  # returns key pair by fingerprint


  rsa_manager.public_key_list  # list of public rsa keys

  rsa_manager.fingerprint_list  # list of available rsa keys


.. _Rsa_Manager_Protocol:

You could implement and use your custom rsa manager by implementing protocol
`mtpylon.crypto.rsa_manager.RasManagerProtocol`


.. code-block:: python

  class RsaManagerProtocol(Protocol):

      def __contains__(self, item: int) -> bool:  # pragma: no cover
          ...

      def __getitem__(self, item: int) -> KeyPair:  # pragma: no cover
          ...

      @property
      def public_key_list(self) -> List[bytes]:  # pragma: no cover
          ...

      @property
      def fingerprint_list(self) -> List[int]:  # pragma: no cover
          ...
