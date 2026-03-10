import time

# Simple in-memory cache with TTL (Time To Live)
# Structure: { "fake_placeholder": ("real_value", timestamp) }
_cache = {}
TTL_SECONDS = 300  # Data expires after 5 minutes

class SessionStore:
    @staticmethod
    def save(key: str, value: str):
        _cache[key] = (value, time.time())
    
    @staticmethod
    def get(key: str) -> str | None:
        if key not in _cache:
            return None
        
        val, timestamp = _cache[key]
        # Check if expired
        if time.time() - timestamp > TTL_SECONDS:
            del _cache[key]
            return None
        return val

    @staticmethod
    def cleanup():
        """Remove expired keys to prevent memory leaks."""
        current_time = time.time()
        expired_keys = [k for k, (v, t) in _cache.items() if current_time - t > TTL_SECONDS]
        for k in expired_keys:
            del _cache[k]