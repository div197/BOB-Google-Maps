"""bob_core.retry_strategy

Intelligent retry strategies with exponential backoff and jitter.
Implements resilient patterns following Niṣkāma Karma Yoga principles.
"""
from __future__ import annotations

import time
import random
import logging
from typing import Callable, Any, Optional, Type, Union, List
from dataclasses import dataclass
from enum import Enum
import functools

__all__ = [
    "RetryStrategy", 
    "ExponentialBackoff", 
    "LinearBackoff",
    "FixedBackoff",
    "RetryError",
    "retry_with_backoff"
]


class BackoffType(Enum):
    """Types of backoff strategies."""
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    FIXED = "fixed"


class RetryError(Exception):
    """Raised when all retry attempts are exhausted."""
    
    def __init__(self, message: str, attempts: int, last_exception: Exception):
        super().__init__(message)
        self.attempts = attempts
        self.last_exception = last_exception


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    backoff_multiplier: float = 2.0
    jitter: bool = True
    jitter_range: float = 0.1
    exceptions: tuple = (Exception,)
    on_retry: Optional[Callable] = None


class RetryStrategy:
    """Base class for retry strategies."""
    
    def __init__(self, config: RetryConfig):
        self.config = config
        self._logger = logging.getLogger("bob_core.retry_strategy")
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number."""
        raise NotImplementedError
    
    def should_retry(self, exception: Exception, attempt: int) -> bool:
        """Determine if we should retry based on exception and attempt count."""
        if attempt >= self.config.max_attempts:
            return False
        
        return isinstance(exception, self.config.exceptions)
    
    def add_jitter(self, delay: float) -> float:
        """Add jitter to delay to prevent thundering herd."""
        if not self.config.jitter:
            return delay
        
        jitter_amount = delay * self.config.jitter_range
        jitter = random.uniform(-jitter_amount, jitter_amount)
        return max(0, delay + jitter)
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry logic."""
        last_exception = None
        
        for attempt in range(1, self.config.max_attempts + 1):
            try:
                self._logger.debug(f"Attempt {attempt}/{self.config.max_attempts}")
                result = func(*args, **kwargs)
                
                if attempt > 1:
                    self._logger.info(f"Success on attempt {attempt}")
                
                return result
                
            except Exception as e:
                last_exception = e
                
                if not self.should_retry(e, attempt):
                    self._logger.error(f"Not retrying after attempt {attempt}: {e}")
                    break
                
                if attempt < self.config.max_attempts:
                    delay = self.calculate_delay(attempt)
                    delay_with_jitter = self.add_jitter(delay)
                    
                    self._logger.warning(
                        f"Attempt {attempt} failed: {e}. "
                        f"Retrying in {delay_with_jitter:.2f}s"
                    )
                    
                    # Call retry callback if provided
                    if self.config.on_retry:
                        self.config.on_retry(attempt, e, delay_with_jitter)
                    
                    time.sleep(delay_with_jitter)
                else:
                    self._logger.error(f"Final attempt {attempt} failed: {e}")
        
        # All attempts exhausted
        raise RetryError(
            f"All {self.config.max_attempts} attempts failed",
            self.config.max_attempts,
            last_exception
        )


class ExponentialBackoff(RetryStrategy):
    """Exponential backoff retry strategy."""
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        delay = self.config.base_delay * (self.config.backoff_multiplier ** (attempt - 1))
        return min(delay, self.config.max_delay)


class LinearBackoff(RetryStrategy):
    """Linear backoff retry strategy."""
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate linear backoff delay."""
        delay = self.config.base_delay * attempt
        return min(delay, self.config.max_delay)


class FixedBackoff(RetryStrategy):
    """Fixed delay retry strategy."""
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate fixed delay."""
        return min(self.config.base_delay, self.config.max_delay)


