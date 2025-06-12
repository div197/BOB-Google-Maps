"""bob_core.performance_monitoring

Performance Monitoring system for tracking and optimizing system performance.
Follows the principles of Niṣkāma Karma Yoga - selfless service with perfect execution.
"""
from __future__ import annotations

import time
import threading
import logging
import psutil
import statistics
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections import deque, defaultdict
from contextlib import contextmanager
import functools

__all__ = [
    "PerformanceMonitor", "MetricCollector", "PerformanceProfiler",
    "SystemMetrics", "ApplicationMetrics", "PerformanceAlert",
    "Benchmark", "PerformanceOptimizer", "MetricThreshold"
]


@dataclass
class MetricThreshold:
    """Threshold configuration for performance metrics."""
    warning_value: float
    critical_value: float
    comparison: str = "greater"  # "greater", "less", "equal"
    
    def check_threshold(self, value: float) -> str:
        """Check if value exceeds thresholds."""
        if self.comparison == "greater":
            if value >= self.critical_value:
                return "critical"
            elif value >= self.warning_value:
                return "warning"
        elif self.comparison == "less":
            if value <= self.critical_value:
                return "critical"
            elif value <= self.warning_value:
                return "warning"
        return "normal"


@dataclass
class SystemMetrics:
    """System-level performance metrics."""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    disk_io_read_mb: float
    disk_io_write_mb: float
    network_sent_mb: float
    network_recv_mb: float
    process_count: int
    load_average: List[float] = field(default_factory=list)


@dataclass
class ApplicationMetrics:
    """Application-level performance metrics."""
    timestamp: float
    function_name: str
    execution_time: float
    memory_usage_mb: float
    cpu_usage_percent: float
    success: bool
    error_message: Optional[str] = None
    custom_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceAlert:
    """Performance alert notification."""
    timestamp: float
    metric_name: str
    current_value: float
    threshold_value: float
    severity: str  # "warning", "critical"
    message: str
    context: Dict[str, Any] = field(default_factory=dict)


class MetricCollector(ABC):
    """Abstract base class for metric collectors."""
    
    def __init__(self, name: str, collection_interval: float = 1.0):
        self.name = name
        self.collection_interval = collection_interval
        self._logger = logging.getLogger(f"bob_core.metrics.{name}")
    
    @abstractmethod
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect metrics and return as dictionary."""
        pass
    
    def get_description(self) -> str:
        """Get description of this collector."""
        return f"{self.name} (interval: {self.collection_interval}s)"


class SystemMetricCollector(MetricCollector):
    """Collector for system-level metrics."""
    
    def __init__(self, collection_interval: float = 5.0):
        super().__init__("system", collection_interval)
        self._last_disk_io = None
        self._last_network_io = None
        self._last_timestamp = None
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect system metrics."""
        try:
            current_time = time.time()
            
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk_usage = psutil.disk_usage('/')
            
            # Disk I/O
            disk_io = psutil.disk_io_counters()
            disk_read_mb = 0
            disk_write_mb = 0
            
            if self._last_disk_io and self._last_timestamp:
                time_delta = current_time - self._last_timestamp
                read_delta = disk_io.read_bytes - self._last_disk_io.read_bytes
                write_delta = disk_io.write_bytes - self._last_disk_io.write_bytes
                
                disk_read_mb = (read_delta / 1024 / 1024) / time_delta
                disk_write_mb = (write_delta / 1024 / 1024) / time_delta
            
            self._last_disk_io = disk_io
            
            # Network I/O
            network_io = psutil.net_io_counters()
            network_sent_mb = 0
            network_recv_mb = 0
            
            if self._last_network_io and self._last_timestamp:
                time_delta = current_time - self._last_timestamp
                sent_delta = network_io.bytes_sent - self._last_network_io.bytes_sent
                recv_delta = network_io.bytes_recv - self._last_network_io.bytes_recv
                
                network_sent_mb = (sent_delta / 1024 / 1024) / time_delta
                network_recv_mb = (recv_delta / 1024 / 1024) / time_delta
            
            self._last_network_io = network_io
            self._last_timestamp = current_time
            
            # Process count
            process_count = len(psutil.pids())
            
            # Load average (Unix-like systems)
            load_average = []
            try:
                load_average = list(psutil.getloadavg())
            except AttributeError:
                # Windows doesn't have load average
                pass
            
            metrics = SystemMetrics(
                timestamp=current_time,
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / 1024 / 1024,
                memory_available_mb=memory.available / 1024 / 1024,
                disk_usage_percent=disk_usage.percent,
                disk_io_read_mb=disk_read_mb,
                disk_io_write_mb=disk_write_mb,
                network_sent_mb=network_sent_mb,
                network_recv_mb=network_recv_mb,
                process_count=process_count,
                load_average=load_average
            )
            
            return metrics.__dict__
            
        except Exception as e:
            self._logger.error(f"Failed to collect system metrics: {e}")
            return {}


