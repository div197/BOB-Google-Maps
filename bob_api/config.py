"""bob_api.config

Configuration management for BOB Google Maps API v0.6.0
Environment-based settings with divine defaults.

Made with 🙏 following Niṣkāma Karma Yoga principles
"""

import os
from typing import List, Optional
from functools import lru_cache

try:
    from pydantic_settings import BaseSettings
    from pydantic import Field, field_validator
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings, Field, validator as field_validator

__all__ = ["Settings", "get_settings"]


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    APP_NAME: str = Field("BOB Google Maps API", description="Application name")
    VERSION: str = Field("0.6.0", description="Application version")
    ENVIRONMENT: str = Field("development", description="Environment (development/staging/production)")
    DEBUG: bool = Field(False, description="Debug mode")
    
    # Server
    HOST: str = Field("0.0.0.0", description="Server host")
    PORT: int = Field(8000, description="Server port")
    WORKERS: int = Field(1, description="Number of worker processes")
    
    # Security
    SECRET_KEY: str = Field("your-secret-key-change-in-production", description="Secret key for JWT")
    API_KEY: Optional[str] = Field(None, description="API key for authentication")
    ALLOWED_HOSTS: List[str] = Field(["*"], description="Allowed hosts")
    ALLOWED_ORIGINS: List[str] = Field(["*"], description="Allowed CORS origins")
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = Field(100, description="Requests per minute per IP")
    RATE_LIMIT_WINDOW: int = Field(60, description="Rate limit window in seconds")
    
    # Scraping
    DEFAULT_BACKEND: str = Field("auto", description="Default scraping backend")
    DEFAULT_TIMEOUT: int = Field(60, description="Default timeout in seconds")
    MAX_WORKERS: int = Field(4, description="Maximum concurrent workers")
    MAX_BATCH_SIZE: int = Field(100, description="Maximum batch size")
    
    # Database (for future use)
    DATABASE_URL: Optional[str] = Field(None, description="Database connection URL")
    REDIS_URL: Optional[str] = Field(None, description="Redis connection URL")
    
    # Monitoring
    ENABLE_METRICS: bool = Field(True, description="Enable metrics collection")
    METRICS_RETENTION_DAYS: int = Field(30, description="Metrics retention period")
    
    # Logging
    LOG_LEVEL: str = Field("INFO", description="Logging level")
    LOG_FORMAT: str = Field("json", description="Log format (json/text)")
    LOG_FILE: Optional[str] = Field(None, description="Log file path")
    
    # Cloud Deployment
    CLOUD_PROVIDER: Optional[str] = Field(None, description="Cloud provider (aws/gcp/azure)")
    DEPLOYMENT_REGION: Optional[str] = Field(None, description="Deployment region")
    
    # AWS Settings
    AWS_ACCESS_KEY_ID: Optional[str] = Field(None, description="AWS access key")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(None, description="AWS secret key")
    AWS_REGION: str = Field("us-east-1", description="AWS region")
    AWS_S3_BUCKET: Optional[str] = Field(None, description="S3 bucket for storage")
    
    # GCP Settings
    GCP_PROJECT_ID: Optional[str] = Field(None, description="GCP project ID")
    GCP_SERVICE_ACCOUNT_KEY: Optional[str] = Field(None, description="GCP service account key")
    GCP_REGION: str = Field("us-central1", description="GCP region")
    
    # Azure Settings
    AZURE_SUBSCRIPTION_ID: Optional[str] = Field(None, description="Azure subscription ID")
    AZURE_RESOURCE_GROUP: Optional[str] = Field(None, description="Azure resource group")
    AZURE_REGION: str = Field("eastus", description="Azure region")
    
    # Docker Settings
    DOCKER_REGISTRY: str = Field("docker.io", description="Docker registry")
    DOCKER_NAMESPACE: str = Field("divyanshu", description="Docker namespace")
    DOCKER_IMAGE_NAME: str = Field("bob-google-maps", description="Docker image name")
    
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v):
        """Validate environment value."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"Log level must be one of: {allowed}")
        return v.upper()
    
    @field_validator("DEFAULT_BACKEND")
    @classmethod
    def validate_backend(cls, v):
        """Validate scraping backend."""
        allowed = ["auto", "selenium", "playwright"]
        if v not in allowed:
            raise ValueError(f"Backend must be one of: {allowed}")
        return v
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse allowed origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v):
        """Parse allowed hosts from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT == "development"
    
    @property
    def database_config(self) -> dict:
        """Get database configuration."""
        return {
            "url": self.DATABASE_URL,
            "echo": self.DEBUG and not self.is_production
        }
    
    @property
    def redis_config(self) -> dict:
        """Get Redis configuration."""
        return {
            "url": self.REDIS_URL or "redis://localhost:6379/0"
        }
    
    @property
    def cors_config(self) -> dict:
        """Get CORS configuration."""
        return {
            "allow_origins": self.ALLOWED_ORIGINS,
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["*"]
        }
    
    @property
    def logging_config(self) -> dict:
        """Get logging configuration."""
        return {
            "level": self.LOG_LEVEL,
            "format": self.LOG_FORMAT,
            "file": self.LOG_FILE
        }
    
    @property
    def deployment_config(self) -> dict:
        """Get deployment configuration."""
        return {
            "cloud_provider": self.CLOUD_PROVIDER,
            "region": self.DEPLOYMENT_REGION,
            "docker_registry": self.DOCKER_REGISTRY,
            "docker_namespace": self.DOCKER_NAMESPACE,
            "image_name": self.DOCKER_IMAGE_NAME
        }
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings() 