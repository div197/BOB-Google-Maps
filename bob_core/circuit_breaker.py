"""bob_core.circuit_breaker

Circuit Breaker pattern implementation for fault tolerance and cascade failure prevention.
Follows the principles of Niṣkāma Karma Yoga - selfless service with perfect execution.
"""
from __future__ import annotations

import time
import threading
from enum import Enum
from typing import Callable, Any, Optional, Dict
from dataclasses import dataclass, field
from collections import deque
import logging

__all__ = ["CircuitBreaker", "CircuitBreakerState", "CircuitBreakerError"]


class CircuitBreakerState(Enum):
    """Circuit breaker states following the classic pattern."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing fast, not calling service
    HALF_OPEN = "half_open"  # Testing if service has recovered


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open and prevents execution."""
    pass


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior."""
    failure_threshold: int = 5  # Number of failures before opening
    recovery_timeout: int = 60  # Seconds before trying half-open
    success_threshold: int = 3  # Successes needed to close from half-open
    timeout: float = 30.0  # Operation timeout in seconds
    expected_exception: type = Exception  # Exception type that counts as failure


@dataclass
class CircuitBreakerMetrics:
    """Metrics tracking for circuit breaker."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    timeouts: int = 0
    circuit_open_count: int = 0
    last_failure_time: Optional[float] = None
    recent_failures: deque = field(default_factory=lambda: deque(maxlen=100))


