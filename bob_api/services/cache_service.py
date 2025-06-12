"""bob_api.services.cache_service

Cache Service for BOB Google Maps API v0.6.0
Divine caching implementation following Niṣkāma Karma Yoga principles.

Made with 🙏 for interconnected excellence
"""

import asyncio
import time
import json
import pickle
from typing import Dict, Any, Optional
from collections import OrderedDict

from .interfaces import CacheService


class CacheServiceImpl(CacheService):
    """Divine cache service implementation."""
    
    def __init__(
        self,
        redis_url: Optional[str] = None,
        default_ttl: int = 3600,
        max_memory_cache_size: int = 1000
    ):
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self.max_memory_cache_size = max_memory_cache_size
        self._initialized = False
        
        # Redis client (if available)
        self._redis = None
        
        # In-memory cache as fallback
        self._memory_cache: OrderedDict = OrderedDict()
        self._cache_expiry: Dict[str, float] = {}
        
        # Cache statistics
        self._stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0,
            'evictions': 0
        }
    
    async def initialize(self):
        """Initialize the cache service."""
        if self._initialized:
            return
        
        # Try to initialize Redis if URL is provided
        if self.redis_url:
            try:
                import redis.asyncio as redis
                self._redis = redis.from_url(self.redis_url)
                # Test connection
                await self._redis.ping()
            except Exception:
                # Fall back to memory cache
                self._redis = None
        
        self._initialized = True
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            # Try Redis first
            if self._redis:
                try:
                    value = await self._redis.get(key)
                    if value is not None:
                        self._stats['hits'] += 1
                        return self._deserialize(value)
                except Exception:
                    pass
            
            # Try memory cache
            if key in self._memory_cache:
                # Check if expired
                if key in self._cache_expiry and time.time() > self._cache_expiry[key]:
                    await self._remove_from_memory_cache(key)
                    self._stats['misses'] += 1
                    return None
                
                # Move to end (LRU)
                value = self._memory_cache[key]
                self._memory_cache.move_to_end(key)
                self._stats['hits'] += 1
                return value
            
            self._stats['misses'] += 1
            return None
            
        except Exception:
            self._stats['misses'] += 1
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with optional TTL."""
        try:
            ttl = ttl or self.default_ttl
            
            # Try Redis first
            if self._redis:
                try:
                    serialized_value = self._serialize(value)
                    await self._redis.setex(key, ttl, serialized_value)
                    self._stats['sets'] += 1
                    return
                except Exception:
                    pass
            
            # Use memory cache
            await self._set_in_memory_cache(key, value, ttl)
            self._stats['sets'] += 1
            
        except Exception:
            pass
    
    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        try:
            # Try Redis first
            if self._redis:
                try:
                    await self._redis.delete(key)
                except Exception:
                    pass
            
            # Remove from memory cache
            await self._remove_from_memory_cache(key)
            self._stats['deletes'] += 1
            
        except Exception:
            pass
    
    async def clear_all(self) -> None:
        """Clear all cache entries."""
        try:
            # Clear Redis
            if self._redis:
                try:
                    await self._redis.flushdb()
                except Exception:
                    pass
            
            # Clear memory cache
            self._memory_cache.clear()
            self._cache_expiry.clear()
            
        except Exception:
            pass
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        try:
            total_requests = self._stats['hits'] + self._stats['misses']
            hit_rate = self._stats['hits'] / total_requests if total_requests > 0 else 0
            
            stats = {
                "hits": self._stats['hits'],
                "misses": self._stats['misses'],
                "sets": self._stats['sets'],
                "deletes": self._stats['deletes'],
                "evictions": self._stats['evictions'],
                "hit_rate": hit_rate,
                "memory_cache_size": len(self._memory_cache),
                "memory_cache_max_size": self.max_memory_cache_size,
                "redis_available": self._redis is not None,
                "timestamp": time.time()
            }
            
            # Add Redis stats if available
            if self._redis:
                try:
                    redis_info = await self._redis.info()
                    stats["redis_info"] = {
                        "used_memory": redis_info.get('used_memory', 0),
                        "used_memory_human": redis_info.get('used_memory_human', '0B'),
                        "connected_clients": redis_info.get('connected_clients', 0),
                        "total_commands_processed": redis_info.get('total_commands_processed', 0)
                    }
                except Exception:
                    pass
            
            return stats
            
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": time.time()
            }
    
    async def _set_in_memory_cache(self, key: str, value: Any, ttl: int):
        """Set value in memory cache."""
        # Check if we need to evict items
        while len(self._memory_cache) >= self.max_memory_cache_size:
            # Remove oldest item (LRU)
            oldest_key = next(iter(self._memory_cache))
            await self._remove_from_memory_cache(oldest_key)
            self._stats['evictions'] += 1
        
        # Set the value
        self._memory_cache[key] = value
        self._cache_expiry[key] = time.time() + ttl
        
        # Move to end (most recently used)
        self._memory_cache.move_to_end(key)
    
    async def _remove_from_memory_cache(self, key: str):
        """Remove key from memory cache."""
        if key in self._memory_cache:
            del self._memory_cache[key]
        if key in self._cache_expiry:
            del self._cache_expiry[key]
    
    def _serialize(self, value: Any) -> bytes:
        """Serialize value for storage."""
        try:
            # Try JSON first (for simple types)
            return json.dumps(value).encode('utf-8')
        except (TypeError, ValueError):
            # Fall back to pickle for complex objects
            return pickle.dumps(value)
    
    def _deserialize(self, value: bytes) -> Any:
        """Deserialize value from storage."""
        try:
            # Try JSON first
            return json.loads(value.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Fall back to pickle
            return pickle.loads(value)
    
    def is_healthy(self) -> bool:
        """Check if the service is healthy."""
        return self._initialized
    
    async def shutdown(self):
        """Shutdown the service gracefully."""
        if self._redis:
            try:
                await self._redis.close()
            except Exception:
                pass
        
        self._memory_cache.clear()
        self._cache_expiry.clear()
        self._initialized = False 