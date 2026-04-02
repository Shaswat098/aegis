from django.core.cache import cache
import hashlib
import json

def check_cache():
    try:
        cache.set("test", "ok", 10)
        return cache.get("test")
    except:
        return "Redis not working"

def generate_cache_key(features: dict) -> str:
    key_string = json.dumps(features, sort_keys = True)
    return "fraud:" + hashlib.md5(key_string.encode()).hexdigest()  

def get_cached_prediction(features: dict):
    key = generate_cache_key(features)
    return cache.get(key)

def set_cached_prediction(features: dict, value: float, ttl=300):
    key = generate_cache_key(features)
    cache.set(key, value, timeout=ttl)