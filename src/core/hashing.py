import asyncio
import hashlib


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

async def async_sha256(data: bytes) -> str:
    return await asyncio.to_thread(sha256, data)