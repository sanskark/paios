import time

cache = {}
TTL = 60


def make_key(user_input, context):
    context_str = " ".join(context)
    return f"{user_input.lower()}::{context_str.lower()}"


def get_cache(key):
    item = cache.get(key)
    if not item:
        return None

    value, timestamp = item
    if time.time() - timestamp > TTL:
        del cache[key]
        return None

    return value


def set_cache(key, value):
    cache[key] = (value, time.time())


def clear_cache():
    cache.clear()
