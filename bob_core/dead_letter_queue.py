"""bob_core.dead_letter_queue

Dead Letter Queue implementation for handling permanently failed requests.
Follows the principles of Niṣkāma Karma Yoga - selfless service with perfect execution.
"""
from __future__ import annotations

import json
import time
import threading
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
import logging
import pickle
from collections import deque

__all__ = ["DeadLetterQueue", "FailedRequest", "FailureReason", "DLQProcessor"]


class FailureReason(Enum):
    """Reasons for request failure."""
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    INVALID_RESPONSE = "invalid_response"
    NETWORK_ERROR = "network_error"
    PARSING_ERROR = "parsing_error"
    AUTHENTICATION_ERROR = "authentication_error"
    QUOTA_EXCEEDED = "quota_exceeded"
    PERMANENT_FAILURE = "permanent_failure"
    UNKNOWN_ERROR = "unknown_error"


@dataclass
class FailedRequest:
    """Represents a failed request in the dead letter queue."""
    id: str
    url: str
    failure_reason: FailureReason
    error_message: str
    timestamp: float
    retry_count: int = 0
    max_retries: int = 3
    original_data: Optional[Dict[str, Any]] = None
    stack_trace: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "url": self.url,
            "failure_reason": self.failure_reason.value,
            "error_message": self.error_message,
            "timestamp": self.timestamp,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "original_data": self.original_data,
            "stack_trace": self.stack_trace,
            "context": self.context
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FailedRequest':
        """Create from dictionary."""
        return cls(
            id=data["id"],
            url=data["url"],
            failure_reason=FailureReason(data["failure_reason"]),
            error_message=data["error_message"],
            timestamp=data["timestamp"],
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            original_data=data.get("original_data"),
            stack_trace=data.get("stack_trace"),
            context=data.get("context", {})
        )
    
    def is_retryable(self) -> bool:
        """Check if request can be retried."""
        if self.retry_count >= self.max_retries:
            return False
        
        # Some failures are not retryable
        non_retryable = {
            FailureReason.AUTHENTICATION_ERROR,
            FailureReason.PERMANENT_FAILURE,
            FailureReason.INVALID_RESPONSE
        }
        
        return self.failure_reason not in non_retryable
    
    def should_retry_now(self, backoff_multiplier: float = 2.0) -> bool:
        """Check if enough time has passed for retry."""
        if not self.is_retryable():
            return False
        
        # Exponential backoff: 1min, 2min, 4min, 8min...
        backoff_seconds = 60 * (backoff_multiplier ** self.retry_count)
        time_since_failure = time.time() - self.timestamp
        
        return time_since_failure >= backoff_seconds


