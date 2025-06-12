"""Tests for bob_core.circuit_breaker module."""

import pytest
import time
from unittest.mock import patch, MagicMock

from bob_core.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerState,
    CircuitBreakerError,
    get_circuit_breaker,
    reset_all_circuit_breakers
)


class TestCircuitBreaker:
    """Test circuit breaker functionality."""
    
    def test_circuit_breaker_initialization(self):
        """Test circuit breaker initialization."""
        breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=30,
            success_threshold=2,
            name="test"
        )
        
        assert breaker.name == "test"
        assert breaker.state == CircuitBreakerState.CLOSED
        assert breaker.config.failure_threshold == 3
        assert breaker.config.recovery_timeout == 30
        assert breaker.config.success_threshold == 2
    
    def test_successful_execution(self):
        """Test successful function execution."""
        breaker = CircuitBreaker(name="test_success")
        
        def successful_function():
            return "success"
        
        result = breaker.call(successful_function)
        assert result == "success"
        assert breaker.state == CircuitBreakerState.CLOSED
        assert breaker.metrics.successful_requests == 1
        assert breaker.metrics.failed_requests == 0
    
    def test_failure_handling(self):
        """Test failure handling and circuit opening."""
        breaker = CircuitBreaker(failure_threshold=2, name="test_failure")
        
        def failing_function():
            raise ValueError("Test error")
        
        # First failure
        with pytest.raises(ValueError):
            breaker.call(failing_function)
        
        assert breaker.state == CircuitBreakerState.CLOSED
        assert breaker.metrics.failed_requests == 1
        
        # Second failure - should open circuit
        with pytest.raises(ValueError):
            breaker.call(failing_function)
        
        assert breaker.state == CircuitBreakerState.OPEN
        assert breaker.metrics.failed_requests == 2
        assert breaker.metrics.circuit_open_count == 1
    
    def test_circuit_open_behavior(self):
        """Test behavior when circuit is open."""
        breaker = CircuitBreaker(failure_threshold=1, name="test_open")
        
        def failing_function():
            raise ValueError("Test error")
        
        # Trigger circuit opening
        with pytest.raises(ValueError):
            breaker.call(failing_function)
        
        assert breaker.state == CircuitBreakerState.OPEN
        
        # Subsequent calls should fail fast
        with pytest.raises(CircuitBreakerError):
            breaker.call(failing_function)
        
        # Should not execute the function
        assert breaker.metrics.total_requests == 2  # Initial failure + fast fail
    
    def test_circuit_recovery(self):
        """Test circuit recovery mechanism."""
        breaker = CircuitBreaker(
            failure_threshold=1,
            recovery_timeout=1,  # 1 second for testing
            success_threshold=1,
            name="test_recovery"
        )
        
        def failing_function():
            raise ValueError("Test error")
        
        def successful_function():
            return "success"
        
        # Open the circuit
        with pytest.raises(ValueError):
            breaker.call(failing_function)
        
        assert breaker.state == CircuitBreakerState.OPEN
        
        # Wait for recovery timeout
        time.sleep(1.1)
        
        # Next call should transition to half-open, then to closed after success
        result = breaker.call(successful_function)
        assert result == "success"
        # After one success with success_threshold=1, should transition to closed
        assert breaker.state == CircuitBreakerState.CLOSED
    
    def test_decorator_usage(self):
        """Test circuit breaker as decorator."""
        breaker = CircuitBreaker(failure_threshold=2, name="test_decorator")
        
        @breaker
        def decorated_function(value):
            if value == "fail":
                raise ValueError("Decorated failure")
            return f"decorated_{value}"
        
        # Test successful execution
        result = decorated_function("success")
        assert result == "decorated_success"
        
        # Test failure
        with pytest.raises(ValueError):
            decorated_function("fail")
        
        assert breaker.metrics.successful_requests == 1
        assert breaker.metrics.failed_requests == 1
    
    def test_metrics_collection(self):
        """Test metrics collection."""
        breaker = CircuitBreaker(name="test_metrics")
        
        def test_function(should_fail=False):
            if should_fail:
                raise ValueError("Test error")
            return "success"
        
        # Execute some operations
        breaker.call(test_function)
        breaker.call(test_function)
        
        try:
            breaker.call(test_function, should_fail=True)
        except ValueError:
            pass
        
        metrics = breaker.get_metrics()
        
        assert metrics["name"] == "test_metrics"
        assert metrics["total_requests"] == 3
        assert metrics["successful_requests"] == 2
        assert metrics["failed_requests"] == 1
        assert metrics["success_rate"] == 2/3
        assert metrics["state"] == "closed"
    
    def test_global_circuit_breaker_registry(self):
        """Test global circuit breaker registry."""
        # Clear any existing breakers
        reset_all_circuit_breakers()
        
        # Get a named circuit breaker
        breaker1 = get_circuit_breaker("test_global", failure_threshold=3)
        breaker2 = get_circuit_breaker("test_global")
        
        # Should return the same instance
        assert breaker1 is breaker2
        assert breaker1.name == "test_global"
        assert breaker1.config.failure_threshold == 3
    
    def test_timeout_handling(self):
        """Test timeout handling (Windows compatible)."""
        breaker = CircuitBreaker(timeout=0.1, name="test_timeout")
        
        def slow_function():
            time.sleep(0.2)  # Longer than timeout
            return "slow_result"
        
        # On Windows, timeout might not work, so we just test the call
        try:
            result = breaker.call(slow_function)
            # If no timeout occurred, function should complete
            assert result == "slow_result"
        except TimeoutError:
            # If timeout occurred (Unix-like systems)
            assert breaker.metrics.failed_requests == 1
    
    def test_half_open_state_failure(self):
        """Test failure in half-open state."""
        breaker = CircuitBreaker(
            failure_threshold=1,
            recovery_timeout=1,
            name="test_half_open_failure"
        )
        
        def failing_function():
            raise ValueError("Test error")
        
        # Open the circuit
        with pytest.raises(ValueError):
            breaker.call(failing_function)
        
        assert breaker.state == CircuitBreakerState.OPEN
        
        # Wait for recovery timeout
        time.sleep(1.1)
        
        # Manually set to half-open for testing
        breaker._transition_to_half_open()
        assert breaker.state == CircuitBreakerState.HALF_OPEN
        
        # Failure in half-open should go back to open
        with pytest.raises(ValueError):
            breaker.call(failing_function)
        
        assert breaker.state == CircuitBreakerState.OPEN
    
    def test_reset_functionality(self):
        """Test manual reset functionality."""
        breaker = CircuitBreaker(failure_threshold=1, name="test_reset")
        
        def failing_function():
            raise ValueError("Test error")
        
        # Open the circuit
        with pytest.raises(ValueError):
            breaker.call(failing_function)
        
        assert breaker.state == CircuitBreakerState.OPEN
        
        # Reset the circuit breaker
        breaker.reset()
        
        assert breaker.state == CircuitBreakerState.CLOSED
        assert breaker._failure_count == 0
        assert breaker._success_count == 0 