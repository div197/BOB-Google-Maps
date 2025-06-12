"""bob_core.connection_pooling

Connection Pooling system for efficient resource utilization and management.
Follows the principles of Niṣkāma Karma Yoga - selfless service with perfect execution.
"""
from __future__ import annotations

import time
import threading
import logging
import queue
from typing import Any, Dict, List, Optional, Callable, Union, Generic, TypeVar
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from contextlib import contextmanager
import weakref

__all__ = [
    "ConnectionPool", "PooledConnection", "ConnectionFactory",
    "WebDriverPool", "DatabasePool", "HTTPConnectionPool",
    "PoolConfig", "PoolStats", "ConnectionManager"
]

T = TypeVar('T')


@dataclass
class PoolConfig:
    """Configuration for connection pools."""
    min_connections: int = 1
    max_connections: int = 10
    max_idle_time_seconds: int = 300  # 5 minutes
    connection_timeout_seconds: int = 30
    validation_interval_seconds: int = 60
    retry_attempts: int = 3
    retry_delay_seconds: float = 1.0
    enable_health_check: bool = True
    enable_metrics: bool = True


@dataclass
class PoolStats:
    """Statistics for connection pool."""
    total_connections: int = 0
    active_connections: int = 0
    idle_connections: int = 0
    created_connections: int = 0
    destroyed_connections: int = 0
    failed_acquisitions: int = 0
    successful_acquisitions: int = 0
    average_acquisition_time: float = 0.0
    peak_connections: int = 0
    last_updated: float = field(default_factory=time.time)


