from cachetools import TTLCache

# cache up to 128 items for 60 seconds
sheet_cache = TTLCache(maxsize=128, ttl=60)