def create_retry_strategy(
    strategy_type: Union[BackoffType, str] = BackoffType.EXPONENTIAL,
    **config_kwargs
) -> RetryStrategy:
    """Factory function to create retry strategies."""
    config = RetryConfig(**config_kwargs)
    
    if isinstance(strategy_type, str):
        strategy_type = BackoffType(strategy_type)
    
    if strategy_type == BackoffType.EXPONENTIAL:
        return ExponentialBackoff(config)
    elif strategy_type == BackoffType.LINEAR:
        return LinearBackoff(config)
    elif strategy_type == BackoffType.FIXED:
        return FixedBackoff(config)
    else:
        raise ValueError(f"Unknown strategy type: {strategy_type}")


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_multiplier: float = 2.0,
    jitter: bool = True,
    jitter_range: float = 0.1,
    exceptions: tuple = (Exception,),
    strategy: Union[BackoffType, str] = BackoffType.EXPONENTIAL,
    on_retry: Optional[Callable] = None
):
    """
    Decorator for adding retry logic with backoff to functions.
    
    Parameters
    ----------
    max_attempts : int
        Maximum number of retry attempts
    base_delay : float
        Base delay in seconds
    max_delay : float
        Maximum delay in seconds
    backoff_multiplier : float
        Multiplier for exponential backoff
    jitter : bool
        Whether to add jitter to delays
    jitter_range : float
        Jitter range as fraction of delay
    exceptions : tuple
        Exception types to retry on
    strategy : BackoffType or str
        Backoff strategy to use
    on_retry : Callable
        Callback function called on each retry
    
    Example:
        ```python
        @retry_with_backoff(max_attempts=5, base_delay=2.0)
        def unreliable_api_call():
            response = requests.get("https://api.example.com/data")
            response.raise_for_status()
            return response.json()
        
        # With custom retry callback
        def log_retry(attempt, exception, delay):
            print(f"Retry {attempt}: {exception}, waiting {delay}s")
        
        @retry_with_backoff(
            max_attempts=3,
            exceptions=(requests.RequestException,),
            on_retry=log_retry
        )
        def api_call_with_logging():
            return requests.get("https://api.example.com/data")
        ```
    """
    def decorator(func: Callable) -> Callable:
        retry_strategy = create_retry_strategy(
            strategy_type=strategy,
            max_attempts=max_attempts,
            base_delay=base_delay,
            max_delay=max_delay,
            backoff_multiplier=backoff_multiplier,
            jitter=jitter,
            jitter_range=jitter_range,
            exceptions=exceptions,
            on_retry=on_retry
        )
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return retry_strategy.execute(func, *args, **kwargs)
        
        # Add retry strategy as attribute for introspection
        wrapper._retry_strategy = retry_strategy
        
        return wrapper
    
    return decorator


class AdaptiveRetryStrategy(RetryStrategy):
    """
    Adaptive retry strategy that adjusts based on success/failure patterns.
    
    This strategy learns from past attempts and adjusts its behavior:
    - Increases delays if failures are frequent
    - Decreases delays if success rate is high
    - Tracks success patterns for different error types
    """
    
    def __init__(self, config: RetryConfig):
        super().__init__(config)
        self._success_history: List[bool] = []
        self._error_patterns: dict = {}
        self._adaptive_multiplier = 1.0
        self._max_history = 100
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate adaptive delay based on historical performance."""
        base_delay = self.config.base_delay * (
            self.config.backoff_multiplier ** (attempt - 1)
        )
        
        # Apply adaptive multiplier based on recent success rate
        adaptive_delay = base_delay * self._adaptive_multiplier
        
        return min(adaptive_delay, self.config.max_delay)
    
    def _update_adaptive_multiplier(self, success: bool):
        """Update adaptive multiplier based on operation outcome."""
        self._success_history.append(success)
        
        # Keep only recent history
        if len(self._success_history) > self._max_history:
            self._success_history = self._success_history[-self._max_history:]
        
        # Calculate recent success rate
        if len(self._success_history) >= 10:  # Need minimum samples
            recent_success_rate = sum(self._success_history[-20:]) / min(20, len(self._success_history))
            
            if recent_success_rate > 0.8:
                # High success rate - reduce delays
                self._adaptive_multiplier = max(0.5, self._adaptive_multiplier * 0.9)
            elif recent_success_rate < 0.3:
                # Low success rate - increase delays
                self._adaptive_multiplier = min(3.0, self._adaptive_multiplier * 1.2)
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute with adaptive retry logic."""
        try:
            result = super().execute(func, *args, **kwargs)
            self._update_adaptive_multiplier(True)
            return result
        except RetryError:
            self._update_adaptive_multiplier(False)
            raise


# Predefined retry strategies for common use cases
def web_scraping_retry():
    """Retry strategy optimized for web scraping operations."""
    return create_retry_strategy(
        strategy_type=BackoffType.EXPONENTIAL,
        max_attempts=5,
        base_delay=2.0,
        max_delay=30.0,
        backoff_multiplier=1.5,
        jitter=True,
        jitter_range=0.2,
        exceptions=(Exception,)  # Catch all for web scraping
    )


def api_call_retry():
    """Retry strategy optimized for API calls."""
    return create_retry_strategy(
        strategy_type=BackoffType.EXPONENTIAL,
        max_attempts=3,
        base_delay=1.0,
        max_delay=10.0,
        backoff_multiplier=2.0,
        jitter=True,
        jitter_range=0.1
    )


def database_retry():
    """Retry strategy optimized for database operations."""
    return create_retry_strategy(
        strategy_type=BackoffType.LINEAR,
        max_attempts=3,
        base_delay=0.5,
        max_delay=5.0,
        jitter=True,
        jitter_range=0.05
    ) 