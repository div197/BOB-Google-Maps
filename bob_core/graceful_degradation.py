"""bob_core.graceful_degradation

Graceful Degradation system for maintaining partial functionality during failures.
Follows the principles of Niṣkāma Karma Yoga - selfless service with perfect execution.
"""
from __future__ import annotations

import time
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import threading
from collections import defaultdict
from contextlib import contextmanager
import re

__all__ = [
    "DegradationLevel", "DegradationStrategy", "GracefulDegradationManager",
    "FallbackFunction", "PartialDataStrategy", "CachedDataStrategy",
    "MinimalDataStrategy", "EmergencyModeStrategy", "CacheManager"
]


class DegradationLevel(Enum):
    """Levels of service degradation."""
    FULL_SERVICE = 0          # Normal operation
    REDUCED_FEATURES = 1      # Some features disabled
    ESSENTIAL_ONLY = 2        # Only core functionality
    MINIMAL_SERVICE = 3       # Bare minimum service
    EMERGENCY_MODE = 4        # Emergency fallbacks only
    SERVICE_UNAVAILABLE = 5   # Complete service failure


@dataclass
class DegradationConfig:
    """Configuration for degradation behavior."""
    level: DegradationLevel
    enabled_features: List[str] = field(default_factory=list)
    fallback_strategies: Dict[str, str] = field(default_factory=dict)
    cache_ttl_seconds: int = 3600
    emergency_contact: Optional[str] = None
    auto_recovery_enabled: bool = True


