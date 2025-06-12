"""bob_core.memory_management

Memory Management system for automatic cleanup and optimization.
Follows the principles of Niṣkāma Karma Yoga - selfless service with perfect execution.
"""
from __future__ import annotations

import gc
import time
import threading
import logging
import psutil
import os
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import weakref
from collections import defaultdict

__all__ = [
    "MemoryManager", "MemoryMonitor", "MemoryOptimizer",
    "MemoryThreshold", "MemoryCleanupStrategy", "ObjectTracker",
    "CacheManager", "ResourcePool"
]


@dataclass
class MemoryThreshold:
    """Memory usage thresholds for triggering actions."""
    warning_percent: float = 75.0
    critical_percent: float = 85.0
    emergency_percent: float = 95.0
    cleanup_target_percent: float = 60.0


@dataclass
class MemoryStats:
    """Memory usage statistics."""
    total_memory: int
    available_memory: int
    used_memory: int
    used_percent: float
    process_memory: int
    process_percent: float
    timestamp: float = field(default_factory=time.time)
    
    @property
    def is_warning(self) -> bool:
        """Check if memory usage is at warning level."""
        return self.used_percent >= 75.0
    
    @property
    def is_critical(self) -> bool:
        """Check if memory usage is at critical level."""
        return self.used_percent >= 85.0
    
    @property
    def is_emergency(self) -> bool:
        """Check if memory usage is at emergency level."""
        return self.used_percent >= 95.0


class MemoryCleanupStrategy(ABC):
    """Abstract base class for memory cleanup strategies."""
    
    def __init__(self, name: str, priority: int = 5):
        self.name = name
        self.priority = priority  # 1 = highest priority, 10 = lowest
        self._logger = logging.getLogger(f"bob_core.memory_cleanup.{name}")
    
    @abstractmethod
    def cleanup(self, target_reduction_mb: int) -> int:
        """
        Perform cleanup to reduce memory usage.
        
        Parameters
        ----------
        target_reduction_mb : int
            Target memory reduction in MB
            
        Returns
        -------
        int
            Actual memory reduction achieved in MB
        """
        pass
    
    @abstractmethod
    def estimate_cleanup_potential(self) -> int:
        """Estimate how much memory this strategy could free in MB."""
        pass
    
    def get_description(self) -> str:
        """Get human-readable description of this strategy."""
        return f"{self.name} (priority: {self.priority})"


