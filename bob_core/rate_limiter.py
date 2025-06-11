"""bob_core.rate_limiter

Rate limiting utilities to prevent overwhelming target servers.
"""
from __future__ import annotations

import time
import random
from typing import Optional, Dict, Any
from threading import Lock
from collections import defaultdict, deque
from datetime import datetime, timedelta

__all__ = ["RateLimiter", "AdaptiveRateLimiter", "DomainRateLimiter"]


class RateLimiter:
    """Simple rate limiter with fixed delay."""
    
    def __init__(self, delay: float = 1.0, jitter: float = 0.1):
        """
        Initialize rate limiter.
        
        Parameters
        ----------
        delay : float
            Base delay between requests in seconds
        jitter : float
            Random jitter factor (0.0 to 1.0)
        """
        self.delay = delay
        self.jitter = jitter
        self.last_request = 0.0
        self._lock = Lock()
    
    def wait(self) -> None:
        """Wait for appropriate delay before next request."""
        with self._lock:
            now = time.time()
            elapsed = now - self.last_request
            
            # Calculate delay with jitter
            actual_delay = self.delay
            if self.jitter > 0:
                jitter_amount = random.uniform(-self.jitter, self.jitter) * self.delay
                actual_delay += jitter_amount
            
            if elapsed < actual_delay:
                sleep_time = actual_delay - elapsed
                time.sleep(sleep_time)
            
            self.last_request = time.time()


class AdaptiveRateLimiter:
    """Adaptive rate limiter that adjusts based on response times and errors."""
    
    def __init__(
        self,
        initial_delay: float = 1.0,
        min_delay: float = 0.5,
        max_delay: float = 10.0,
        backoff_factor: float = 1.5,
        recovery_factor: float = 0.9
    ):
        """
        Initialize adaptive rate limiter.
        
        Parameters
        ----------
        initial_delay : float
            Initial delay between requests
        min_delay : float
            Minimum delay allowed
        max_delay : float
            Maximum delay allowed
        backoff_factor : float
            Factor to increase delay on errors
        recovery_factor : float
            Factor to decrease delay on success
        """
        self.current_delay = initial_delay
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.recovery_factor = recovery_factor
        self.last_request = 0.0
        self.consecutive_successes = 0
        self.consecutive_errors = 0
        self._lock = Lock()
    
    def wait(self) -> None:
        """Wait for appropriate delay before next request."""
        with self._lock:
            now = time.time()
            elapsed = now - self.last_request
            
            if elapsed < self.current_delay:
                sleep_time = self.current_delay - elapsed
                time.sleep(sleep_time)
            
            self.last_request = time.time()
    
    def report_success(self, response_time: Optional[float] = None) -> None:
        """Report successful request to adjust rate limiting."""
        with self._lock:
            self.consecutive_successes += 1
            self.consecutive_errors = 0
            
            # Gradually decrease delay on consecutive successes
            if self.consecutive_successes >= 5:
                self.current_delay *= self.recovery_factor
                self.current_delay = max(self.current_delay, self.min_delay)
                self.consecutive_successes = 0
    
    def report_error(self, error_type: str = "unknown") -> None:
        """Report error to adjust rate limiting."""
        with self._lock:
            self.consecutive_errors += 1
            self.consecutive_successes = 0
            
            # Increase delay on errors
            if error_type in ["rate_limit", "timeout", "server_error"]:
                self.current_delay *= self.backoff_factor
                self.current_delay = min(self.current_delay, self.max_delay)
    
    def get_current_delay(self) -> float:
        """Get current delay setting."""
        return self.current_delay


class DomainRateLimiter:
    """Rate limiter that tracks requests per domain."""
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        burst_size: int = 10,
        default_delay: float = 1.0
    ):
        """
        Initialize domain-based rate limiter.
        
        Parameters
        ----------
        requests_per_minute : int
            Maximum requests per minute per domain
        burst_size : int
            Maximum burst requests allowed
        default_delay : float
            Default delay between requests
        """
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size
        self.default_delay = default_delay
        
        # Track requests per domain
        self.domain_requests: Dict[str, deque] = defaultdict(deque)
        self.domain_locks: Dict[str, Lock] = defaultdict(Lock)
    
    def wait(self, domain: str) -> None:
        """Wait for appropriate delay for the given domain."""
        with self.domain_locks[domain]:
            now = datetime.now()
            requests = self.domain_requests[domain]
            
            # Remove old requests (older than 1 minute)
            cutoff = now - timedelta(minutes=1)
            while requests and requests[0] < cutoff:
                requests.popleft()
            
            # Check if we need to wait
            if len(requests) >= self.requests_per_minute:
                # Wait until oldest request is more than 1 minute old
                oldest_request = requests[0]
                wait_until = oldest_request + timedelta(minutes=1)
                wait_time = (wait_until - now).total_seconds()
                
                if wait_time > 0:
                    time.sleep(wait_time)
            
            elif len(requests) >= self.burst_size:
                # Apply default delay for burst control
                time.sleep(self.default_delay)
            
            # Record this request
            requests.append(now)
    
    def get_domain_stats(self, domain: str) -> Dict[str, Any]:
        """Get statistics for a domain."""
        with self.domain_locks[domain]:
            requests = self.domain_requests[domain]
            now = datetime.now()
            
            # Count recent requests
            cutoff = now - timedelta(minutes=1)
            recent_requests = sum(1 for req_time in requests if req_time >= cutoff)
            
            return {
                "domain": domain,
                "requests_last_minute": recent_requests,
                "total_requests": len(requests),
                "rate_limit": self.requests_per_minute,
                "burst_limit": self.burst_size
            } 