class ApplicationMetricCollector(MetricCollector):
    """Collector for application-level metrics."""
    
    def __init__(self, collection_interval: float = 1.0):
        super().__init__("application", collection_interval)
        self._function_metrics: deque = deque(maxlen=1000)
        self._lock = threading.RLock()
    
    def record_function_execution(self, 
                                 function_name: str,
                                 execution_time: float,
                                 success: bool,
                                 error_message: Optional[str] = None,
                                 custom_metrics: Dict[str, Any] = None) -> None:
        """Record function execution metrics."""
        try:
            # Get current process memory
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_usage_mb = memory_info.rss / 1024 / 1024
            
            # Get CPU usage (approximate)
            cpu_usage = process.cpu_percent()
            
            metrics = ApplicationMetrics(
                timestamp=time.time(),
                function_name=function_name,
                execution_time=execution_time,
                memory_usage_mb=memory_usage_mb,
                cpu_usage_percent=cpu_usage,
                success=success,
                error_message=error_message,
                custom_metrics=custom_metrics or {}
            )
            
            with self._lock:
                self._function_metrics.append(metrics)
            
        except Exception as e:
            self._logger.error(f"Failed to record function metrics: {e}")
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect application metrics."""
        with self._lock:
            if not self._function_metrics:
                return {}
            
            # Calculate aggregated metrics
            recent_metrics = list(self._function_metrics)
            
            # Group by function name
            function_stats = defaultdict(list)
            for metric in recent_metrics:
                function_stats[metric.function_name].append(metric)
            
            aggregated = {}
            for func_name, metrics_list in function_stats.items():
                execution_times = [m.execution_time for m in metrics_list]
                success_count = sum(1 for m in metrics_list if m.success)
                
                aggregated[func_name] = {
                    "call_count": len(metrics_list),
                    "success_count": success_count,
                    "error_count": len(metrics_list) - success_count,
                    "success_rate": success_count / len(metrics_list),
                    "avg_execution_time": statistics.mean(execution_times),
                    "min_execution_time": min(execution_times),
                    "max_execution_time": max(execution_times),
                    "median_execution_time": statistics.median(execution_times),
                    "total_execution_time": sum(execution_times)
                }
                
                if len(execution_times) > 1:
                    aggregated[func_name]["std_execution_time"] = statistics.stdev(execution_times)
            
            return {
                "timestamp": time.time(),
                "function_statistics": aggregated,
                "total_recorded_calls": len(recent_metrics)
            }


def performance_monitor(metric_collector: ApplicationMetricCollector = None,
                       custom_metrics: Dict[str, Any] = None):
    """Decorator for monitoring function performance."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            error_message = None
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                error_message = str(e)
                raise
            finally:
                execution_time = time.time() - start_time
                
                if metric_collector:
                    metric_collector.record_function_execution(
                        function_name=func.__name__,
                        execution_time=execution_time,
                        success=success,
                        error_message=error_message,
                        custom_metrics=custom_metrics
                    )
        
        return wrapper
    return decorator


