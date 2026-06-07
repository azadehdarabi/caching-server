import json

import redis


class CacheManager:

    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port, decode_responses=False)

    def get(self, key: str):
        result = self.client.get(key)
        if not result:
            return None, None
        payload = json.loads(result)
        return bytes.fromhex(payload["body"]), payload["headers"]

    def set(self, key: str, value: bytes, headers: dict, ttl: int = 60):
        payload = json.dumps({"body": value.hex(), "headers": headers})
        self.client.set(key, payload, ex=ttl)

    def clear(self):
        self.client.flushdb()