class CircuitBreaker:
    """
    Circuit Breaker implementation for preventing cascade failures.
    
    Follows the three-state pattern:
    - CLOSED: Normal operation, monitoring for failures
    - OPEN: Fast-failing, not executing protected function
    - HALF_OPEN: Testing if service has recovered
    
    Example:
        ```python
        breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)
        
        @breaker
        def risky_operation():
            # This might fail
            return external_api_call()
        
        try:
            result = risky_operation()
        except CircuitBreakerError:
            # Circuit is open, use fallback
            result = fallback_operation()
        ```
    """
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 recovery_timeout: int = 60,
                 success_threshold: int = 3,
                 timeout: float = 30.0,
                 expected_exception: type = Exception,
                 name: str = "default"):
        """
        Initialize circuit breaker.
        
        Parameters
        ----------
        failure_threshold : int
            Number of consecutive failures before opening circuit
        recovery_timeout : int
            Seconds to wait before attempting recovery
        success_threshold : int
            Number of successes needed to close circuit from half-open
        timeout : float
            Timeout for protected operations
        expected_exception : type
            Exception type that counts as failure
        name : str
            Name for logging and metrics
        """
        self.config = CircuitBreakerConfig(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            success_threshold=success_threshold,
            timeout=timeout,
            expected_exception=expected_exception
        )
        self.name = name
        self.state = CircuitBreakerState.CLOSED
        self.metrics = CircuitBreakerMetrics()
        self._lock = threading.RLock()
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time: Optional[float] = None
        self._logger = logging.getLogger(f"bob_core.circuit_breaker.{name}")
    
    @property
    def failure_threshold(self) -> int:
        """Get the failure threshold."""
        return self.config.failure_threshold
    
    @property
    def recovery_timeout(self) -> int:
        """Get the recovery timeout."""
        return self.config.recovery_timeout
    
    @property
    def success_threshold(self) -> int:
        """Get the success threshold."""
        return self.config.success_threshold
        
    def __call__(self, func: Callable) -> Callable:
        """Decorator to protect a function with circuit breaker."""
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.
        
        Parameters
        ----------
        func : Callable
            Function to execute
        *args, **kwargs
            Arguments to pass to function
            
        Returns
        -------
        Any
            Function result
            
        Raises
        ------
        CircuitBreakerError
            When circuit is open
        """
        with self._lock:
            self.metrics.total_requests += 1
            
            # Check if circuit should transition states
            self._update_state()
            
            if self.state == CircuitBreakerState.OPEN:
                self._logger.warning(f"Circuit breaker {self.name} is OPEN - failing fast")
                raise CircuitBreakerError(f"Circuit breaker {self.name} is open")
            
            # Execute the function
            start_time = time.time()
            try:
                # Set timeout for operation
                result = self._execute_with_timeout(func, args, kwargs)
                
                # Record success
                self._record_success()
                execution_time = time.time() - start_time
                self._logger.debug(f"Circuit breaker {self.name} - Success in {execution_time:.2f}s")
                
                return result
                
            except self.config.expected_exception as e:
                # Record failure
                self._record_failure()
                execution_time = time.time() - start_time
                self._logger.warning(f"Circuit breaker {self.name} - Failure in {execution_time:.2f}s: {e}")
                raise
            
    def _execute_with_timeout(self, func: Callable, args: tuple, kwargs: dict) -> Any:
        """Execute function with timeout protection."""
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Operation timed out after {self.config.timeout}s")
        
        # Set timeout (Unix-like systems)
        if hasattr(signal, 'SIGALRM'):
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(self.config.timeout))
            
            try:
                result = func(*args, **kwargs)
                signal.alarm(0)  # Cancel alarm
                return result
            finally:
                signal.signal(signal.SIGALRM, old_handler)
        else:
            # Fallback for Windows - no timeout protection
            return func(*args, **kwargs)
    
    def _update_state(self) -> None:
        """Update circuit breaker state based on current conditions."""
        current_time = time.time()
        
        if self.state == CircuitBreakerState.OPEN:
            # Check if we should try half-open
            if (self._last_failure_time and 
                current_time - self._last_failure_time >= self.config.recovery_timeout):
                self._transition_to_half_open()
                
        elif self.state == CircuitBreakerState.HALF_OPEN:
            # Check if we should close (enough successes)
            if self._success_count >= self.config.success_threshold:
                self._transition_to_closed()
    
    def _record_success(self) -> None:
        """Record a successful operation."""
        self.metrics.successful_requests += 1
        
        if self.state == CircuitBreakerState.HALF_OPEN:
            self._success_count += 1
            # Check if we should transition to closed immediately
            if self._success_count >= self.config.success_threshold:
                self._transition_to_closed()
        elif self.state == CircuitBreakerState.CLOSED:
            # Reset failure count on success
            self._failure_count = 0
    
    def _record_failure(self) -> None:
        """Record a failed operation."""
        self.metrics.failed_requests += 1
        self.metrics.recent_failures.append(time.time())
        self._last_failure_time = time.time()
        self.metrics.last_failure_time = self._last_failure_time
        
        if self.state == CircuitBreakerState.CLOSED:
            self._failure_count += 1
            if self._failure_count >= self.config.failure_threshold:
                self._transition_to_open()
        elif self.state == CircuitBreakerState.HALF_OPEN:
            # Any failure in half-open goes back to open
            self._transition_to_open()
    
    def _transition_to_open(self) -> None:
        """Transition to OPEN state."""
        self.state = CircuitBreakerState.OPEN
        self.metrics.circuit_open_count += 1
        self._logger.error(f"Circuit breaker {self.name} transitioned to OPEN")
    
    def _transition_to_half_open(self) -> None:
        """Transition to HALF_OPEN state."""
        self.state = CircuitBreakerState.HALF_OPEN
        self._success_count = 0
        self._logger.info(f"Circuit breaker {self.name} transitioned to HALF_OPEN")
    
    def _transition_to_closed(self) -> None:
        """Transition to CLOSED state."""
        self.state = CircuitBreakerState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._logger.info(f"Circuit breaker {self.name} transitioned to CLOSED")
    
    def reset(self) -> None:
        """Manually reset circuit breaker to CLOSED state."""
        with self._lock:
            self.state = CircuitBreakerState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._last_failure_time = None
            self._logger.info(f"Circuit breaker {self.name} manually reset to CLOSED")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics and state information."""
        with self._lock:
            return {
                "name": self.name,
                "state": self.state.value,
                "total_requests": self.metrics.total_requests,
                "successful_requests": self.metrics.successful_requests,
                "failed_requests": self.metrics.failed_requests,
                "success_rate": (
                    self.metrics.successful_requests / self.metrics.total_requests 
                    if self.metrics.total_requests > 0 else 0
                ),
                "failure_count": self._failure_count,
                "success_count": self._success_count,
                "circuit_open_count": self.metrics.circuit_open_count,
                "last_failure_time": self.metrics.last_failure_time,
                "recent_failures_count": len(self.metrics.recent_failures),
                "config": {
                    "failure_threshold": self.config.failure_threshold,
                    "recovery_timeout": self.config.recovery_timeout,
                    "success_threshold": self.config.success_threshold,
                    "timeout": self.config.timeout
                }
            }


# Global circuit breaker registry for monitoring
_circuit_breakers: Dict[str, CircuitBreaker] = {}


def get_circuit_breaker(name: str, **kwargs) -> CircuitBreaker:
    """Get or create a named circuit breaker."""
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(name=name, **kwargs)
    return _circuit_breakers[name]


def get_all_circuit_breakers() -> Dict[str, CircuitBreaker]:
    """Get all registered circuit breakers."""
    return _circuit_breakers.copy()


def reset_all_circuit_breakers() -> None:
    """Reset all circuit breakers to CLOSED state."""
    for breaker in _circuit_breakers.values():
        breaker.reset() 