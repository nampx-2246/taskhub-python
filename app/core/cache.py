import json
import os

try:
    import redis
except ImportError:  # pragma: no cover
    redis = None


def get_redis_client():
    if redis is None:
        return None
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        client = redis.from_url(redis_url, decode_responses=True)
        client.ping()
        return client
    except Exception:
        return None


def get_cached_tags(db, get_tags):
    redis_client = get_redis_client()
    if redis_client is None:
        return get_tags(db)

    cached = redis_client.get("tags_list")
    if cached:
        return json.loads(cached)

    tags = get_tags(db)
    try:
        redis_client.set("tags_list", json.dumps([{"id": tag.id, "name": tag.name} for tag in tags]), ex=300)
    except Exception:
        pass
    return tags


def invalidate_tags_cache():
    redis_client = get_redis_client()
    if redis_client is None:
        return
    try:
        redis_client.delete("tags_list")
    except Exception:
        pass
