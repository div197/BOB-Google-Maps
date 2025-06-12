"""bob_core.auto_recovery

Auto-Recovery system for restarting failed components and healing system state.
Follows the principles of Niṣkāma Karma Yoga - selfless service with perfect execution.
"""
from __future__ import annotations

import time
import threading
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import traceback
import psutil
import subprocess
import os

__all__ = [
    "RecoveryAction", "ComponentState", "AutoRecoveryManager",
    "RestartAction", "ResetAction", "CleanupAction", "HealthCheckAction",
    "ComponentMonitor", "RecoveryStrategy"
]


class ComponentState(Enum):
    """States of system components."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILING = "failing"
    FAILED = "failed"
    RECOVERING = "recovering"
    UNKNOWN = "unknown"


class RecoveryActionType(Enum):
    """Types of recovery actions."""
    RESTART = "restart"
    RESET = "reset"
    CLEANUP = "cleanup"
    HEALTH_CHECK = "health_check"
    CUSTOM = "custom"


@dataclass
class RecoveryConfig:
    """Configuration for auto-recovery behavior."""
    max_recovery_attempts: int = 3
    recovery_cooldown_seconds: int = 60
    health_check_interval_seconds: int = 30
    failure_threshold: int = 3
    auto_recovery_enabled: bool = True
    escalation_enabled: bool = True
    notification_enabled: bool = True


@dataclass
class RecoveryAttempt:
    """Record of a recovery attempt."""
    timestamp: float
    action_type: RecoveryActionType
    component_name: str
    success: bool
    error_message: Optional[str] = None
    duration_seconds: float = 0.0
    context: Dict[str, Any] = field(default_factory=dict)


class RecoveryAction(ABC):
    """Abstract base class for recovery actions."""
    
    def __init__(self, name: str, action_type: RecoveryActionType):
        self.name = name
        self.action_type = action_type
        self._logger = logging.getLogger(f"bob_core.recovery.{name}")
    
    @abstractmethod
    def execute(self, component_name: str, context: Dict[str, Any]) -> bool:
        """Execute the recovery action."""
        pass
    
    @abstractmethod
    def is_applicable(self, component_state: ComponentState, context: Dict[str, Any]) -> bool:
        """Check if this action is applicable for the current state."""
        pass
    
    def get_description(self) -> str:
        """Get human-readable description of this action."""
        return f"{self.name} ({self.action_type.value})"


class RestartAction(RecoveryAction):
    """Action to restart a failed component."""
    
    def __init__(self, 
                 name: str = "restart",
                 restart_command: Optional[str] = None,
                 process_name: Optional[str] = None,
                 service_name: Optional[str] = None):
        super().__init__(name, RecoveryActionType.RESTART)
        self.restart_command = restart_command
        self.process_name = process_name
        self.service_name = service_name
    
    def execute(self, component_name: str, context: Dict[str, Any]) -> bool:
        """Execute restart action."""
        try:
            self._logger.info(f"Attempting to restart component: {component_name}")
            
            # Try different restart methods
            if self.restart_command:
                return self._restart_with_command()
            elif self.process_name:
                return self._restart_process()
            elif self.service_name:
                return self._restart_service()
            else:
                return self._restart_generic(component_name, context)
                
        except Exception as e:
            self._logger.error(f"Failed to restart {component_name}: {e}")
            return False
    
    def _restart_with_command(self) -> bool:
        """Restart using custom command."""
        try:
            result = subprocess.run(
                self.restart_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            self._logger.error("Restart command timed out")
            return False
        except Exception as e:
            self._logger.error(f"Restart command failed: {e}")
            return False
    
    def _restart_process(self) -> bool:
        """Restart by killing and restarting process."""
        try:
            # Find and kill process
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == self.process_name:
                    proc.terminate()
                    proc.wait(timeout=10)
                    self._logger.info(f"Terminated process {self.process_name}")
                    break
            
            # Process should be restarted by system or supervisor
            time.sleep(5)
            
            # Check if process is running again
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == self.process_name:
                    self._logger.info(f"Process {self.process_name} restarted successfully")
                    return True
            
            return False
            
        except Exception as e:
            self._logger.error(f"Failed to restart process {self.process_name}: {e}")
            return False
    
    def _restart_service(self) -> bool:
        """Restart system service."""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(
                    f"net stop {self.service_name} && net start {self.service_name}",
                    shell=True,
                    capture_output=True,
                    text=True
                )
            else:  # Unix-like
                result = subprocess.run(
                    f"systemctl restart {self.service_name}",
                    shell=True,
                    capture_output=True,
                    text=True
                )
            
            return result.returncode == 0
            
        except Exception as e:
            self._logger.error(f"Failed to restart service {self.service_name}: {e}")
            return False
    
    def _restart_generic(self, component_name: str, context: Dict[str, Any]) -> bool:
        """Generic restart for application components."""
        try:
            # Look for restart function in context
            restart_func = context.get("restart_function")
            if restart_func and callable(restart_func):
                restart_func()
                return True
            
            # Look for component instance to restart
            component_instance = context.get("component_instance")
            if component_instance and hasattr(component_instance, 'restart'):
                component_instance.restart()
                return True
            
            self._logger.warning(f"No restart method available for {component_name}")
            return False
            
        except Exception as e:
            self._logger.error(f"Generic restart failed for {component_name}: {e}")
            return False
    
    def is_applicable(self, component_state: ComponentState, context: Dict[str, Any]) -> bool:
        """Check if restart is applicable."""
        return component_state in [ComponentState.FAILED, ComponentState.FAILING]


class ResetAction(RecoveryAction):
    """Action to reset component state."""
    
    def __init__(self, name: str = "reset", reset_function: Optional[Callable] = None):
        super().__init__(name, RecoveryActionType.RESET)
        self.reset_function = reset_function
    
    def execute(self, component_name: str, context: Dict[str, Any]) -> bool:
        """Execute reset action."""
        try:
            self._logger.info(f"Resetting component: {component_name}")
            
            if self.reset_function:
                self.reset_function(component_name, context)
                return True
            
            # Look for reset function in context
            reset_func = context.get("reset_function")
            if reset_func and callable(reset_func):
                reset_func()
                return True
            
            # Look for component instance to reset
            component_instance = context.get("component_instance")
            if component_instance and hasattr(component_instance, 'reset'):
                component_instance.reset()
                return True
            
            self._logger.warning(f"No reset method available for {component_name}")
            return False
            
        except Exception as e:
            self._logger.error(f"Failed to reset {component_name}: {e}")
            return False
    
    def is_applicable(self, component_state: ComponentState, context: Dict[str, Any]) -> bool:
        """Check if reset is applicable."""
        return component_state in [ComponentState.DEGRADED, ComponentState.FAILING]


class CleanupAction(RecoveryAction):
    """Action to cleanup component resources."""
    
    def __init__(self, 
                 name: str = "cleanup",
                 cleanup_function: Optional[Callable] = None,
                 temp_dirs: List[str] = None,
                 log_files: List[str] = None):
        super().__init__(name, RecoveryActionType.CLEANUP)
        self.cleanup_function = cleanup_function
        self.temp_dirs = temp_dirs or []
        self.log_files = log_files or []
    
    def execute(self, component_name: str, context: Dict[str, Any]) -> bool:
        """Execute cleanup action."""
        try:
            self._logger.info(f"Cleaning up component: {component_name}")
            
            success = True
            
            # Custom cleanup function
            if self.cleanup_function:
                try:
                    self.cleanup_function(component_name, context)
                except Exception as e:
                    self._logger.error(f"Custom cleanup failed: {e}")
                    success = False
            
            # Clean temporary directories
            for temp_dir in self.temp_dirs:
                try:
                    import shutil
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
                        self._logger.info(f"Cleaned temp directory: {temp_dir}")
                except Exception as e:
                    self._logger.error(f"Failed to clean {temp_dir}: {e}")
                    success = False
            
            # Clean log files
            for log_file in self.log_files:
                try:
                    if os.path.exists(log_file):
                        os.remove(log_file)
                        self._logger.info(f"Cleaned log file: {log_file}")
                except Exception as e:
                    self._logger.error(f"Failed to clean {log_file}: {e}")
                    success = False
            
            # Look for cleanup function in context
            cleanup_func = context.get("cleanup_function")
            if cleanup_func and callable(cleanup_func):
                try:
                    cleanup_func()
                except Exception as e:
                    self._logger.error(f"Context cleanup failed: {e}")
                    success = False
            
            return success
            
        except Exception as e:
            self._logger.error(f"Failed to cleanup {component_name}: {e}")
            return False
    
    def is_applicable(self, component_state: ComponentState, context: Dict[str, Any]) -> bool:
        """Check if cleanup is applicable."""
        return True  # Cleanup is always applicable


class HealthCheckAction(RecoveryAction):
    """Action to perform health check on component."""
    
    def __init__(self, 
                 name: str = "health_check",
                 health_check_function: Optional[Callable] = None):
        super().__init__(name, RecoveryActionType.HEALTH_CHECK)
        self.health_check_function = health_check_function
    
    def execute(self, component_name: str, context: Dict[str, Any]) -> bool:
        """Execute health check action."""
        try:
            self._logger.info(f"Performing health check on: {component_name}")
            
            if self.health_check_function:
                return self.health_check_function(component_name, context)
            
            # Look for health check function in context
            health_func = context.get("health_check_function")
            if health_func and callable(health_func):
                return health_func()
            
            # Look for component instance health check
            component_instance = context.get("component_instance")
            if component_instance and hasattr(component_instance, 'health_check'):
                return component_instance.health_check()
            
            self._logger.warning(f"No health check method available for {component_name}")
            return False
            
        except Exception as e:
            self._logger.error(f"Health check failed for {component_name}: {e}")
            return False
    
    def is_applicable(self, component_state: ComponentState, context: Dict[str, Any]) -> bool:
        """Check if health check is applicable."""
        return True  # Health check is always applicable


class RecoveryStrategy:
    """Strategy defining recovery actions for a component."""
    
    def __init__(self, 
                 name: str,
                 actions: List[RecoveryAction],
                 max_attempts: int = 3,
                 cooldown_seconds: int = 60):
        self.name = name
        self.actions = actions
        self.max_attempts = max_attempts
        self.cooldown_seconds = cooldown_seconds
        self._logger = logging.getLogger(f"bob_core.recovery_strategy.{name}")
    
    def execute_recovery(self, 
                        component_name: str,
                        component_state: ComponentState,
                        context: Dict[str, Any]) -> List[RecoveryAttempt]:
        """Execute recovery strategy."""
        attempts = []
        
        for action in self.actions:
            if not action.is_applicable(component_state, context):
                continue
            
            start_time = time.time()
            try:
                self._logger.info(f"Executing {action.get_description()} for {component_name}")
                success = action.execute(component_name, context)
                duration = time.time() - start_time
                
                attempt = RecoveryAttempt(
                    timestamp=start_time,
                    action_type=action.action_type,
                    component_name=component_name,
                    success=success,
                    duration_seconds=duration,
                    context=context.copy()
                )
                
                attempts.append(attempt)
                
                if success:
                    self._logger.info(f"Recovery action {action.name} succeeded for {component_name}")
                    break
                else:
                    self._logger.warning(f"Recovery action {action.name} failed for {component_name}")
                
            except Exception as e:
                duration = time.time() - start_time
                error_msg = str(e)
                
                attempt = RecoveryAttempt(
                    timestamp=start_time,
                    action_type=action.action_type,
                    component_name=component_name,
                    success=False,
                    error_message=error_msg,
                    duration_seconds=duration,
                    context=context.copy()
                )
                
                attempts.append(attempt)
                self._logger.error(f"Recovery action {action.name} threw exception: {e}")
        
        return attempts


class ComponentMonitor:
    """Monitor for tracking component health and triggering recovery."""
    
    def __init__(self, 
                 name: str,
                 health_check_function: Callable[[], bool],
                 recovery_strategy: RecoveryStrategy,
                 check_interval_seconds: int = 30):
        self.name = name
        self.health_check_function = health_check_function
        self.recovery_strategy = recovery_strategy
        self.check_interval_seconds = check_interval_seconds
        self.current_state = ComponentState.UNKNOWN
        self.last_check_time = 0.0
        self.failure_count = 0
        self.recovery_attempts = []
        self.last_recovery_time = 0.0
        self._logger = logging.getLogger(f"bob_core.component_monitor.{name}")
    
    def check_health(self) -> ComponentState:
        """Check component health and return current state."""
        try:
            self.last_check_time = time.time()
            is_healthy = self.health_check_function()
            
            if is_healthy:
                if self.current_state != ComponentState.HEALTHY:
                    self._logger.info(f"Component {self.name} is now healthy")
                self.current_state = ComponentState.HEALTHY
                self.failure_count = 0
            else:
                self.failure_count += 1
                if self.failure_count == 1:
                    self.current_state = ComponentState.DEGRADED
                elif self.failure_count <= 3:
                    self.current_state = ComponentState.FAILING
                else:
                    self.current_state = ComponentState.FAILED
                
                self._logger.warning(f"Component {self.name} health check failed (count: {self.failure_count})")
            
            return self.current_state
            
        except Exception as e:
            self._logger.error(f"Health check error for {self.name}: {e}")
            self.current_state = ComponentState.UNKNOWN
            return self.current_state
    
    def should_recover(self, cooldown_seconds: int = 60) -> bool:
        """Check if component should be recovered."""
        if self.current_state not in [ComponentState.FAILING, ComponentState.FAILED]:
            return False
        
        # Check cooldown period
        time_since_recovery = time.time() - self.last_recovery_time
        if time_since_recovery < cooldown_seconds:
            return False
        
        return True
    
    def attempt_recovery(self, context: Dict[str, Any] = None) -> List[RecoveryAttempt]:
        """Attempt to recover the component."""
        if context is None:
            context = {}
        
        context["component_name"] = self.name
        context["current_state"] = self.current_state
        context["failure_count"] = self.failure_count
        
        self.current_state = ComponentState.RECOVERING
        self.last_recovery_time = time.time()
        
        attempts = self.recovery_strategy.execute_recovery(
            self.name,
            self.current_state,
            context
        )
        
        self.recovery_attempts.extend(attempts)
        
        # Check if recovery was successful
        if attempts and attempts[-1].success:
            self._logger.info(f"Recovery successful for {self.name}")
            self.current_state = ComponentState.HEALTHY
            self.failure_count = 0
        else:
            self._logger.error(f"Recovery failed for {self.name}")
            self.current_state = ComponentState.FAILED
        
        return attempts


class AutoRecoveryManager:
    """
    Manager for automatic recovery of system components.
    
    Monitors component health and automatically triggers recovery actions
    when failures are detected.
    
    Example:
        ```python
        # Setup recovery manager
        manager = AutoRecoveryManager()
        
        # Register component with recovery strategy
        strategy = RecoveryStrategy("browser_recovery", [
            CleanupAction("cleanup_temp", temp_dirs=["/tmp/chrome"]),
            RestartAction("restart_browser", process_name="chrome")
        ])
        
        monitor = ComponentMonitor(
            "browser",
            health_check_function=lambda: check_browser_health(),
            recovery_strategy=strategy
        )
        
        manager.register_component(monitor)
        
        # Start monitoring
        manager.start_monitoring()
        ```
    """
    
    def __init__(self, config: RecoveryConfig = None):
        """Initialize auto-recovery manager."""
        self.config = config or RecoveryConfig()
        self._components: Dict[str, ComponentMonitor] = {}
        self._monitoring_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.auto_recovery")
        self._recovery_history: List[RecoveryAttempt] = []
    
    def register_component(self, monitor: ComponentMonitor) -> None:
        """Register a component for monitoring and recovery."""
        with self._lock:
            self._components[monitor.name] = monitor
            self._logger.info(f"Registered component for monitoring: {monitor.name}")
    
    def unregister_component(self, component_name: str) -> None:
        """Unregister a component from monitoring."""
        with self._lock:
            if component_name in self._components:
                del self._components[component_name]
                self._logger.info(f"Unregistered component: {component_name}")
    
    def start_monitoring(self) -> None:
        """Start monitoring all registered components."""
        if self._monitoring_thread and self._monitoring_thread.is_alive():
            self._logger.warning("Monitoring is already running")
            return
        
        self._stop_monitoring.clear()
        self._monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self._monitoring_thread.start()
        self._logger.info("Started component monitoring")
    
    def stop_monitoring(self) -> None:
        """Stop monitoring all components."""
        self._stop_monitoring.set()
        if self._monitoring_thread:
            self._monitoring_thread.join(timeout=5)
        self._logger.info("Stopped component monitoring")
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while not self._stop_monitoring.is_set():
            try:
                with self._lock:
                    for component_name, monitor in self._components.items():
                        try:
                            # Check component health
                            current_state = monitor.check_health()
                            
                            # Trigger recovery if needed
                            if (self.config.auto_recovery_enabled and 
                                monitor.should_recover(self.config.recovery_cooldown_seconds)):
                                
                                self._logger.warning(f"Triggering recovery for {component_name}")
                                attempts = monitor.attempt_recovery()
                                self._recovery_history.extend(attempts)
                                
                                # Limit recovery history size
                                if len(self._recovery_history) > 1000:
                                    self._recovery_history = self._recovery_history[-500:]
                        
                        except Exception as e:
                            self._logger.error(f"Error monitoring component {component_name}: {e}")
                
                # Wait for next check
                self._stop_monitoring.wait(self.config.health_check_interval_seconds)
                
            except Exception as e:
                self._logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)  # Wait before retrying
    
    def get_component_status(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific component."""
        with self._lock:
            monitor = self._components.get(component_name)
            if not monitor:
                return None
            
            return {
                "name": monitor.name,
                "state": monitor.current_state.value,
                "failure_count": monitor.failure_count,
                "last_check_time": monitor.last_check_time,
                "last_recovery_time": monitor.last_recovery_time,
                "recovery_attempts": len(monitor.recovery_attempts),
                "check_interval_seconds": monitor.check_interval_seconds
            }
    
    def get_all_components_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all registered components."""
        with self._lock:
            return {
                name: self.get_component_status(name)
                for name in self._components.keys()
            }
    
    def manually_recover_component(self, 
                                  component_name: str,
                                  context: Dict[str, Any] = None) -> List[RecoveryAttempt]:
        """Manually trigger recovery for a specific component."""
        with self._lock:
            monitor = self._components.get(component_name)
            if not monitor:
                raise ValueError(f"Component {component_name} not registered")
            
            self._logger.info(f"Manually triggering recovery for {component_name}")
            attempts = monitor.attempt_recovery(context or {})
            self._recovery_history.extend(attempts)
            
            return attempts
    
    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get recovery statistics and metrics."""
        with self._lock:
            total_attempts = len(self._recovery_history)
            successful_attempts = sum(1 for attempt in self._recovery_history if attempt.success)
            
            # Group by action type
            action_stats = {}
            for attempt in self._recovery_history:
                action_type = attempt.action_type.value
                if action_type not in action_stats:
                    action_stats[action_type] = {"total": 0, "successful": 0}
                
                action_stats[action_type]["total"] += 1
                if attempt.success:
                    action_stats[action_type]["successful"] += 1
            
            # Recent attempts (last 24 hours)
            recent_cutoff = time.time() - (24 * 3600)
            recent_attempts = [
                attempt for attempt in self._recovery_history
                if attempt.timestamp >= recent_cutoff
            ]
            
            return {
                "total_recovery_attempts": total_attempts,
                "successful_recovery_attempts": successful_attempts,
                "success_rate": successful_attempts / total_attempts if total_attempts > 0 else 0,
                "action_statistics": action_stats,
                "recent_attempts_24h": len(recent_attempts),
                "registered_components": len(self._components),
                "monitoring_enabled": self._monitoring_thread and self._monitoring_thread.is_alive(),
                "config": {
                    "auto_recovery_enabled": self.config.auto_recovery_enabled,
                    "max_recovery_attempts": self.config.max_recovery_attempts,
                    "recovery_cooldown_seconds": self.config.recovery_cooldown_seconds,
                    "health_check_interval_seconds": self.config.health_check_interval_seconds
                }
            }


# Global auto-recovery manager instance
_global_recovery_manager: Optional[AutoRecoveryManager] = None


def get_global_recovery_manager() -> AutoRecoveryManager:
    """Get or create global auto-recovery manager."""
    global _global_recovery_manager
    if _global_recovery_manager is None:
        _global_recovery_manager = AutoRecoveryManager()
    return _global_recovery_manager 