class DegradationStrategy(ABC):
    """Abstract base class for degradation strategies."""
    
    def __init__(self, name: str, level: DegradationLevel):
        self.name = name
        self.level = level
        self._logger = logging.getLogger(f"bob_core.degradation.{name}")
    
    @abstractmethod
    def execute(self, operation: str, *args, **kwargs) -> Any:
        """Execute the degraded operation."""
        pass
    
    @abstractmethod
    def is_applicable(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check if this strategy applies to the operation."""
        pass


class FallbackFunction(DegradationStrategy):
    """Strategy that uses a fallback function."""
    
    def __init__(self, name: str, level: DegradationLevel, fallback_func: Callable):
        super().__init__(name, level)
        self.fallback_func = fallback_func
    
    def execute(self, operation: str, *args, **kwargs) -> Any:
        """Execute using fallback function."""
        try:
            return self.fallback_func(*args, **kwargs)
        except Exception as e:
            self._logger.error(f"Fallback function failed for {operation}: {e}")
            return None
    
    def is_applicable(self, operation: str, context: Dict[str, Any]) -> bool:
        """Always applicable if fallback function exists."""
        return self.fallback_func is not None


class PartialDataStrategy(DegradationStrategy):
    """Strategy that returns partial data."""
    
    def __init__(self, name: str, level: DegradationLevel, essential_fields: List[str]):
        super().__init__(name, level)
        self.essential_fields = essential_fields
    
    def execute(self, operation: str, *args, **kwargs) -> Any:
        """Return partial data with only essential fields."""
        if operation == "business_info":
            return self._get_partial_business_info(*args, **kwargs)
        elif operation == "reviews":
            return []  # No reviews in degraded mode
        return None
    
    def _get_partial_business_info(self, url: str = None, **kwargs) -> Dict[str, Any]:
        """Extract minimal business info from URL."""
        info = {}
        
        if url:
            # Try to extract business name from URL
            name_match = re.search(r'/search/([^/@]+)', url)
            if name_match:
                name = name_match.group(1).replace('+', ' ').replace('%20', ' ')
                info["name"] = name
            else:
                info["name"] = "Unknown Business"
        
        # Fill essential fields with defaults
        for field in self.essential_fields:
            if field not in info:
                info[field] = "Unavailable"
        
        return info
    
    def is_applicable(self, operation: str, context: Dict[str, Any]) -> bool:
        """Applicable for data extraction operations."""
        return operation in ["business_info", "reviews"]


class CachedDataStrategy(DegradationStrategy):
    """Strategy that uses cached data."""
    
    def __init__(self, name: str, level: DegradationLevel, cache_manager: 'CacheManager'):
        super().__init__(name, level)
        self.cache_manager = cache_manager
    
    def execute(self, operation: str, *args, **kwargs) -> Any:
        """Return cached data if available."""
        cache_key = self._generate_cache_key(operation, *args, **kwargs)
        cached_data = self.cache_manager.get(cache_key)
        
        if cached_data:
            self._logger.info(f"Returning cached data for {operation}")
            return cached_data
        
        return None
    
    def _generate_cache_key(self, operation: str, *args, **kwargs) -> str:
        """Generate cache key for operation."""
        url = kwargs.get('url') or (args[0] if args else '')
        return f"{operation}:{hash(url)}"
    
    def is_applicable(self, operation: str, context: Dict[str, Any]) -> bool:
        """Applicable if cached data exists."""
        cache_key = self._generate_cache_key(operation, **context)
        return self.cache_manager.exists(cache_key)


class MinimalDataStrategy(DegradationStrategy):
    """Strategy that returns minimal hardcoded data."""
    
    def __init__(self, name: str, level: DegradationLevel):
        super().__init__(name, level)
    
    def execute(self, operation: str, *args, **kwargs) -> Any:
        """Return minimal data structure."""
        if operation == "business_info":
            return {
                "name": "Business (Service Degraded)",
                "rating": "Unavailable",
                "category": "Unknown",
                "address": "Unavailable",
                "phone": "Unavailable",
                "website": "Unavailable"
            }
        elif operation == "reviews":
            return []
        return {}
    
    def is_applicable(self, operation: str, context: Dict[str, Any]) -> bool:
        """Always applicable as last resort."""
        return True


class EmergencyModeStrategy(DegradationStrategy):
    """Strategy for emergency mode operation."""
    
    def __init__(self, name: str, level: DegradationLevel, emergency_message: str):
        super().__init__(name, level)
        self.emergency_message = emergency_message
    
    def execute(self, operation: str, *args, **kwargs) -> Any:
        """Return emergency response."""
        return {
            "error": True,
            "message": self.emergency_message,
            "timestamp": time.time(),
            "operation": operation
        }
    
    def is_applicable(self, operation: str, context: Dict[str, Any]) -> bool:
        """Applicable in emergency situations."""
        return context.get("emergency_mode", False)


class CacheManager:
    """Simple in-memory cache manager for degradation strategies."""
    
    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() < entry["expires"]:
                    return entry["value"]
                else:
                    del self._cache[key]
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached value."""
        ttl = ttl or self.default_ttl
        with self._lock:
            self._cache[key] = {
                "value": value,
                "expires": time.time() + ttl,
                "created": time.time()
            }
    
    def exists(self, key: str) -> bool:
        """Check if key exists and is not expired."""
        return self.get(key) is not None
    
    def delete(self, key: str) -> bool:
        """Delete cached value."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cached values."""
        with self._lock:
            self._cache.clear()
    
    def cleanup_expired(self) -> int:
        """Remove expired entries and return count."""
        current_time = time.time()
        expired_keys = []
        
        with self._lock:
            for key, entry in self._cache.items():
                if current_time >= entry["expires"]:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_entries = len(self._cache)
            current_time = time.time()
            expired_count = sum(1 for entry in self._cache.values() 
                              if current_time >= entry["expires"])
            
            return {
                "total_entries": total_entries,
                "active_entries": total_entries - expired_count,
                "expired_entries": expired_count,
                "cache_size_bytes": len(str(self._cache))
            }


class GracefulDegradationManager:
    """
    Main manager for graceful degradation across the system.
    
    Coordinates different degradation strategies and manages service levels
    based on system health and failure patterns.
    
    Example:
        ```python
        manager = GracefulDegradationManager()
        
        # Register strategies
        manager.register_strategy("cached_data", CachedDataStrategy(...))
        manager.register_strategy("partial_data", PartialDataStrategy(...))
        
        # Execute with degradation
        result = manager.execute_with_degradation("scrape_business", url="...")
        ```
    """
    
    def __init__(self, initial_level: DegradationLevel = DegradationLevel.FULL_SERVICE):
        self.current_level = initial_level
        self.strategies: Dict[str, List[DegradationStrategy]] = defaultdict(list)
        self.cache_manager = CacheManager()
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.graceful_degradation")
        
        # Metrics
        self.degradation_events = 0
        self.recovery_events = 0
        self.strategy_usage = defaultdict(int)
        
        # Auto-recovery settings
        self.auto_recovery_enabled = True
        self.recovery_check_interval = 300  # 5 minutes
        self.last_recovery_check = time.time()
        
        # Initialize default strategies
        self._initialize_default_strategies()
    
    def _initialize_default_strategies(self) -> None:
        """Initialize default degradation strategies."""
        # Partial data strategy for reduced features
        partial_strategy = PartialDataStrategy(
            "partial_data",
            DegradationLevel.REDUCED_FEATURES,
            ["name", "rating", "category", "address"]
        )
        self.register_strategy(DegradationLevel.REDUCED_FEATURES, partial_strategy)
        
        # Cached data strategy for essential only
        cached_strategy = CachedDataStrategy(
            "cached_data",
            DegradationLevel.ESSENTIAL_ONLY,
            self.cache_manager
        )
        self.register_strategy(DegradationLevel.ESSENTIAL_ONLY, cached_strategy)
        
        # Minimal data strategy for minimal service
        minimal_strategy = MinimalDataStrategy(
            "minimal_data",
            DegradationLevel.MINIMAL_SERVICE
        )
        self.register_strategy(DegradationLevel.MINIMAL_SERVICE, minimal_strategy)
        
        # Emergency mode strategy
        emergency_strategy = EmergencyModeStrategy(
            "emergency_mode",
            DegradationLevel.EMERGENCY_MODE,
            "Service temporarily unavailable. Please try again later."
        )
        self.register_strategy(DegradationLevel.EMERGENCY_MODE, emergency_strategy)
    
    def register_strategy(self, level: DegradationLevel, strategy: DegradationStrategy) -> None:
        """Register a degradation strategy for a specific level."""
        with self._lock:
            self.strategies[level].append(strategy)
            self._logger.info(f"Registered strategy '{strategy.name}' for level {level.name}")
    
    def set_degradation_level(self, level: DegradationLevel, reason: str = "") -> None:
        """Set the current degradation level."""
        with self._lock:
            if level != self.current_level:
                old_level = self.current_level
                self.current_level = level
                
                if level.value > old_level.value:
                    self.degradation_events += 1
                    self._logger.warning(f"Degraded from {old_level.name} to {level.name}: {reason}")
                else:
                    self.recovery_events += 1
                    self._logger.info(f"Recovered from {old_level.name} to {level.name}: {reason}")
    
    def execute_with_degradation(self, operation: str, **kwargs) -> Any:
        """Execute operation with current degradation level."""
        with self._lock:
            # Check for auto-recovery
            if self.auto_recovery_enabled:
                self._check_auto_recovery()
            
            # Try full service first
            if self.current_level == DegradationLevel.FULL_SERVICE:
                return None  # Let normal operation proceed
            
            # Find applicable strategy for current level
            applicable_strategies = self._find_applicable_strategies(operation, kwargs)
            
            for strategy in applicable_strategies:
                try:
                    result = strategy.execute(operation, **kwargs)
                    if result is not None:
                        self.strategy_usage[strategy.name] += 1
                        self._logger.info(f"Used strategy '{strategy.name}' for {operation}")
                        return result
                except Exception as e:
                    self._logger.error(f"Strategy '{strategy.name}' failed: {e}")
                    continue
            
            # No strategy worked, escalate degradation
            self._escalate_degradation(f"No working strategy for {operation}")
            return self._get_emergency_response(operation)
    
    def _find_applicable_strategies(self, operation: str, context: Dict[str, Any]) -> List[DegradationStrategy]:
        """Find strategies applicable to the current operation and level."""
        applicable = []
        
        # Start from current level and go up (more degraded)
        for level_value in range(self.current_level.value, len(DegradationLevel)):
            level = DegradationLevel(level_value)
            
            for strategy in self.strategies.get(level, []):
                if strategy.is_applicable(operation, context):
                    applicable.append(strategy)
        
        return applicable
    
    def _escalate_degradation(self, reason: str) -> None:
        """Escalate to next degradation level."""
        current_value = self.current_level.value
        if current_value < len(DegradationLevel) - 1:
            new_level = DegradationLevel(current_value + 1)
            self.set_degradation_level(new_level, f"Escalation: {reason}")
    
    def _check_auto_recovery(self) -> None:
        """Check if system can recover to better service level."""
        current_time = time.time()
        if current_time - self.last_recovery_check < self.recovery_check_interval:
            return
        
        self.last_recovery_check = current_time
        
        # Simple recovery logic - try to improve service level
        if self.current_level.value > 0:
            better_level = DegradationLevel(self.current_level.value - 1)
            # In a real implementation, you'd check system health here
            # For now, we'll just attempt recovery after some time
            if self.degradation_events > 0:  # Has been degraded before
                self.set_degradation_level(better_level, "Auto-recovery attempt")
    
    def _get_emergency_response(self, operation: str) -> Dict[str, Any]:
        """Get emergency response when all strategies fail."""
        return {
            "error": True,
            "message": "Service temporarily unavailable",
            "operation": operation,
            "degradation_level": self.current_level.name,
            "timestamp": time.time()
        }
    
    def cache_data(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """Cache data for future degraded operations."""
        self.cache_manager.set(key, data, ttl)
    
    def get_cached_data(self, key: str) -> Optional[Any]:
        """Get cached data."""
        return self.cache_manager.get(key)
    
    def get_minimal_business_info(self, url: str) -> Dict[str, Any]:
        """Get minimal business info for degraded mode."""
        # Try to extract business name from URL
        info = {
            "name": "Unknown Business",
            "rating": "Unavailable",
            "category": "Unknown",
            "address": "Unavailable",
            "phone": "Unavailable",
            "website": "Unavailable"
        }
        
        if url:
            # Extract business name from Google Maps search URL
            name_patterns = [
                r'/search/([^/@]+)',
                r'query=([^&]+)',
                r'q=([^&]+)'
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, url)
                if match:
                    name = match.group(1).replace('+', ' ').replace('%20', ' ')
                    # Clean up the name
                    name = re.sub(r'[^\w\s]', ' ', name).strip()
                    if name:
                        info["name"] = name
                        break
        
        return info
    
    def get_cached_business_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get cached business info if available."""
        cache_key = f"business_info:{hash(url)}"
        return self.cache_manager.get(cache_key)
    
    @contextmanager
    def degradation_context(self, level: DegradationLevel, reason: str = ""):
        """Context manager for temporary degradation."""
        old_level = self.current_level
        try:
            self.set_degradation_level(level, reason)
            yield
        finally:
            self.set_degradation_level(old_level, "Exiting degradation context")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current degradation status and metrics."""
        with self._lock:
            return {
                "current_level": self.current_level.name,
                "degradation_events": self.degradation_events,
                "recovery_events": self.recovery_events,
                "strategy_usage": dict(self.strategy_usage),
                "cache_stats": self.cache_manager.get_stats(),
                "auto_recovery_enabled": self.auto_recovery_enabled,
                "last_recovery_check": self.last_recovery_check,
                "available_strategies": {
                    level.name: [s.name for s in strategies]
                    for level, strategies in self.strategies.items()
                }
            }
    
    def reset_metrics(self) -> None:
        """Reset degradation metrics."""
        with self._lock:
            self.degradation_events = 0
            self.recovery_events = 0
            self.strategy_usage.clear()
    
    def cleanup_cache(self) -> int:
        """Cleanup expired cache entries."""
        return self.cache_manager.cleanup_expired()


# Global degradation manager instance
_global_degradation_manager: Optional[GracefulDegradationManager] = None


def get_global_degradation_manager() -> GracefulDegradationManager:
    """Get or create global degradation manager."""
    global _global_degradation_manager
    if _global_degradation_manager is None:
        _global_degradation_manager = GracefulDegradationManager()
    return _global_degradation_manager 