class PerformanceProfiler:
    """Profiler for detailed performance analysis."""
    
    def __init__(self, name: str = "default"):
        self.name = name
        self._profiles: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._active_profiles: Dict[str, float] = {}
        self._lock = threading.RLock()
        self._logger = logging.getLogger(f"bob_core.profiler.{name}")
    
    def start_profile(self, profile_name: str) -> None:
        """Start profiling a section."""
        with self._lock:
            self._active_profiles[profile_name] = time.time()
    
    def end_profile(self, profile_name: str, metadata: Dict[str, Any] = None) -> float:
        """End profiling a section and return duration."""
        with self._lock:
            if profile_name not in self._active_profiles:
                self._logger.warning(f"No active profile found: {profile_name}")
                return 0.0
            
            start_time = self._active_profiles.pop(profile_name)
            duration = time.time() - start_time
            
            profile_data = {
                "start_time": start_time,
                "duration": duration,
                "metadata": metadata or {}
            }
            
            self._profiles[profile_name].append(profile_data)
            
            # Keep only recent profiles (last 1000)
            if len(self._profiles[profile_name]) > 1000:
                self._profiles[profile_name] = self._profiles[profile_name][-500:]
            
            return duration
    
    @contextmanager
    def profile(self, profile_name: str, metadata: Dict[str, Any] = None):
        """Context manager for profiling."""
        self.start_profile(profile_name)
        try:
            yield
        finally:
            self.end_profile(profile_name, metadata)
    
    def get_profile_stats(self, profile_name: str) -> Dict[str, Any]:
        """Get statistics for a profile."""
        with self._lock:
            if profile_name not in self._profiles:
                return {}
            
            durations = [p["duration"] for p in self._profiles[profile_name]]
            
            if not durations:
                return {}
            
            return {
                "profile_name": profile_name,
                "call_count": len(durations),
                "total_duration": sum(durations),
                "avg_duration": statistics.mean(durations),
                "min_duration": min(durations),
                "max_duration": max(durations),
                "median_duration": statistics.median(durations),
                "std_duration": statistics.stdev(durations) if len(durations) > 1 else 0,
                "recent_profiles": self._profiles[profile_name][-10:]  # Last 10 profiles
            }
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all profiles."""
        with self._lock:
            return {
                profile_name: self.get_profile_stats(profile_name)
                for profile_name in self._profiles.keys()
            }


class Benchmark:
    """Benchmark runner for performance testing."""
    
    def __init__(self, name: str):
        self.name = name
        self._results: List[Dict[str, Any]] = []
        self._logger = logging.getLogger(f"bob_core.benchmark.{name}")
    
    def run_benchmark(self, 
                     func: Callable,
                     iterations: int = 100,
                     warmup_iterations: int = 10,
                     args: tuple = (),
                     kwargs: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run benchmark on a function."""
        kwargs = kwargs or {}
        
        self._logger.info(f"Running benchmark: {func.__name__} ({iterations} iterations)")
        
        # Warmup
        for _ in range(warmup_iterations):
            try:
                func(*args, **kwargs)
            except Exception as e:
                self._logger.warning(f"Warmup iteration failed: {e}")
        
        # Actual benchmark
        durations = []
        errors = 0
        
        for i in range(iterations):
            start_time = time.time()
            try:
                func(*args, **kwargs)
                duration = time.time() - start_time
                durations.append(duration)
            except Exception as e:
                errors += 1
                self._logger.error(f"Benchmark iteration {i} failed: {e}")
        
        if not durations:
            return {"error": "All benchmark iterations failed"}
        
        # Calculate statistics
        result = {
            "function_name": func.__name__,
            "iterations": iterations,
            "successful_iterations": len(durations),
            "failed_iterations": errors,
            "success_rate": len(durations) / iterations,
            "total_duration": sum(durations),
            "avg_duration": statistics.mean(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "median_duration": statistics.median(durations),
            "std_duration": statistics.stdev(durations) if len(durations) > 1 else 0,
            "operations_per_second": len(durations) / sum(durations),
            "timestamp": time.time()
        }
        
        # Calculate percentiles
        sorted_durations = sorted(durations)
        result["p95_duration"] = sorted_durations[int(len(sorted_durations) * 0.95)]
        result["p99_duration"] = sorted_durations[int(len(sorted_durations) * 0.99)]
        
        self._results.append(result)
        
        self._logger.info(f"Benchmark completed: {result['avg_duration']:.4f}s avg, "
                         f"{result['operations_per_second']:.2f} ops/sec")
        
        return result
    
    def compare_benchmarks(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple benchmark results."""
        if len(results) < 2:
            return {"error": "Need at least 2 results to compare"}
        
        baseline = results[0]
        comparisons = []
        
        for result in results[1:]:
            speedup = baseline["avg_duration"] / result["avg_duration"]
            comparison = {
                "baseline": baseline["function_name"],
                "compared": result["function_name"],
                "speedup": speedup,
                "baseline_avg": baseline["avg_duration"],
                "compared_avg": result["avg_duration"],
                "improvement_percent": (speedup - 1) * 100
            }
            comparisons.append(comparison)
        
        return {
            "baseline": baseline["function_name"],
            "comparisons": comparisons,
            "timestamp": time.time()
        }


class PerformanceOptimizer:
    """Optimizer for performance improvements."""
    
    def __init__(self):
        self._optimizations: List[Dict[str, Any]] = []
        self._logger = logging.getLogger("bob_core.performance_optimizer")
    
    def analyze_performance(self, metrics: Dict[str, Any]) -> List[str]:
        """Analyze performance metrics and suggest optimizations."""
        suggestions = []
        
        # Analyze system metrics
        if "system" in metrics:
            system_metrics = metrics["system"]
            
            if system_metrics.get("cpu_percent", 0) > 80:
                suggestions.append("High CPU usage detected. Consider optimizing CPU-intensive operations.")
            
            if system_metrics.get("memory_percent", 0) > 85:
                suggestions.append("High memory usage detected. Consider implementing memory cleanup strategies.")
            
            if system_metrics.get("disk_usage_percent", 0) > 90:
                suggestions.append("High disk usage detected. Consider cleaning up temporary files.")
        
        # Analyze application metrics
        if "application" in metrics:
            app_metrics = metrics["application"]
            function_stats = app_metrics.get("function_statistics", {})
            
            for func_name, stats in function_stats.items():
                if stats.get("avg_execution_time", 0) > 5.0:
                    suggestions.append(f"Function '{func_name}' has high execution time. Consider optimization.")
                
                if stats.get("success_rate", 1.0) < 0.9:
                    suggestions.append(f"Function '{func_name}' has low success rate. Check error handling.")
        
        return suggestions
    
    def record_optimization(self, 
                          optimization_type: str,
                          description: str,
                          before_metrics: Dict[str, Any],
                          after_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Record an optimization and its impact."""
        optimization = {
            "timestamp": time.time(),
            "type": optimization_type,
            "description": description,
            "before_metrics": before_metrics,
            "after_metrics": after_metrics,
            "improvement": self._calculate_improvement(before_metrics, after_metrics)
        }
        
        self._optimizations.append(optimization)
        
        self._logger.info(f"Recorded optimization: {description}")
        
        return optimization
    
    def _calculate_improvement(self, before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate improvement between before and after metrics."""
        improvements = {}
        
        # Compare common metrics
        for key in ["avg_execution_time", "cpu_percent", "memory_percent"]:
            if key in before and key in after:
                before_val = before[key]
                after_val = after[key]
                
                if before_val > 0:
                    improvement_percent = ((before_val - after_val) / before_val) * 100
                    improvements[key] = {
                        "before": before_val,
                        "after": after_val,
                        "improvement_percent": improvement_percent
                    }
        
        return improvements
    
    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Get history of optimizations."""
        return self._optimizations.copy()


class PerformanceMonitor:
    """
    Main performance monitoring system.
    
    Coordinates metric collection, analysis, and optimization suggestions.
    
    Example:
        ```python
        # Initialize monitor
        monitor = PerformanceMonitor()
        
        # Start monitoring
        monitor.start_monitoring()
        
        # Use performance decorator
        @monitor.track_performance
        def my_function():
            time.sleep(1)
        
        # Get performance report
        report = monitor.get_performance_report()
        ```
    """
    
    def __init__(self, 
                 system_collection_interval: float = 5.0,
                 app_collection_interval: float = 1.0):
        self.system_collector = SystemMetricCollector(system_collection_interval)
        self.app_collector = ApplicationMetricCollector(app_collection_interval)
        self.profiler = PerformanceProfiler()
        self.optimizer = PerformanceOptimizer()
        
        self._collectors: List[MetricCollector] = [
            self.system_collector,
            self.app_collector
        ]
        
        self._thresholds: Dict[str, MetricThreshold] = {
            "cpu_percent": MetricThreshold(70.0, 90.0),
            "memory_percent": MetricThreshold(80.0, 95.0),
            "avg_execution_time": MetricThreshold(2.0, 5.0)
        }
        
        self._alerts: deque = deque(maxlen=100)
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.performance_monitor")
    
    def add_threshold(self, metric_name: str, threshold: MetricThreshold) -> None:
        """Add performance threshold."""
        with self._lock:
            self._thresholds[metric_name] = threshold
            self._logger.info(f"Added threshold for {metric_name}")
    
    def start_monitoring(self) -> None:
        """Start performance monitoring."""
        if self._monitoring:
            self._logger.warning("Performance monitoring is already running")
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self._monitor_thread.start()
        self._logger.info("Started performance monitoring")
    
    def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        self._logger.info("Stopped performance monitoring")
    
    def track_performance(self, custom_metrics: Dict[str, Any] = None):
        """Decorator for tracking function performance."""
        return performance_monitor(self.app_collector, custom_metrics)
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self._monitoring:
            try:
                # Collect metrics from all collectors
                all_metrics = {}
                for collector in self._collectors:
                    try:
                        metrics = collector.collect_metrics()
                        all_metrics[collector.name] = metrics
                    except Exception as e:
                        self._logger.error(f"Error collecting metrics from {collector.name}: {e}")
                
                # Check thresholds and generate alerts
                self._check_thresholds(all_metrics)
                
                # Sleep until next collection
                time.sleep(min(c.collection_interval for c in self._collectors))
                
            except Exception as e:
                self._logger.error(f"Error in monitoring loop: {e}")
                time.sleep(5)
    
    def _check_thresholds(self, metrics: Dict[str, Any]) -> None:
        """Check metrics against thresholds and generate alerts."""
        current_time = time.time()
        
        for metric_name, threshold in self._thresholds.items():
            # Find metric value in collected data
            metric_value = self._find_metric_value(metrics, metric_name)
            
            if metric_value is not None:
                severity = threshold.check_threshold(metric_value)
                
                if severity in ["warning", "critical"]:
                    alert = PerformanceAlert(
                        timestamp=current_time,
                        metric_name=metric_name,
                        current_value=metric_value,
                        threshold_value=threshold.warning_value if severity == "warning" else threshold.critical_value,
                        severity=severity,
                        message=f"{metric_name} is {severity}: {metric_value} (threshold: {threshold.warning_value if severity == 'warning' else threshold.critical_value})",
                        context={"metrics": metrics}
                    )
                    
                    with self._lock:
                        self._alerts.append(alert)
                    
                    self._logger.warning(f"Performance alert: {alert.message}")
    
    def _find_metric_value(self, metrics: Dict[str, Any], metric_name: str) -> Optional[float]:
        """Find metric value in nested metrics dictionary."""
        # Simple search in top-level metrics
        for collector_name, collector_metrics in metrics.items():
            if isinstance(collector_metrics, dict) and metric_name in collector_metrics:
                return collector_metrics[metric_name]
            
            # Search in function statistics
            if collector_name == "application" and "function_statistics" in collector_metrics:
                func_stats = collector_metrics["function_statistics"]
                for func_name, stats in func_stats.items():
                    if metric_name in stats:
                        return stats[metric_name]
        
        return None
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        metrics = {}
        for collector in self._collectors:
            try:
                collector_metrics = collector.collect_metrics()
                metrics[collector.name] = collector_metrics
            except Exception as e:
                metrics[collector.name] = {"error": str(e)}
        
        return metrics
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        current_metrics = self.get_current_metrics()
        profiler_stats = self.profiler.get_all_stats()
        optimization_suggestions = self.optimizer.analyze_performance(current_metrics)
        
        with self._lock:
            recent_alerts = list(self._alerts)[-10:]  # Last 10 alerts
        
        return {
            "timestamp": time.time(),
            "current_metrics": current_metrics,
            "profiler_statistics": profiler_stats,
            "optimization_suggestions": optimization_suggestions,
            "recent_alerts": [alert.__dict__ for alert in recent_alerts],
            "thresholds": {name: {"warning": t.warning_value, "critical": t.critical_value} 
                          for name, t in self._thresholds.items()},
            "monitoring_active": self._monitoring
        }
    
    def get_alerts(self, severity: Optional[str] = None) -> List[PerformanceAlert]:
        """Get performance alerts, optionally filtered by severity."""
        with self._lock:
            alerts = list(self._alerts)
        
        if severity:
            alerts = [alert for alert in alerts if alert.severity == severity]
        
        return alerts


# Global performance monitor instance
_global_performance_monitor: Optional[PerformanceMonitor] = None


def get_global_performance_monitor() -> PerformanceMonitor:
    """Get or create global performance monitor."""
    global _global_performance_monitor
    if _global_performance_monitor is None:
        _global_performance_monitor = PerformanceMonitor()
    return _global_performance_monitor 