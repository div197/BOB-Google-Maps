"""
BOB Cache Module v4.3.0

SQLite-based intelligent caching for 1800x speedup on repeat queries.
"""
from .cache_manager import CacheManagerUltimate

# Also export as CacheManager for backwards compatibility
CacheManager = CacheManagerUltimate

__all__ = ['CacheManager', 'CacheManagerUltimate']
