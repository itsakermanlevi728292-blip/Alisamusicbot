import time
from typing import Dict, Any, Optional

# In-memory dictionary to store cached data with expiration timestamps
_CACHE: Dict[str, Dict[str, Any]] = {}


async def get_cache(key: str) -> Optional[Any]:
    """
    Retrieve cached value by key if it exists and has not expired.
    """
    if key in _CACHE:
        item = _CACHE[key]
        if item["ttl"] is None or item["ttl"] > time.time():
            return item["data"]
        else:
            # Remove expired key
            del _CACHE[key]
    return None


async def save_cache(key: str, data: Any, ttl: int = 3600) -> None:
    """
    Save value to cache with a Time-To-Live (TTL) in seconds.
    Default TTL is set to 3600 seconds (1 hour).
    """
    expiration = time.time() + ttl if ttl else None
    _CACHE[key] = {
        "data": data,
        "ttl": expiration
    }


async def clear_cache(key: Optional[str] = None) -> None:
    """
    Clear a specific cache entry or flush the entire cache.
    """
    global _CACHE
    if key:
        _CACHE.pop(key, None)
    else:
        _CACHE.clear()