class GarbageCollectionStrategy(MemoryCleanupStrategy):
    """Strategy for garbage collection cleanup."""
    
    def __init__(self):
        super().__init__("garbage_collection", priority=1)
    
    def cleanup(self, target_reduction_mb: int) -> int:
        """Perform garbage collection."""
        try:
            # Get memory before cleanup
            process = psutil.Process()
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Force garbage collection
            collected = gc.collect()
            
            # Get memory after cleanup
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            reduction = max(0, memory_before - memory_after)
            
            self._logger.info(f"Garbage collection freed {reduction:.1f} MB, collected {collected} objects")
            return int(reduction)
            
        except Exception as e:
            self._logger.error(f"Garbage collection failed: {e}")
            return 0
    
    def estimate_cleanup_potential(self) -> int:
        """Estimate garbage collection potential."""
        # Count unreachable objects
        try:
            unreachable = len(gc.garbage)
            # Rough estimate: each unreachable object = 1KB
            return max(1, unreachable // 1024)  # Convert to MB
        except:
            return 5  # Conservative estimate


class CacheCleanupStrategy(MemoryCleanupStrategy):
    """Strategy for cleaning up caches."""
    
    def __init__(self, cache_managers: List['CacheManager'] = None):
        super().__init__("cache_cleanup", priority=2)
        self.cache_managers = cache_managers or []
    
    def add_cache_manager(self, cache_manager: 'CacheManager') -> None:
        """Add a cache manager to monitor."""
        self.cache_managers.append(cache_manager)
    
    def cleanup(self, target_reduction_mb: int) -> int:
        """Clean up caches."""
        total_reduction = 0
        
        for cache_manager in self.cache_managers:
            try:
                reduction = cache_manager.cleanup_expired()
                total_reduction += reduction
                
                # If we haven't reached target, clean more aggressively
                if total_reduction < target_reduction_mb:
                    additional = cache_manager.cleanup_lru(target_reduction_mb - total_reduction)
                    total_reduction += additional
                
            except Exception as e:
                self._logger.error(f"Cache cleanup failed for {cache_manager}: {e}")
        
        self._logger.info(f"Cache cleanup freed {total_reduction} MB")
        return total_reduction
    
    def estimate_cleanup_potential(self) -> int:
        """Estimate cache cleanup potential."""
        total_potential = 0
        for cache_manager in self.cache_managers:
            try:
                potential = cache_manager.estimate_cleanup_potential()
                total_potential += potential
            except:
                continue
        return total_potential


class ObjectPoolCleanupStrategy(MemoryCleanupStrategy):
    """Strategy for cleaning up object pools."""
    
    def __init__(self, object_pools: List['ResourcePool'] = None):
        super().__init__("object_pool_cleanup", priority=3)
        self.object_pools = object_pools or []
    
    def add_object_pool(self, pool: 'ResourcePool') -> None:
        """Add an object pool to monitor."""
        self.object_pools.append(pool)
    
    def cleanup(self, target_reduction_mb: int) -> int:
        """Clean up object pools."""
        total_reduction = 0
        
        for pool in self.object_pools:
            try:
                reduction = pool.cleanup_idle_objects()
                total_reduction += reduction
            except Exception as e:
                self._logger.error(f"Object pool cleanup failed for {pool}: {e}")
        
        self._logger.info(f"Object pool cleanup freed {total_reduction} MB")
        return total_reduction
    
    def estimate_cleanup_potential(self) -> int:
        """Estimate object pool cleanup potential."""
        total_potential = 0
        for pool in self.object_pools:
            try:
                potential = pool.estimate_cleanup_potential()
                total_potential += potential
            except:
                continue
        return total_potential


class MemoryMonitor:
    """Monitor for tracking memory usage and triggering alerts."""
    
    def __init__(self, 
                 thresholds: MemoryThreshold = None,
                 check_interval_seconds: int = 30):
        self.thresholds = thresholds or MemoryThreshold()
        self.check_interval_seconds = check_interval_seconds
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._callbacks: Dict[str, List[Callable]] = defaultdict(list)
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.memory_monitor")
        self._stats_history: List[MemoryStats] = []
        self._max_history = 1000
    
    def start_monitoring(self) -> None:
        """Start memory monitoring."""
        if self._monitoring:
            self._logger.warning("Memory monitoring is already running")
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._monitor_thread.start()
        self._logger.info("Started memory monitoring")
    
    def stop_monitoring(self) -> None:
        """Stop memory monitoring."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        self._logger.info("Stopped memory monitoring")
    
    def add_callback(self, event_type: str, callback: Callable[[MemoryStats], None]) -> None:
        """Add callback for memory events."""
        with self._lock:
            self._callbacks[event_type].append(callback)
            self._logger.info(f"Added callback for {event_type}")
    
    def get_current_stats(self) -> MemoryStats:
        """Get current memory statistics."""
        try:
            # System memory
            memory = psutil.virtual_memory()
            
            # Process memory
            process = psutil.Process()
            process_memory = process.memory_info()
            
            return MemoryStats(
                total_memory=memory.total,
                available_memory=memory.available,
                used_memory=memory.used,
                used_percent=memory.percent,
                process_memory=process_memory.rss,
                process_percent=process_memory.rss / memory.total * 100
            )
            
        except Exception as e:
            self._logger.error(f"Failed to get memory stats: {e}")
            return MemoryStats(0, 0, 0, 0.0, 0, 0.0)
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        last_warning_time = 0
        last_critical_time = 0
        
        while self._monitoring:
            try:
                stats = self.get_current_stats()
                
                # Store in history
                with self._lock:
                    self._stats_history.append(stats)
                    if len(self._stats_history) > self._max_history:
                        self._stats_history = self._stats_history[-self._max_history//2:]
                
                current_time = time.time()
                
                # Check thresholds and trigger callbacks
                if stats.is_emergency:
                    self._trigger_callbacks("emergency", stats)
                elif stats.is_critical and current_time - last_critical_time > 60:
                    self._trigger_callbacks("critical", stats)
                    last_critical_time = current_time
                elif stats.is_warning and current_time - last_warning_time > 300:
                    self._trigger_callbacks("warning", stats)
                    last_warning_time = current_time
                
                # Always trigger general update
                self._trigger_callbacks("update", stats)
                
                time.sleep(self.check_interval_seconds)
                
            except Exception as e:
                self._logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)
    
    def _trigger_callbacks(self, event_type: str, stats: MemoryStats) -> None:
        """Trigger callbacks for an event type."""
        with self._lock:
            for callback in self._callbacks[event_type]:
                try:
                    callback(stats)
                except Exception as e:
                    self._logger.error(f"Callback error for {event_type}: {e}")
    
    def get_memory_trend(self, minutes: int = 30) -> Dict[str, Any]:
        """Get memory usage trend over time."""
        with self._lock:
            if not self._stats_history:
                return {"trend": "unknown", "data_points": 0}
            
            cutoff_time = time.time() - (minutes * 60)
            recent_stats = [s for s in self._stats_history if s.timestamp >= cutoff_time]
            
            if len(recent_stats) < 2:
                return {"trend": "insufficient_data", "data_points": len(recent_stats)}
            
            # Calculate trend
            first_usage = recent_stats[0].used_percent
            last_usage = recent_stats[-1].used_percent
            avg_usage = sum(s.used_percent for s in recent_stats) / len(recent_stats)
            
            trend = "stable"
            if last_usage > first_usage + 5:
                trend = "increasing"
            elif last_usage < first_usage - 5:
                trend = "decreasing"
            
            return {
                "trend": trend,
                "data_points": len(recent_stats),
                "first_usage": first_usage,
                "last_usage": last_usage,
                "average_usage": avg_usage,
                "peak_usage": max(s.used_percent for s in recent_stats),
                "min_usage": min(s.used_percent for s in recent_stats)
            }


class MemoryOptimizer:
    """Optimizer for memory usage with multiple cleanup strategies."""
    
    def __init__(self, thresholds: MemoryThreshold = None):
        self.thresholds = thresholds or MemoryThreshold()
        self.strategies: List[MemoryCleanupStrategy] = []
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.memory_optimizer")
        self._cleanup_history: List[Dict[str, Any]] = []
        
        # Add default strategies
        self.add_strategy(GarbageCollectionStrategy())
    
    def add_strategy(self, strategy: MemoryCleanupStrategy) -> None:
        """Add a cleanup strategy."""
        with self._lock:
            self.strategies.append(strategy)
            # Sort by priority (lower number = higher priority)
            self.strategies.sort(key=lambda s: s.priority)
            self._logger.info(f"Added cleanup strategy: {strategy.get_description()}")
    
    def optimize_memory(self, target_reduction_mb: int = None) -> Dict[str, Any]:
        """Optimize memory usage using available strategies."""
        with self._lock:
            start_time = time.time()
            
            # Get current memory stats
            process = psutil.Process()
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Calculate target reduction if not provided
            if target_reduction_mb is None:
                memory_stats = psutil.virtual_memory()
                if memory_stats.percent > self.thresholds.critical_percent:
                    # Aggressive cleanup
                    target_reduction_mb = int(memory_before * 0.3)
                elif memory_stats.percent > self.thresholds.warning_percent:
                    # Moderate cleanup
                    target_reduction_mb = int(memory_before * 0.15)
                else:
                    # Light cleanup
                    target_reduction_mb = int(memory_before * 0.05)
            
            self._logger.info(f"Starting memory optimization, target reduction: {target_reduction_mb} MB")
            
            total_reduction = 0
            strategy_results = []
            
            # Execute strategies in priority order
            for strategy in self.strategies:
                if total_reduction >= target_reduction_mb:
                    break
                
                remaining_target = target_reduction_mb - total_reduction
                
                try:
                    reduction = strategy.cleanup(remaining_target)
                    total_reduction += reduction
                    
                    strategy_results.append({
                        "strategy": strategy.name,
                        "reduction_mb": reduction,
                        "success": True
                    })
                    
                    self._logger.info(f"Strategy {strategy.name} freed {reduction} MB")
                    
                except Exception as e:
                    strategy_results.append({
                        "strategy": strategy.name,
                        "reduction_mb": 0,
                        "success": False,
                        "error": str(e)
                    })
                    
                    self._logger.error(f"Strategy {strategy.name} failed: {e}")
            
            # Get final memory stats
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            actual_reduction = max(0, memory_before - memory_after)
            
            duration = time.time() - start_time
            
            result = {
                "target_reduction_mb": target_reduction_mb,
                "actual_reduction_mb": actual_reduction,
                "memory_before_mb": memory_before,
                "memory_after_mb": memory_after,
                "duration_seconds": duration,
                "strategies_executed": len(strategy_results),
                "strategy_results": strategy_results,
                "success": actual_reduction > 0
            }
            
            # Store in history
            self._cleanup_history.append(result)
            if len(self._cleanup_history) > 100:
                self._cleanup_history = self._cleanup_history[-50:]
            
            self._logger.info(f"Memory optimization completed: {actual_reduction:.1f} MB freed in {duration:.2f}s")
            
            return result
    
    def get_optimization_potential(self) -> Dict[str, Any]:
        """Estimate total memory optimization potential."""
        with self._lock:
            strategy_potentials = {}
            total_potential = 0
            
            for strategy in self.strategies:
                try:
                    potential = strategy.estimate_cleanup_potential()
                    strategy_potentials[strategy.name] = potential
                    total_potential += potential
                except Exception as e:
                    strategy_potentials[strategy.name] = 0
                    self._logger.error(f"Failed to estimate potential for {strategy.name}: {e}")
            
            return {
                "total_potential_mb": total_potential,
                "strategy_potentials": strategy_potentials,
                "strategies_available": len(self.strategies)
            }
    
    def get_cleanup_history(self) -> List[Dict[str, Any]]:
        """Get history of cleanup operations."""
        with self._lock:
            return self._cleanup_history.copy()


class ObjectTracker:
    """Tracker for monitoring object creation and lifecycle."""
    
    def __init__(self):
        self._tracked_objects: Dict[str, List[weakref.ref]] = defaultdict(list)
        self._creation_counts: Dict[str, int] = defaultdict(int)
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.object_tracker")
    
    def track_object(self, obj: Any, category: str = "general") -> None:
        """Track an object for monitoring."""
        with self._lock:
            try:
                weak_ref = weakref.ref(obj, lambda ref: self._on_object_deleted(ref, category))
                self._tracked_objects[category].append(weak_ref)
                self._creation_counts[category] += 1
            except TypeError:
                # Object doesn't support weak references
                self._logger.warning(f"Cannot track object of type {type(obj).__name__}")
    
    def _on_object_deleted(self, ref: weakref.ref, category: str) -> None:
        """Callback when tracked object is deleted."""
        with self._lock:
            if ref in self._tracked_objects[category]:
                self._tracked_objects[category].remove(ref)
    
    def get_object_counts(self) -> Dict[str, Dict[str, int]]:
        """Get counts of tracked objects."""
        with self._lock:
            # Clean up dead references
            for category in self._tracked_objects:
                self._tracked_objects[category] = [
                    ref for ref in self._tracked_objects[category] if ref() is not None
                ]
            
            return {
                category: {
                    "alive": len(refs),
                    "created": self._creation_counts[category],
                    "deleted": self._creation_counts[category] - len(refs)
                }
                for category, refs in self._tracked_objects.items()
            }
    
    def cleanup_dead_references(self) -> int:
        """Clean up dead weak references."""
        with self._lock:
            cleaned = 0
            for category in self._tracked_objects:
                before_count = len(self._tracked_objects[category])
                self._tracked_objects[category] = [
                    ref for ref in self._tracked_objects[category] if ref() is not None
                ]
                after_count = len(self._tracked_objects[category])
                cleaned += before_count - after_count
            
            return cleaned


class CacheManager:
    """Manager for in-memory caches with automatic cleanup."""
    
    def __init__(self, 
                 name: str,
                 max_size: int = 1000,
                 ttl_seconds: int = 3600):
        self.name = name
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_times: Dict[str, float] = {}
        self._lock = threading.RLock()
        self._logger = logging.getLogger(f"bob_core.cache_manager.{name}")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            
            # Check TTL
            if time.time() - entry["timestamp"] > self.ttl_seconds:
                del self._cache[key]
                del self._access_times[key]
                return None
            
            # Update access time
            self._access_times[key] = time.time()
            return entry["value"]
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        with self._lock:
            # Check size limit
            if len(self._cache) >= self.max_size and key not in self._cache:
                self._evict_lru()
            
            self._cache[key] = {
                "value": value,
                "timestamp": time.time()
            }
            self._access_times[key] = time.time()
    
    def _evict_lru(self) -> None:
        """Evict least recently used item."""
        if not self._access_times:
            return
        
        lru_key = min(self._access_times.items(), key=lambda x: x[1])[0]
        del self._cache[lru_key]
        del self._access_times[lru_key]
    
    def cleanup_expired(self) -> int:
        """Clean up expired entries."""
        with self._lock:
            current_time = time.time()
            expired_keys = []
            
            for key, entry in self._cache.items():
                if current_time - entry["timestamp"] > self.ttl_seconds:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
                del self._access_times[key]
            
            self._logger.info(f"Cleaned up {len(expired_keys)} expired entries")
            return len(expired_keys)
    
    def cleanup_lru(self, target_count: int) -> int:
        """Clean up least recently used entries."""
        with self._lock:
            if len(self._cache) <= target_count:
                return 0
            
            # Sort by access time
            sorted_items = sorted(self._access_times.items(), key=lambda x: x[1])
            to_remove = len(self._cache) - target_count
            
            removed_count = 0
            for key, _ in sorted_items[:to_remove]:
                if key in self._cache:
                    del self._cache[key]
                    del self._access_times[key]
                    removed_count += 1
            
            self._logger.info(f"Cleaned up {removed_count} LRU entries")
            return removed_count
    
    def estimate_cleanup_potential(self) -> int:
        """Estimate cleanup potential in MB."""
        with self._lock:
            # Rough estimate: 1KB per cache entry
            return len(self._cache) // 1024  # Convert to MB
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            current_time = time.time()
            expired_count = sum(
                1 for entry in self._cache.values()
                if current_time - entry["timestamp"] > self.ttl_seconds
            )
            
            return {
                "name": self.name,
                "size": len(self._cache),
                "max_size": self.max_size,
                "expired_entries": expired_count,
                "ttl_seconds": self.ttl_seconds
            }


class ResourcePool:
    """Pool for managing reusable resources."""
    
    def __init__(self, 
                 name: str,
                 factory: Callable[[], Any],
                 max_size: int = 10,
                 idle_timeout_seconds: int = 300):
        self.name = name
        self.factory = factory
        self.max_size = max_size
        self.idle_timeout_seconds = idle_timeout_seconds
        self._pool: List[Dict[str, Any]] = []
        self._in_use: Dict[int, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._logger = logging.getLogger(f"bob_core.resource_pool.{name}")
    
    def acquire(self) -> Any:
        """Acquire a resource from the pool."""
        with self._lock:
            # Try to get from pool
            while self._pool:
                resource_info = self._pool.pop(0)
                resource = resource_info["resource"]
                
                # Check if resource is still valid
                if hasattr(resource, 'is_valid') and not resource.is_valid():
                    continue
                
                # Move to in-use
                resource_id = id(resource)
                self._in_use[resource_id] = {
                    "resource": resource,
                    "acquired_time": time.time()
                }
                
                return resource
            
            # Create new resource if pool is empty
            try:
                resource = self.factory()
                resource_id = id(resource)
                self._in_use[resource_id] = {
                    "resource": resource,
                    "acquired_time": time.time()
                }
                return resource
            except Exception as e:
                self._logger.error(f"Failed to create resource: {e}")
                raise
    
    def release(self, resource: Any) -> None:
        """Release a resource back to the pool."""
        with self._lock:
            resource_id = id(resource)
            
            if resource_id not in self._in_use:
                self._logger.warning("Attempting to release unknown resource")
                return
            
            # Remove from in-use
            del self._in_use[resource_id]
            
            # Add back to pool if there's space
            if len(self._pool) < self.max_size:
                self._pool.append({
                    "resource": resource,
                    "returned_time": time.time()
                })
            else:
                # Pool is full, dispose of resource
                if hasattr(resource, 'close'):
                    try:
                        resource.close()
                    except:
                        pass
    
    def cleanup_idle_objects(self) -> int:
        """Clean up idle objects from the pool."""
        with self._lock:
            current_time = time.time()
            cleaned = 0
            
            # Clean up idle resources in pool
            active_pool = []
            for resource_info in self._pool:
                if current_time - resource_info["returned_time"] > self.idle_timeout_seconds:
                    # Resource is idle, dispose of it
                    resource = resource_info["resource"]
                    if hasattr(resource, 'close'):
                        try:
                            resource.close()
                        except:
                            pass
                    cleaned += 1
                else:
                    active_pool.append(resource_info)
            
            self._pool = active_pool
            
            self._logger.info(f"Cleaned up {cleaned} idle resources")
            return cleaned
    
    def estimate_cleanup_potential(self) -> int:
        """Estimate cleanup potential in MB."""
        with self._lock:
            # Rough estimate: 1MB per pooled resource
            return len(self._pool)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics."""
        with self._lock:
            return {
                "name": self.name,
                "pool_size": len(self._pool),
                "in_use": len(self._in_use),
                "max_size": self.max_size,
                "idle_timeout_seconds": self.idle_timeout_seconds
            }


class MemoryManager:
    """
    Main memory management system that coordinates all memory-related operations.
    
    Features:
    - Automatic memory monitoring
    - Intelligent cleanup strategies
    - Resource pooling
    - Cache management
    - Object lifecycle tracking
    
    Example:
        ```python
        # Initialize memory manager
        manager = MemoryManager()
        
        # Start monitoring
        manager.start_monitoring()
        
        # Register caches and pools
        cache = CacheManager("my_cache")
        manager.register_cache(cache)
        
        # Memory will be automatically optimized when thresholds are reached
        ```
    """
    
    def __init__(self, thresholds: MemoryThreshold = None):
        self.thresholds = thresholds or MemoryThreshold()
        self.monitor = MemoryMonitor(self.thresholds)
        self.optimizer = MemoryOptimizer(self.thresholds)
        self.object_tracker = ObjectTracker()
        self._caches: List[CacheManager] = []
        self._pools: List[ResourcePool] = []
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.memory_manager")
        
        # Setup automatic cleanup
        self._setup_automatic_cleanup()
    
    def _setup_automatic_cleanup(self) -> None:
        """Setup automatic cleanup triggers."""
        # Add cache cleanup strategy
        cache_strategy = CacheCleanupStrategy(self._caches)
        self.optimizer.add_strategy(cache_strategy)
        
        # Add pool cleanup strategy
        pool_strategy = ObjectPoolCleanupStrategy(self._pools)
        self.optimizer.add_strategy(pool_strategy)
        
        # Setup monitoring callbacks
        self.monitor.add_callback("warning", self._on_memory_warning)
        self.monitor.add_callback("critical", self._on_memory_critical)
        self.monitor.add_callback("emergency", self._on_memory_emergency)
    
    def start_monitoring(self) -> None:
        """Start memory monitoring."""
        self.monitor.start_monitoring()
        self._logger.info("Memory management started")
    
    def stop_monitoring(self) -> None:
        """Stop memory monitoring."""
        self.monitor.stop_monitoring()
        self._logger.info("Memory management stopped")
    
    def register_cache(self, cache: CacheManager) -> None:
        """Register a cache for management."""
        with self._lock:
            self._caches.append(cache)
            # Update cache strategy
            for strategy in self.optimizer.strategies:
                if isinstance(strategy, CacheCleanupStrategy):
                    strategy.add_cache_manager(cache)
                    break
            self._logger.info(f"Registered cache: {cache.name}")
    
    def register_pool(self, pool: ResourcePool) -> None:
        """Register a resource pool for management."""
        with self._lock:
            self._pools.append(pool)
            # Update pool strategy
            for strategy in self.optimizer.strategies:
                if isinstance(strategy, ObjectPoolCleanupStrategy):
                    strategy.add_object_pool(pool)
                    break
            self._logger.info(f"Registered pool: {pool.name}")
    
    def track_object(self, obj: Any, category: str = "general") -> None:
        """Track an object for monitoring."""
        self.object_tracker.track_object(obj, category)
    
    def optimize_memory(self, force: bool = False) -> Dict[str, Any]:
        """Optimize memory usage."""
        if force:
            return self.optimizer.optimize_memory()
        else:
            stats = self.monitor.get_current_stats()
            if stats.is_warning:
                return self.optimizer.optimize_memory()
            else:
                return {"message": "Memory optimization not needed", "skipped": True}
    
    def _on_memory_warning(self, stats: MemoryStats) -> None:
        """Handle memory warning."""
        self._logger.warning(f"Memory warning: {stats.used_percent:.1f}% used")
        # Light cleanup
        self.optimizer.optimize_memory(target_reduction_mb=50)
    
    def _on_memory_critical(self, stats: MemoryStats) -> None:
        """Handle critical memory usage."""
        self._logger.error(f"Critical memory usage: {stats.used_percent:.1f}% used")
        # Aggressive cleanup
        self.optimizer.optimize_memory(target_reduction_mb=200)
    
    def _on_memory_emergency(self, stats: MemoryStats) -> None:
        """Handle emergency memory usage."""
        self._logger.critical(f"Emergency memory usage: {stats.used_percent:.1f}% used")
        # Emergency cleanup
        self.optimizer.optimize_memory(target_reduction_mb=500)
    
    def get_comprehensive_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics."""
        with self._lock:
            current_stats = self.monitor.get_current_stats()
            trend = self.monitor.get_memory_trend()
            object_counts = self.object_tracker.get_object_counts()
            optimization_potential = self.optimizer.get_optimization_potential()
            
            cache_stats = [cache.get_stats() for cache in self._caches]
            pool_stats = [pool.get_stats() for pool in self._pools]
            
            return {
                "current_memory": {
                    "used_percent": current_stats.used_percent,
                    "used_memory_mb": current_stats.used_memory / 1024 / 1024,
                    "process_memory_mb": current_stats.process_memory / 1024 / 1024,
                    "available_memory_mb": current_stats.available_memory / 1024 / 1024
                },
                "trend": trend,
                "thresholds": {
                    "warning": self.thresholds.warning_percent,
                    "critical": self.thresholds.critical_percent,
                    "emergency": self.thresholds.emergency_percent
                },
                "object_tracking": object_counts,
                "optimization_potential": optimization_potential,
                "optimizer": {
                    "strategies": [strategy.get_description() for strategy in self.optimizer.strategies],
                    "cleanup_history": self.optimizer.get_cleanup_history()
                },
                "caches": cache_stats,
                "pools": pool_stats,
                "monitoring_active": self.monitor._monitoring
            }


# Global memory manager instance
_global_memory_manager: Optional[MemoryManager] = None


def get_global_memory_manager() -> MemoryManager:
    """Get or create global memory manager."""
    global _global_memory_manager
    if _global_memory_manager is None:
        _global_memory_manager = MemoryManager()
    return _global_memory_manager 