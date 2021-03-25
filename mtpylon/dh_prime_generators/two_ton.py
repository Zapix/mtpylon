# -*- coding: utf-8 -*-
from aiohttp import ClientSession

from .typing import DhPrimeGenerator

SAFE_PRIME_URL = "https://2ton.com.au/getprimes/random/2048/3"


async def generate() -> DhPrimeGenerator:
    """
    Get's 2048 dh prime number from open api(https://2ton.com.au/safeprimes/)
    Returns this value as integer
    """
    while True:
        async with ClientSession() as session:
            async with session.get(SAFE_PRIME_URL) as resp:
                data = await resp.json()

        yield int(data['p']['base10'])
