# -*- coding: utf-8 -*-
from dataclasses import dataclass

import rsa  # type: ignore

from mtpylon import long
from mtpylon.crypto import KeyPair, RsaManager


@dataclass
class KeyData:
    public_str: str
    private_str: str
    fingerprint: long


key_data_list = [
    KeyData(  # 3072 private key works for enrypt/decrypt p_q_inner_data
        public_str='''
        -----BEGIN RSA PUBLIC KEY-----
        MIIBigKCAYEAv6sa90z70ttMO6EtJFUHS0iXlsQX/9vJYg9WQyNiMD3dE3FXAAbV
        BuEjDqcfHyk5PSPhph6ifFItEPhVTv2uH0S2OFLEjTNk+HpOhbCRDLY9OXbzq7xr
        0iNhuF4zRQaXeXGxHxVh9GtTrUNsEc0Q5szOoWutTdas3kg4nrcqsy0MN2zpQ2Yf
        6zksWJqR34vwCBTQttqwWFlqQg3q0N/JS0Y3CBAwj9oZTeJQNYy2Nn65cyalYXYN
        ccOVAgImqCSsmz5EBHLdxNPvr2fK2XC4ncHCK/EA5r5zdrxr8wWQK6jZdgpDEj5X
        JHeHc7YiVJAyzsdm/BbVYjzitid1BpJ0qxUFRxr005MVHbp3eRgd8H60F9aRZo2W
        jDy3o0zeNRNcsl5AjaSFb4i3tc/J7nXVOnFSs3eY+hKmQm77TvtqGgC6EOpIy8X0
        sH1nsCs9ni0J18RtUrJ6DF7xo2JfIfvOebDYeoY6CbUKOfo4QxyjtEcsztPIhrrk
        G6VvDPtGBajJAgMBAAE=
        -----END RSA PUBLIC KEY-----
        ''',
        private_str='''
        -----BEGIN RSA PRIVATE KEY-----
        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
        -----END RSA PRIVATE KEY-----
        ''',
        fingerprint=long(9495775286241702748)
    ),
    KeyData(
        public_str='''
        -----BEGIN RSA PUBLIC KEY-----
        MIIBigKCAYEA0hNWtBzAFaw7c7hambC8TRutayBY6FFd1UzIxzo+DI50UwyyQkgm
        kFkrXehN0quHIRHv4O1ZZA/8GxRMrlBGdkbSEVkhRkcolTlTain7HFKO6Fy2315I
        VI56pQ6rqfPSsQRAeIXkrJJmkHS8HeT0FFs5knnVUfLYErEkP1CWpOqJNLOIxrBO
        X0ToomzWcyIp+AxAps8Aa6lapYGVFbYKCqN9WnrHgQ/FdFVqWHlpI6g4pd/nNZba
        kqo/WsB0gmldBk46LUa3u7nuFpfDfqAItdy3JYZf/FEWO7QqgW3jlSjHgqNsYBYD
        RY2PARlo2+s6utAUxFmAX/xzp+W8EiWm9xTECbfEvm7HXwSWW+t5An3qptDv27fU
        Rop27Z70D10cksSm9dqc214RtQqFp7CkrrQFJv99j1/8JNC6aOdlokT0DXxCidXD
        +6DsJULu6N/mApILdXh6X6/0l9oNpBJXKw9crgZozNoV77f5X1OaBDzs3N+zAiNv
        Lu7ECZSeBJ8vAgMBAAE=
        -----END RSA PUBLIC KEY-----
        ''',
        private_str='''
        -----BEGIN RSA PRIVATE KEY-----
        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
        -----END RSA PRIVATE KEY-----
        ''',
        fingerprint=long(5685758434392400330),
    ),
    KeyData(
        public_str='''
        -----BEGIN RSA PUBLIC KEY-----
        MIIBCgKCAQEA1n37XUmUEXriQq4LHHfGWtNegqKlSs2k0Q90B7frahTVMdT+G2Hu
        QMDBHiMy0OuiG3RywNNQ6luJQ4IOwq7Z77BDugEWj2zlk05CnaW3wc2pvMHgm1YJ
        npPRxPGHowrd2RJk3DefezjvSIRRogNjpjz/Mdso+rJ2YKfRbCcgdOyqmPJqDOIs
        ozoZJMlDnwFg1nySA/rLAT7y8z/KtP80lpxs+cJw0ro/KvQ+qKhmq04efzuZ3zWs
        5bUnO+CnZD+a8Sdy8HsuZyRTcaLjkIJhArdWTm1HnriQsHBp+rBk22iWebn6a36p
        /IupQfYW8iRQYpj1ntOlSs4cFfJXEXBwRwIDAQAB
        -----END RSA PUBLIC KEY-----
        ''',
        private_str='''
        -----BEGIN RSA PRIVATE KEY-----
        MIIEowIBAAKCAQEA1n37XUmUEXriQq4LHHfGWtNegqKlSs2k0Q90B7frahTVMdT+
        G2HuQMDBHiMy0OuiG3RywNNQ6luJQ4IOwq7Z77BDugEWj2zlk05CnaW3wc2pvMHg
        m1YJnpPRxPGHowrd2RJk3DefezjvSIRRogNjpjz/Mdso+rJ2YKfRbCcgdOyqmPJq
        DOIsozoZJMlDnwFg1nySA/rLAT7y8z/KtP80lpxs+cJw0ro/KvQ+qKhmq04efzuZ
        3zWs5bUnO+CnZD+a8Sdy8HsuZyRTcaLjkIJhArdWTm1HnriQsHBp+rBk22iWebn6
        a36p/IupQfYW8iRQYpj1ntOlSs4cFfJXEXBwRwIDAQABAoIBAE6wW0ZHFw4uodFK
        noLsIhXyE2sjljZSKVQVMkEepTv+tpQYiryq+chBrteKnDrvJ0KhPvQk0juYJ0xf
        62Ba21NGvCICAi/OCI85F9FUGYz9EXdRPUBfmRnXKw7weQ1EkEzxpZTwxw5ivc5B
        1Nz2F1nGaOz2dRs725fsGTVvSUX7XMdRSq19KtbIdl/3ETLAtWr1qWajI5hf1cLe
        MMWItudAY3WG+6O2eidJp38Ix12b+kkN/4MNHx/85bKJj+q2MuF4YgV4TqUxgCUM
        fpwlmuaCfplAB8GUDpfSwysfjOcpAWs21YJMbevBIgjI9nc04DfmveOJwDcLEm1Y
        z9Fi3tECgYEA/X8X4yUfl1040OG5vfQGoIpQKaZz2fLhU1na2lvMEjGs33zj7TYt
        NHmLfmqaLO4t5ga/I3AVhnE4bc4tICfewZPbMlwyFEncC7feTMxLD+fskCl2Rl7X
        vCAomo/nwOpD7SltlcbvhQxHM95Y6e0N+zartFXGKdMcSy+uiUi3CM8CgYEA2JxG
        c3RaPm6ngAeL6ouJxIyqQiMmuj9cgQXBXSCMpNwMF1/8/FkIiLA9cFihB76EXL8j
        /FvjqM05Vs5Qk0vxoPJGsGFoalP3gQO1aLroZXjm5KRNp6d7NTlDvjDHV1MypWoQ
        GUnU6mVpYEEojNXyXFGI1EW5S1/k6KZYRwPzDwkCgYEAl3ps0cULPa3tF5TrI0FA
        /InqIRlgPSrPzrjw+G7GYVDh1qKQqN0o4iSHYMFe495n+v6pFQoTMsVRTPxZJs/s
        Yoxx/YPuQQVpwm7bHdUuPZD/YZ4FGUPvcnFdEg9QE41pjbylyUyZME4H9ky1oQOQ
        yT8AF8Dxq2iFjcAuccbL6S0CgYB/mIbTic2DC1G11DwyPGI6GpZMgUJV4e8OvaIq
        xnqyvkCNIGj5CUVCp3Z5kGvDERINRDbheAuCKunE3aGPMuQx56WGTsrgH3gjUljx
        SXCOHYr9Ul/AC6NDNelWxosWQJcL4496Jgi6zmQlZByL4ZdzlD/isvO0l9dSyHIl
        2wi5aQKBgC8ZdJhszTu/Qb71U6yRrCmlGfSnr/9JXckkEpetjF6u02TkBEho7nsV
        6SNseOuJTj1kdJ3b5+91UAFW/bYznnoDtkw/9uYwXKyC3QuosH3+cFeeb7hpo0CX
        gVetBNHrHzrubLs8GfT2erGwLJ1b31v/XjB1KeiMtThliNe6MCiD
        -----END RSA PRIVATE KEY-----
        ''',
        fingerprint=long(17442734222710702222)
    ),
    KeyData(
        public_str='''
        -----BEGIN RSA PUBLIC KEY-----
        MIGJAoGBAMsR/sjYV6p4r3HwpKX5OKyAJPrlbDoUMUGtxOsLJpubEEskft/eLoiP
        EPhfxFnslCHh5GzhNoEpOPQsu4ldyOwoRXUmq5WfmQZj390lAUeDXnEEgjZ6xl7H
        GHZlU0IMxG8ehM3MbaVoF9sy18UUbqyXaGaosKojAMljxEBg61wXAgMBAAE=
        -----END RSA PUBLIC KEY-----
        ''',
        private_str='''
        -----BEGIN RSA PRIVATE KEY-----
        MIICXgIBAAKBgQDLEf7I2FeqeK9x8KSl+TisgCT65Ww6FDFBrcTrCyabmxBLJH7f
        3i6IjxD4X8RZ7JQh4eRs4TaBKTj0LLuJXcjsKEV1JquVn5kGY9/dJQFHg15xBII2
        esZexxh2ZVNCDMRvHoTNzG2laBfbMtfFFG6sl2hmqLCqIwDJY8RAYOtcFwIDAQAB
        AoGBAKYmpSbEDIaIlFRPpwe98GcDuj4mtPSYTO0GNtZxmzc6GozA4aZd7gkBtcri
        4I8LCPDoGLQVWTk490ahyxfLynYpT36Lhdiy0mn7NCcyh5izAGEBObYAX7Loqwgh
        cN1H7jIJyf73zgFidbxVa1t71YbaZT7G3NIO8OIyN/M0A6OhAkEA8+wy3ZLyGyCD
        jw6jEnKtplAAg3MR6yE6QJQlxIKgptqaZrwSv9Fq0EcUbnUV5iBq6fvSYoP4I5y8
        +0J6WwXGXwJBANUf+q/3zQ8bZsydWVIlIkvtJPqTw1vbPzOjQdrMEo0rRneUvvl9
        aShwRv7cYgPlkzX+R+zcjUaiyPkFIe0AFUkCQQDhzPmZW/p7WjHvMGGNJlPR7aVM
        Ci3AOFYwifQcYcBONXdROzEwGLCEdghX6FOJYOEYEWHEiN4gOWxIPFYABOyJAkB4
        lVdpKHNFEOPg8UYQTCJTgyFhBSmLV0kzFjO0b7IvXUTJc8d5sZNF5gDFQjvSqJnZ
        +r0HLuJgDMpY2qaPSXTBAkEAtBxuXwq11AnLJ8vbOKIz9W2m1MocMnMu0P7LV60n
        gOUhc45umViwXE7v6StjhG1ykSl8q00KXon6wjiL42keQw==
        -----END RSA PRIVATE KEY-----
        ''',
        fingerprint=long(1984166525657425619)
    ),
    KeyData(
        public_str='''
        -----BEGIN RSA PUBLIC KEY-----
        MEgCQQCI0n6BN93gjdBy2TpT6bVlCocwtAktdJZIQkV8Wq6Mj6UrxsdTmdcMB1IO
        94eCnn9fiqu1vW0/TQ7znVCSGiOPAgMBAAE=
        -----END RSA PUBLIC KEY-----
        ''',
        private_str='''
        -----BEGIN RSA PRIVATE KEY-----
        MIIBOwIBAAJBAIjSfoE33eCN0HLZOlPptWUKhzC0CS10lkhCRXxaroyPpSvGx1OZ
        1wwHUg73h4Kef1+Kq7W9bT9NDvOdUJIaI48CAwEAAQJAd5NfNBdbNjE6h+UJcOTD
        v3agCBSQIMXPwX8Js1Cc1ujvsM7OT2k9PpXDDjmLTt9sMjojn7J3+RswhO+dnK+N
        gQIjAI8lQeYe8zgGNQuuH3YhDH+YltzliA0Kbg5JmuUmFUSX1D8CHwD0sQU/p8JM
        EU6/TacQA3/PUuvOHqjEMUfD5oW2nLECImGrHieRfon/UjpB+B11tz1oM6dMxWOA
        dk8xUYqATYqbvakCHl5bROLfFhWvNuaeUyXhs4+HMlcxi3LcbgglBLr+gQIiUKGF
        hIa7d4vHIPPflSd0GRsdJ8bmY0rJjB4qWXiav0xgHA==
        -----END RSA PRIVATE KEY-----
        ''',
        fingerprint=long(13923728974697425819)
    ),
    KeyData(
        public_str='''
        -----BEGIN RSA PUBLIC KEY-----
        MEgCQQC07rGil6ujqOwn2fbrHRbkjmUkg3kafl81F6NfmA4+GpZ058QnYzZVaH8F
        ISC4ZcggmJ+bnnFzZS5HXVnPS2ElAgMBAAE=
        -----END RSA PUBLIC KEY-----
        ''',
        private_str='''
        -----BEGIN RSA PRIVATE KEY-----
        MIIBPQIBAAJBALTusaKXq6Oo7CfZ9usdFuSOZSSDeRp+XzUXo1+YDj4alnTnxCdj
        NlVofwUhILhlyCCYn5uecXNlLkddWc9LYSUCAwEAAQJAb3PBdHidQBkkL4Aye63V
        lkCoyQ87oDhMCXZgKtiNGItqAWkVVpx8LyDC79o7nldmTVJXEeJ9idOCC3FGgLhc
        mQIjANe9GaNKQyH/bjTATpv1F6/3O5cmdqSwNxH1KoQvBA8EoCcCHwDWsrn3iuxi
        ucKqkuPcdzm0sN7sz63elUpLQHg1N9MCIwCkpvxENc9ayTnxJLxaJwq3D/f4+jAe
        rSa6m+ShEckFNUCNAh4iBxOoYzFR+GUdCcjpgU/5DmtWlxfUhk7PHHmw3ZcCIwDB
        j7pPPfkOdQmWybZxk19n3309S2Tf/OM411Da3S3m5Cix
        -----END RSA PRIVATE KEY-----
        ''',
        fingerprint=long(2244281079002705184)
    ),
    KeyData(
        public_str='''
        -----BEGIN RSA PUBLIC KEY-----
        MEgCQQCS2U07TIBID7KzsNc3pa1yCxnhvXG1uSluJE86HMAhjr8IXh7M3x3J3liE
        y/JeJgVdZQ8J+c7jm6HcFlc3fkjZAgMBAAE=
        -----END RSA PUBLIC KEY-----
        ''',
        private_str='''
        -----BEGIN RSA PRIVATE KEY-----
        MIIBPAIBAAJBAJLZTTtMgEgPsrOw1zelrXILGeG9cbW5KW4kTzocwCGOvwheHszf
        HcneWITL8l4mBV1lDwn5zuObodwWVzd+SNkCAwEAAQJAHQBbd12ZbCHligVfy7al
        tYMpvmJapagG3aDAINrynXGM5IvrIkBRzBVdnvogauu6FW1qoF7UdLZm++VYvDPZ
        nQIjAJVNHNvQilc53gvSLAo3E+IMm/yOcpFFTFb/0Ex0Vyg6kbsCHwD7y4Vhcg1g
        xkYXzGfh2izPQJokdnQa8cZ0KOR4jHsCIndDDP1uPUPmHsB0l+dlDcXxap05ML1o
        jM2mNT8NZB3ng0cCHwDF99szpV99Uga0GWMnwMjwXkOTHYrl0GgO1kPjv9cCIm6I
        v3q7L38lqQ7um1ycT7QY8Sh4SfX/HFdcTPe1dnDUhvE=
        -----END RSA PRIVATE KEY-----
        ''',
        fingerprint=long(5339281804123932840)
    )
]
key_pairs = [
    KeyPair(
        public=rsa.PublicKey.load_pkcs1(item.public_str),
        private=rsa.PrivateKey.load_pkcs1(item.private_str),
    )
    for item in key_data_list
]
manager = RsaManager(key_pairs)
