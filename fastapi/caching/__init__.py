"""Simple response caching utilities for FastAPI."""

from fastapi.dependencies.utils import get_dependant
from fastapi.routing import APIRoute


class CachedRoute(APIRoute):
    """A route subclass that caches responses based on dependency signatures."""

    def __init__(self, *args, cache_ttl: int = 60, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_ttl = cache_ttl
        self._cache: dict[str, tuple[float, object]] = {}

    def _get_cache_key(self, path: str) -> str:
        dependant = get_dependant(path=path, call=self.endpoint)
        return f"{path}:{id(dependant)}"