class DeadLetterQueue:
    """
    Dead Letter Queue for handling permanently failed requests.
    
    Features:
    - Persistent storage of failed requests
    - Automatic retry with exponential backoff
    - Failure reason categorization
    - Metrics and analytics
    - Configurable retention policies
    
    Example:
        ```python
        dlq = DeadLetterQueue("failed_requests.json")
        
        # Add failed request
        failed_req = FailedRequest(
            id="req_123",
            url="https://maps.google.com/place/123",
            failure_reason=FailureReason.TIMEOUT,
            error_message="Request timed out after 30s",
            timestamp=time.time()
        )
        dlq.add_failed_request(failed_req)
        
        # Process retryable requests
        retryable = dlq.get_retryable_requests()
        for req in retryable:
            try:
                # Retry the request
                result = retry_scraping(req.url)
                dlq.mark_resolved(req.id)
            except Exception as e:
                dlq.increment_retry_count(req.id)
        ```
    """
    
    def __init__(self, 
                 storage_path: str = "dead_letter_queue.json",
                 max_queue_size: int = 10000,
                 retention_days: int = 30):
        """
        Initialize Dead Letter Queue.
        
        Parameters
        ----------
        storage_path : str
            Path to persistent storage file
        max_queue_size : int
            Maximum number of failed requests to store
        retention_days : int
            Days to retain resolved/expired requests
        """
        self.storage_path = Path(storage_path)
        self.max_queue_size = max_queue_size
        self.retention_days = retention_days
        self._lock = threading.RLock()
        self._failed_requests: Dict[str, FailedRequest] = {}
        self._resolved_requests: Dict[str, FailedRequest] = {}
        self._logger = logging.getLogger("bob_core.dead_letter_queue")
        
        # Load existing data
        self._load_from_storage()
        
        # Start background cleanup
        self._cleanup_thread = threading.Thread(target=self._periodic_cleanup, daemon=True)
        self._cleanup_thread.start()
    
    def add_failed_request(self, failed_request) -> None:
        """Add a failed request to the queue."""
        with self._lock:
            # Handle both FailedRequest objects and dictionaries
            if isinstance(failed_request, dict):
                # Convert dictionary to FailedRequest object
                failed_req = FailedRequest(
                    id=failed_request["id"],
                    url=failed_request["url"],
                    failure_reason=failed_request["failure_reason"],
                    error_message=failed_request["error_message"],
                    timestamp=failed_request["timestamp"],
                    retry_count=failed_request.get("retry_count", 0),
                    max_retries=failed_request.get("max_retries", 3),
                    original_data=failed_request.get("original_data"),
                    stack_trace=failed_request.get("stack_trace"),
                    context=failed_request.get("context", {})
                )
            else:
                failed_req = failed_request
            
            # Check queue size limit
            if len(self._failed_requests) >= self.max_queue_size:
                self._cleanup_old_requests()
            
            self._failed_requests[failed_req.id] = failed_req
            self._logger.warning(f"Added failed request {failed_req.id}: {failed_req.failure_reason.value}")
            
            # Save to storage
            self._save_to_storage()
    
    def get_failed_request(self, request_id: str) -> Optional[FailedRequest]:
        """Get a specific failed request by ID."""
        with self._lock:
            return self._failed_requests.get(request_id)
    
    def get_all_failed_requests(self) -> List[FailedRequest]:
        """Get all failed requests."""
        with self._lock:
            return list(self._failed_requests.values())
    
    def get_retryable_requests(self) -> List[FailedRequest]:
        """Get requests that can be retried now."""
        with self._lock:
            retryable = []
            for req in self._failed_requests.values():
                if req.should_retry_now():
                    retryable.append(req)
            return retryable
    
    def increment_retry_count(self, request_id: str) -> bool:
        """Increment retry count for a request."""
        with self._lock:
            if request_id in self._failed_requests:
                req = self._failed_requests[request_id]
                req.retry_count += 1
                req.timestamp = time.time()  # Update timestamp for backoff calculation
                
                self._logger.info(f"Incremented retry count for {request_id}: {req.retry_count}/{req.max_retries}")
                self._save_to_storage()
                return True
            return False
    
    def mark_resolved(self, request_id: str) -> bool:
        """Mark a request as successfully resolved."""
        with self._lock:
            if request_id in self._failed_requests:
                resolved_req = self._failed_requests.pop(request_id)
                resolved_req.timestamp = time.time()  # Update to resolution time
                self._resolved_requests[request_id] = resolved_req
                
                self._logger.info(f"Marked request {request_id} as resolved")
                self._save_to_storage()
                return True
            return False
    
    def remove_request(self, request_id: str) -> bool:
        """Permanently remove a request from the queue."""
        with self._lock:
            removed = False
            if request_id in self._failed_requests:
                del self._failed_requests[request_id]
                removed = True
            if request_id in self._resolved_requests:
                del self._resolved_requests[request_id]
                removed = True
            
            if removed:
                self._logger.info(f"Permanently removed request {request_id}")
                self._save_to_storage()
            
            return removed
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get queue statistics and metrics."""
        with self._lock:
            # Count by failure reason
            failure_counts = {}
            for req in self._failed_requests.values():
                reason = req.failure_reason.value
                failure_counts[reason] = failure_counts.get(reason, 0) + 1
            
            # Retry statistics
            retry_stats = {
                "no_retries": 0,
                "some_retries": 0,
                "max_retries": 0
            }
            
            for req in self._failed_requests.values():
                if req.retry_count == 0:
                    retry_stats["no_retries"] += 1
                elif req.retry_count >= req.max_retries:
                    retry_stats["max_retries"] += 1
                else:
                    retry_stats["some_retries"] += 1
            
            # Age statistics
            current_time = time.time()
            ages = [(current_time - req.timestamp) / 3600 for req in self._failed_requests.values()]  # Hours
            
            return {
                "total_failed": len(self._failed_requests),
                "total_resolved": len(self._resolved_requests),
                "retryable_now": len(self.get_retryable_requests()),
                "failure_reasons": failure_counts,
                "retry_statistics": retry_stats,
                "age_statistics": {
                    "oldest_hours": max(ages) if ages else 0,
                    "newest_hours": min(ages) if ages else 0,
                    "average_hours": sum(ages) / len(ages) if ages else 0
                },
                "storage_path": str(self.storage_path),
                "queue_size_limit": self.max_queue_size,
                "retention_days": self.retention_days
            }
    
    def export_failed_requests(self, output_path: str, format: str = "json") -> None:
        """Export failed requests to file."""
        with self._lock:
            data = {
                "failed_requests": [req.to_dict() for req in self._failed_requests.values()],
                "resolved_requests": [req.to_dict() for req in self._resolved_requests.values()],
                "export_timestamp": time.time(),
                "statistics": self.get_statistics()
            }
            
            output_file = Path(output_path)
            
            if format.lower() == "json":
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif format.lower() == "pickle":
                with open(output_file, 'wb') as f:
                    pickle.dump(data, f)
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            self._logger.info(f"Exported {len(self._failed_requests)} failed requests to {output_file}")
    
    def _load_from_storage(self) -> None:
        """Load failed requests from persistent storage."""
        if not self.storage_path.exists():
            return
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load failed requests
            for req_data in data.get("failed_requests", []):
                req = FailedRequest.from_dict(req_data)
                self._failed_requests[req.id] = req
            
            # Load resolved requests
            for req_data in data.get("resolved_requests", []):
                req = FailedRequest.from_dict(req_data)
                self._resolved_requests[req.id] = req
            
            self._logger.info(f"Loaded {len(self._failed_requests)} failed requests from storage")
            
        except Exception as e:
            self._logger.error(f"Failed to load from storage: {e}")
    
    def _save_to_storage(self) -> None:
        """Save failed requests to persistent storage."""
        try:
            data = {
                "failed_requests": [req.to_dict() for req in self._failed_requests.values()],
                "resolved_requests": [req.to_dict() for req in self._resolved_requests.values()],
                "last_updated": time.time()
            }
            
            # Atomic write
            temp_path = self.storage_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            temp_path.replace(self.storage_path)
            
        except Exception as e:
            self._logger.error(f"Failed to save to storage: {e}")
    
    def _cleanup_old_requests(self) -> None:
        """Clean up old requests to maintain queue size."""
        if len(self._failed_requests) <= self.max_queue_size:
            return
        
        # Remove oldest requests that have exceeded max retries
        expired_requests = []
        for req_id, req in self._failed_requests.items():
            if req.retry_count >= req.max_retries:
                age_days = (time.time() - req.timestamp) / (24 * 3600)
                if age_days > 1:  # Remove if older than 1 day and max retries exceeded
                    expired_requests.append(req_id)
        
        for req_id in expired_requests:
            del self._failed_requests[req_id]
            self._logger.info(f"Removed expired request {req_id}")
        
        # If still over limit, remove oldest requests
        if len(self._failed_requests) > self.max_queue_size:
            sorted_requests = sorted(
                self._failed_requests.items(),
                key=lambda x: x[1].timestamp
            )
            
            to_remove = len(self._failed_requests) - self.max_queue_size
            for req_id, _ in sorted_requests[:to_remove]:
                del self._failed_requests[req_id]
                self._logger.warning(f"Removed request {req_id} due to queue size limit")
    
    def _periodic_cleanup(self) -> None:
        """Periodic cleanup of old resolved requests."""
        while True:
            try:
                time.sleep(3600)  # Run every hour
                
                with self._lock:
                    current_time = time.time()
                    retention_seconds = self.retention_days * 24 * 3600
                    
                    # Clean up old resolved requests
                    expired_resolved = []
                    for req_id, req in self._resolved_requests.items():
                        if current_time - req.timestamp > retention_seconds:
                            expired_resolved.append(req_id)
                    
                    for req_id in expired_resolved:
                        del self._resolved_requests[req_id]
                    
                    if expired_resolved:
                        self._logger.info(f"Cleaned up {len(expired_resolved)} old resolved requests")
                        self._save_to_storage()
                
            except Exception as e:
                self._logger.error(f"Error in periodic cleanup: {e}")


class DLQProcessor:
    """
    Processor for handling Dead Letter Queue requests with retry logic.
    
    Example:
        ```python
        dlq = DeadLetterQueue()
        processor = DLQProcessor(dlq, retry_function=scrape_url)
        
        # Process retryable requests
        results = processor.process_retryable_requests()
        ```
    """
    
    def __init__(self, 
                 dlq: DeadLetterQueue,
                 retry_function: Callable[[str], Any],
                 max_concurrent: int = 3):
        """
        Initialize DLQ processor.
        
        Parameters
        ----------
        dlq : DeadLetterQueue
            Dead letter queue instance
        retry_function : Callable
            Function to retry failed requests
        max_concurrent : int
            Maximum concurrent retry attempts
        """
        self.dlq = dlq
        self.retry_function = retry_function
        self.max_concurrent = max_concurrent
        self._logger = logging.getLogger("bob_core.dlq_processor")
    
    def process_retryable_requests(self) -> Dict[str, Any]:
        """Process all retryable requests."""
        retryable = self.dlq.get_retryable_requests()
        
        if not retryable:
            return {"processed": 0, "succeeded": 0, "failed": 0}
        
        self._logger.info(f"Processing {len(retryable)} retryable requests")
        
        succeeded = 0
        failed = 0
        
        for req in retryable[:self.max_concurrent]:  # Limit concurrent processing
            try:
                # Attempt retry
                result = self.retry_function(req.url)
                
                # Mark as resolved
                self.dlq.mark_resolved(req.id)
                succeeded += 1
                
                self._logger.info(f"Successfully retried request {req.id}")
                
            except Exception as e:
                # Increment retry count
                self.dlq.increment_retry_count(req.id)
                failed += 1
                
                self._logger.warning(f"Retry failed for request {req.id}: {e}")
        
        return {
            "processed": len(retryable[:self.max_concurrent]),
            "succeeded": succeeded,
            "failed": failed,
            "remaining_retryable": len(retryable) - self.max_concurrent
        }
    
    def process_single_request(self, request_id: str) -> bool:
        """Process a single request by ID."""
        req = self.dlq.get_failed_request(request_id)
        if not req:
            return False
        
        if not req.should_retry_now():
            self._logger.warning(f"Request {request_id} is not ready for retry")
            return False
        
        try:
            result = self.retry_function(req.url)
            self.dlq.mark_resolved(req.id)
            self._logger.info(f"Successfully retried request {request_id}")
            return True
            
        except Exception as e:
            self.dlq.increment_retry_count(req.id)
            self._logger.warning(f"Retry failed for request {request_id}: {e}")
            return False


# Global DLQ instance for easy access
_global_dlq: Optional[DeadLetterQueue] = None


def get_global_dlq() -> DeadLetterQueue:
    """Get or create global Dead Letter Queue instance."""
    global _global_dlq
    if _global_dlq is None:
        _global_dlq = DeadLetterQueue()
    return _global_dlq


def add_failed_request(url: str, 
                      failure_reason: FailureReason,
                      error_message: str,
                      **kwargs) -> str:
    """Convenience function to add failed request to global DLQ."""
    import uuid
    
    request_id = str(uuid.uuid4())
    failed_req = FailedRequest(
        id=request_id,
        url=url,
        failure_reason=failure_reason,
        error_message=error_message,
        timestamp=time.time(),
        **kwargs
    )
    
    dlq = get_global_dlq()
    dlq.add_failed_request(failed_req)
    
    return request_id 