class PooledConnection(Generic[T]):
    """Wrapper for pooled connections with metadata."""
    
    def __init__(self, 
                 connection: T,
                 pool: 'ConnectionPool',
                 connection_id: str):
        self.connection = connection
        self.pool = pool
        self.connection_id = connection_id
        self.created_time = time.time()
        self.last_used_time = time.time()
        self.use_count = 0
        self.is_active = False
        self.is_valid = True
        self._lock = threading.RLock()
    
    def __enter__(self) -> T:
        """Context manager entry."""
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - return connection to pool."""
        self.pool.release_connection(self)
    
    def mark_used(self) -> None:
        """Mark connection as used."""
        with self._lock:
            self.last_used_time = time.time()
            self.use_count += 1
    
    def is_expired(self, max_idle_time: int) -> bool:
        """Check if connection has expired."""
        with self._lock:
            return (time.time() - self.last_used_time) > max_idle_time
    
    def get_age_seconds(self) -> float:
        """Get connection age in seconds."""
        return time.time() - self.created_time
    
    def get_idle_time_seconds(self) -> float:
        """Get idle time in seconds."""
        return time.time() - self.last_used_time


class ConnectionFactory(ABC, Generic[T]):
    """Abstract factory for creating connections."""
    
    @abstractmethod
    def create_connection(self) -> T:
        """Create a new connection."""
        pass
    
    @abstractmethod
    def validate_connection(self, connection: T) -> bool:
        """Validate if connection is still usable."""
        pass
    
    @abstractmethod
    def destroy_connection(self, connection: T) -> None:
        """Properly close/destroy a connection."""
        pass
    
    def get_connection_info(self, connection: T) -> Dict[str, Any]:
        """Get information about the connection."""
        return {"type": type(connection).__name__}


class WebDriverFactory(ConnectionFactory):
    """Factory for creating WebDriver connections."""
    
    def __init__(self, 
                 driver_type: str = "chrome",
                 headless: bool = True,
                 options: Dict[str, Any] = None):
        self.driver_type = driver_type.lower()
        self.headless = headless
        self.options = options or {}
        self._logger = logging.getLogger("bob_core.webdriver_factory")
    
    def create_connection(self):
        """Create a new WebDriver instance."""
        try:
            if self.driver_type == "chrome":
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                
                chrome_options = Options()
                if self.headless:
                    chrome_options.add_argument("--headless")
                
                # Add common options
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=1920,1080")
                
                # Add custom options
                for option, value in self.options.items():
                    if value is True:
                        chrome_options.add_argument(f"--{option}")
                    elif value is not False:
                        chrome_options.add_argument(f"--{option}={value}")
                
                driver = webdriver.Chrome(options=chrome_options)
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(10)
                
                self._logger.info("Created new Chrome WebDriver")
                return driver
                
            else:
                raise ValueError(f"Unsupported driver type: {self.driver_type}")
                
        except Exception as e:
            self._logger.error(f"Failed to create WebDriver: {e}")
            raise
    
    def validate_connection(self, connection) -> bool:
        """Validate WebDriver connection."""
        try:
            # Try to get current URL
            _ = connection.current_url
            return True
        except Exception:
            return False
    
    def destroy_connection(self, connection) -> None:
        """Close WebDriver connection."""
        try:
            connection.quit()
            self._logger.info("Closed WebDriver connection")
        except Exception as e:
            self._logger.error(f"Error closing WebDriver: {e}")
    
    def get_connection_info(self, connection) -> Dict[str, Any]:
        """Get WebDriver connection info."""
        try:
            return {
                "type": "WebDriver",
                "browser": self.driver_type,
                "current_url": connection.current_url,
                "window_handles": len(connection.window_handles),
                "session_id": connection.session_id
            }
        except:
            return {"type": "WebDriver", "browser": self.driver_type, "status": "invalid"}


class HTTPConnectionFactory(ConnectionFactory):
    """Factory for creating HTTP connections."""
    
    def __init__(self, 
                 base_url: str,
                 timeout: int = 30,
                 headers: Dict[str, str] = None):
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers or {}
        self._logger = logging.getLogger("bob_core.http_factory")
    
    def create_connection(self):
        """Create a new HTTP session."""
        try:
            import requests
            
            session = requests.Session()
            session.timeout = self.timeout
            session.headers.update(self.headers)
            
            # Test connection
            response = session.get(self.base_url, timeout=5)
            response.raise_for_status()
            
            self._logger.info(f"Created new HTTP session for {self.base_url}")
            return session
            
        except Exception as e:
            self._logger.error(f"Failed to create HTTP session: {e}")
            raise
    
    def validate_connection(self, connection) -> bool:
        """Validate HTTP session."""
        try:
            # Simple HEAD request to test connection
            response = connection.head(self.base_url, timeout=5)
            return response.status_code < 400
        except Exception:
            return False
    
    def destroy_connection(self, connection) -> None:
        """Close HTTP session."""
        try:
            connection.close()
            self._logger.info("Closed HTTP session")
        except Exception as e:
            self._logger.error(f"Error closing HTTP session: {e}")


class ConnectionPool(Generic[T]):
    """
    Generic connection pool for managing reusable connections.
    
    Features:
    - Configurable min/max connections
    - Automatic connection validation
    - Idle connection cleanup
    - Connection health monitoring
    - Comprehensive metrics
    
    Example:
        ```python
        # Create WebDriver pool
        factory = WebDriverFactory("chrome", headless=True)
        config = PoolConfig(min_connections=2, max_connections=5)
        pool = ConnectionPool(factory, config)
        
        # Use connection
        with pool.get_connection() as driver:
            driver.get("https://example.com")
            # Connection automatically returned to pool
        ```
    """
    
    def __init__(self, 
                 factory: ConnectionFactory[T],
                 config: PoolConfig = None,
                 name: str = "default"):
        self.factory = factory
        self.config = config or PoolConfig()
        self.name = name
        
        self._connections: Dict[str, PooledConnection[T]] = {}
        self._available_queue: queue.Queue = queue.Queue()
        self._lock = threading.RLock()
        self._stats = PoolStats()
        self._logger = logging.getLogger(f"bob_core.connection_pool.{name}")
        
        # Background maintenance
        self._maintenance_thread: Optional[threading.Thread] = None
        self._stop_maintenance = threading.Event()
        
        # Initialize pool
        self._initialize_pool()
        self._start_maintenance()
    
    def _initialize_pool(self) -> None:
        """Initialize the connection pool with minimum connections."""
        with self._lock:
            for i in range(self.config.min_connections):
                try:
                    self._create_connection()
                except Exception as e:
                    self._logger.error(f"Failed to create initial connection {i}: {e}")
    
    def _create_connection(self) -> PooledConnection[T]:
        """Create a new pooled connection."""
        connection_id = f"{self.name}_{int(time.time() * 1000)}_{len(self._connections)}"
        
        try:
            raw_connection = self.factory.create_connection()
            pooled_conn = PooledConnection(raw_connection, self, connection_id)
            
            with self._lock:
                self._connections[connection_id] = pooled_conn
                self._available_queue.put(pooled_conn)
                self._stats.total_connections += 1
                self._stats.created_connections += 1
                self._stats.idle_connections += 1
                
                if self._stats.total_connections > self._stats.peak_connections:
                    self._stats.peak_connections = self._stats.total_connections
            
            self._logger.info(f"Created new connection: {connection_id}")
            return pooled_conn
            
        except Exception as e:
            self._logger.error(f"Failed to create connection: {e}")
            raise
    
    def get_connection(self, timeout: float = None) -> PooledConnection[T]:
        """
        Get a connection from the pool.
        
        Parameters
        ----------
        timeout : float, optional
            Timeout in seconds to wait for connection
            
        Returns
        -------
        PooledConnection
            Pooled connection wrapper
        """
        start_time = time.time()
        timeout = timeout or self.config.connection_timeout_seconds
        
        try:
            # Try to get available connection
            try:
                pooled_conn = self._available_queue.get(timeout=timeout)
                
                # Validate connection
                if self._validate_pooled_connection(pooled_conn):
                    with self._lock:
                        pooled_conn.is_active = True
                        pooled_conn.mark_used()
                        self._stats.active_connections += 1
                        self._stats.idle_connections -= 1
                        self._stats.successful_acquisitions += 1
                        
                        # Update average acquisition time
                        acquisition_time = time.time() - start_time
                        if self._stats.successful_acquisitions == 1:
                            self._stats.average_acquisition_time = acquisition_time
                        else:
                            self._stats.average_acquisition_time = (
                                (self._stats.average_acquisition_time * (self._stats.successful_acquisitions - 1) + 
                                 acquisition_time) / self._stats.successful_acquisitions
                            )
                    
                    self._logger.debug(f"Acquired connection: {pooled_conn.connection_id}")
                    return pooled_conn
                else:
                    # Connection is invalid, destroy and try again
                    self._destroy_connection(pooled_conn)
                    return self.get_connection(timeout - (time.time() - start_time))
                    
            except queue.Empty:
                # No available connections, try to create new one
                with self._lock:
                    if self._stats.total_connections < self.config.max_connections:
                        pooled_conn = self._create_connection()
                        # Remove from available queue since we're using it
                        try:
                            self._available_queue.get_nowait()
                        except queue.Empty:
                            pass
                        
                        pooled_conn.is_active = True
                        pooled_conn.mark_used()
                        self._stats.active_connections += 1
                        self._stats.idle_connections -= 1
                        self._stats.successful_acquisitions += 1
                        
                        return pooled_conn
                    else:
                        # Pool is at max capacity
                        raise queue.Empty("Pool at maximum capacity")
                        
        except Exception as e:
            with self._lock:
                self._stats.failed_acquisitions += 1
            
            self._logger.error(f"Failed to acquire connection: {e}")
            raise
    
    @contextmanager
    def connection(self, timeout: float = None):
        """Context manager for getting and releasing connections."""
        conn = self.get_connection(timeout)
        try:
            yield conn.connection
        finally:
            self.release_connection(conn)
    
    def release_connection(self, pooled_conn: PooledConnection[T]) -> None:
        """Release a connection back to the pool."""
        with self._lock:
            if not pooled_conn.is_active:
                self._logger.warning(f"Attempting to release inactive connection: {pooled_conn.connection_id}")
                return
            
            pooled_conn.is_active = False
            
            # Validate connection before returning to pool
            if self._validate_pooled_connection(pooled_conn):
                self._available_queue.put(pooled_conn)
                self._stats.active_connections -= 1
                self._stats.idle_connections += 1
                self._logger.debug(f"Released connection: {pooled_conn.connection_id}")
            else:
                # Connection is invalid, destroy it
                self._destroy_connection(pooled_conn)
                
                # Create replacement if below minimum
                if self._stats.total_connections < self.config.min_connections:
                    try:
                        self._create_connection()
                    except Exception as e:
                        self._logger.error(f"Failed to create replacement connection: {e}")
    
    def _validate_pooled_connection(self, pooled_conn: PooledConnection[T]) -> bool:
        """Validate a pooled connection."""
        try:
            # Check if connection is expired
            if pooled_conn.is_expired(self.config.max_idle_time_seconds):
                self._logger.info(f"Connection expired: {pooled_conn.connection_id}")
                return False
            
            # Check if connection is still valid
            if not pooled_conn.is_valid:
                return False
            
            # Use factory validation
            if self.config.enable_health_check:
                return self.factory.validate_connection(pooled_conn.connection)
            
            return True
            
        except Exception as e:
            self._logger.error(f"Connection validation failed: {e}")
            return False
    
    def _destroy_connection(self, pooled_conn: PooledConnection[T]) -> None:
        """Destroy a pooled connection."""
        try:
            with self._lock:
                connection_id = pooled_conn.connection_id
                
                # Remove from connections dict
                if connection_id in self._connections:
                    del self._connections[connection_id]
                
                # Update stats
                self._stats.total_connections -= 1
                self._stats.destroyed_connections += 1
                
                if pooled_conn.is_active:
                    self._stats.active_connections -= 1
                else:
                    self._stats.idle_connections -= 1
            
            # Destroy the actual connection
            self.factory.destroy_connection(pooled_conn.connection)
            pooled_conn.is_valid = False
            
            self._logger.info(f"Destroyed connection: {connection_id}")
            
        except Exception as e:
            self._logger.error(f"Error destroying connection: {e}")
    
    def _start_maintenance(self) -> None:
        """Start background maintenance thread."""
        if self._maintenance_thread and self._maintenance_thread.is_alive():
            return
        
        self._stop_maintenance.clear()
        self._maintenance_thread = threading.Thread(
            target=self._maintenance_loop,
            daemon=True
        )
        self._maintenance_thread.start()
        self._logger.info("Started pool maintenance thread")
    
    def _maintenance_loop(self) -> None:
        """Background maintenance loop."""
        while not self._stop_maintenance.is_set():
            try:
                self._cleanup_expired_connections()
                self._ensure_minimum_connections()
                self._update_stats()
                
                # Wait for next maintenance cycle
                self._stop_maintenance.wait(self.config.validation_interval_seconds)
                
            except Exception as e:
                self._logger.error(f"Error in maintenance loop: {e}")
                time.sleep(10)
    
    def _cleanup_expired_connections(self) -> None:
        """Clean up expired idle connections."""
        expired_connections = []
        
        with self._lock:
            for conn_id, pooled_conn in self._connections.items():
                if (not pooled_conn.is_active and 
                    pooled_conn.is_expired(self.config.max_idle_time_seconds)):
                    expired_connections.append(pooled_conn)
        
        for pooled_conn in expired_connections:
            try:
                # Remove from available queue
                temp_queue = queue.Queue()
                while not self._available_queue.empty():
                    try:
                        conn = self._available_queue.get_nowait()
                        if conn != pooled_conn:
                            temp_queue.put(conn)
                    except queue.Empty:
                        break
                
                # Put back non-expired connections
                while not temp_queue.empty():
                    self._available_queue.put(temp_queue.get_nowait())
                
                # Destroy expired connection
                self._destroy_connection(pooled_conn)
                
            except Exception as e:
                self._logger.error(f"Error cleaning up expired connection: {e}")
    
    def _ensure_minimum_connections(self) -> None:
        """Ensure minimum number of connections are available."""
        with self._lock:
            while self._stats.total_connections < self.config.min_connections:
                try:
                    self._create_connection()
                except Exception as e:
                    self._logger.error(f"Failed to create minimum connection: {e}")
                    break
    
    def _update_stats(self) -> None:
        """Update pool statistics."""
        with self._lock:
            self._stats.last_updated = time.time()
    
    def get_stats(self) -> PoolStats:
        """Get current pool statistics."""
        with self._lock:
            return PoolStats(
                total_connections=self._stats.total_connections,
                active_connections=self._stats.active_connections,
                idle_connections=self._stats.idle_connections,
                created_connections=self._stats.created_connections,
                destroyed_connections=self._stats.destroyed_connections,
                failed_acquisitions=self._stats.failed_acquisitions,
                successful_acquisitions=self._stats.successful_acquisitions,
                average_acquisition_time=self._stats.average_acquisition_time,
                peak_connections=self._stats.peak_connections,
                last_updated=self._stats.last_updated
            )
    
    def get_connection_info(self) -> List[Dict[str, Any]]:
        """Get information about all connections."""
        with self._lock:
            info = []
            for conn_id, pooled_conn in self._connections.items():
                try:
                    conn_info = self.factory.get_connection_info(pooled_conn.connection)
                    conn_info.update({
                        "connection_id": conn_id,
                        "is_active": pooled_conn.is_active,
                        "age_seconds": pooled_conn.get_age_seconds(),
                        "idle_time_seconds": pooled_conn.get_idle_time_seconds(),
                        "use_count": pooled_conn.use_count
                    })
                    info.append(conn_info)
                except Exception as e:
                    info.append({
                        "connection_id": conn_id,
                        "error": str(e)
                    })
            return info
    
    def close(self) -> None:
        """Close the connection pool and all connections."""
        self._logger.info("Closing connection pool")
        
        # Stop maintenance
        self._stop_maintenance.set()
        if self._maintenance_thread:
            self._maintenance_thread.join(timeout=5)
        
        # Close all connections
        with self._lock:
            connections_to_destroy = list(self._connections.values())
        
        for pooled_conn in connections_to_destroy:
            self._destroy_connection(pooled_conn)
        
        # Clear queue
        while not self._available_queue.empty():
            try:
                self._available_queue.get_nowait()
            except queue.Empty:
                break
        
        self._logger.info("Connection pool closed")


class WebDriverPool(ConnectionPool):
    """Specialized connection pool for WebDriver instances."""
    
    def __init__(self, 
                 driver_type: str = "chrome",
                 headless: bool = True,
                 config: PoolConfig = None,
                 name: str = "webdriver_pool"):
        factory = WebDriverFactory(driver_type, headless)
        super().__init__(factory, config, name)


class HTTPConnectionPool(ConnectionPool):
    """Specialized connection pool for HTTP sessions."""
    
    def __init__(self, 
                 base_url: str,
                 config: PoolConfig = None,
                 name: str = "http_pool"):
        factory = HTTPConnectionFactory(base_url)
        super().__init__(factory, config, name)


class ConnectionManager:
    """
    Manager for multiple connection pools.
    
    Provides centralized management of different types of connection pools
    with monitoring and statistics.
    """
    
    def __init__(self):
        self._pools: Dict[str, ConnectionPool] = {}
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.connection_manager")
    
    def register_pool(self, name: str, pool: ConnectionPool) -> None:
        """Register a connection pool."""
        with self._lock:
            self._pools[name] = pool
            self._logger.info(f"Registered connection pool: {name}")
    
    def get_pool(self, name: str) -> Optional[ConnectionPool]:
        """Get a connection pool by name."""
        with self._lock:
            return self._pools.get(name)
    
    def create_webdriver_pool(self, 
                             name: str,
                             driver_type: str = "chrome",
                             headless: bool = True,
                             config: PoolConfig = None) -> WebDriverPool:
        """Create and register a WebDriver pool."""
        pool = WebDriverPool(driver_type, headless, config, name)
        self.register_pool(name, pool)
        return pool
    
    def create_http_pool(self, 
                        name: str,
                        base_url: str,
                        config: PoolConfig = None) -> HTTPConnectionPool:
        """Create and register an HTTP connection pool."""
        pool = HTTPConnectionPool(base_url, config, name)
        self.register_pool(name, pool)
        return pool
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all pools."""
        with self._lock:
            stats = {}
            for name, pool in self._pools.items():
                try:
                    pool_stats = pool.get_stats()
                    stats[name] = {
                        "stats": pool_stats.__dict__,
                        "config": pool.config.__dict__,
                        "connection_info": pool.get_connection_info()
                    }
                except Exception as e:
                    stats[name] = {"error": str(e)}
            return stats
    
    def close_all_pools(self) -> None:
        """Close all connection pools."""
        with self._lock:
            for name, pool in self._pools.items():
                try:
                    pool.close()
                    self._logger.info(f"Closed pool: {name}")
                except Exception as e:
                    self._logger.error(f"Error closing pool {name}: {e}")
            
            self._pools.clear()


# Global connection manager instance
_global_connection_manager: Optional[ConnectionManager] = None


def get_global_connection_manager() -> ConnectionManager:
    """Get or create global connection manager."""
    global _global_connection_manager
    if _global_connection_manager is None:
        _global_connection_manager = ConnectionManager()
    return _global_connection_manager 