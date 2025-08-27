"""
Configuration management for Cryptography Virtual Lab
Provides environment-specific configurations and security settings.
"""

import os
from datetime import timedelta
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Basic Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Session Configuration
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=int(os.environ.get('SESSION_TIMEOUT_HOURS', '1')))
    
    # Security Configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Application Configuration
    APP_NAME = 'Cryptography Virtual Lab'
    APP_VERSION = '1.0.0'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # Database Configuration (for future use)
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///cryptolab.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # Rate Limiting Configuration
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    RATELIMIT_DEFAULT = "100 per hour"
    
    # Email Configuration (for future notifications)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@cryptolab.edu')
    
    # API Configuration
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '60 per minute')
    API_VERSION = 'v1'
    
    # Security Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; font-src 'self' https://cdnjs.cloudflare.com; img-src 'self' data:;"
    }
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create necessary directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Set security headers
        @app.after_request
        def set_security_headers(response):
            for header, value in Config.SECURITY_HEADERS.items():
                response.headers[header] = value
            return response

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Less strict security for development
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False  # Disable CSRF for easier development
    
    # More verbose logging
    LOG_LEVEL = 'DEBUG'
    
    # Relaxed rate limiting
    RATELIMIT_DEFAULT = "1000 per hour"
    API_RATE_LIMIT = '600 per minute'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Use in-memory database for testing
    DATABASE_URL = 'sqlite:///:memory:'
    
    # Disable security features for testing
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    
    # Disable rate limiting for testing
    RATELIMIT_ENABLED = False
    
    # Use temporary directories
    UPLOAD_FOLDER = '/tmp/cryptolab_test_uploads'
    LOG_FILE = '/tmp/cryptolab_test.log'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Strict security settings
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True
    
    # Production logging
    LOG_LEVEL = 'WARNING'
    
    # Strict rate limiting
    RATELIMIT_DEFAULT = "50 per hour"
    API_RATE_LIMIT = '30 per minute'
    
    # Production database
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://user:pass@localhost/cryptolab'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Production-specific initialization
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Set up file logging with rotation
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler('logs/cryptolab.log', maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Cryptography Virtual Lab startup')

class DockerConfig(ProductionConfig):
    """Docker container configuration"""
    
    # Use environment variables for all external services
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@db:5432/cryptolab')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
    
    # Container-specific paths
    LOG_FILE = '/app/logs/app.log'
    UPLOAD_FOLDER = '/app/uploads'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """
    Get configuration class based on environment
    
    Args:
        config_name: Configuration name (development, testing, production, docker)
        
    Returns:
        Configuration class
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])

class SecurityConfig:
    """Security-specific configuration"""
    
    # Password requirements
    PASSWORD_MIN_LENGTH = 6
    PASSWORD_MAX_LENGTH = 128
    PASSWORD_REQUIRE_UPPERCASE = False
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_NUMBERS = True
    PASSWORD_REQUIRE_SYMBOLS = False
    
    # Account lockout settings
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=15)
    
    # Session security
    SESSION_REGENERATE_ON_LOGIN = True
    SESSION_INVALIDATE_ON_ROLE_CHANGE = True
    
    # File upload security
    SCAN_UPLOADS = os.environ.get('SCAN_UPLOADS', 'False').lower() == 'true'
    QUARANTINE_SUSPICIOUS_FILES = True
    
    # API security
    API_KEY_REQUIRED = os.environ.get('API_KEY_REQUIRED', 'False').lower() == 'true'
    API_RATE_LIMIT_PER_USER = '100 per hour'
    
    # Audit logging
    LOG_ALL_REQUESTS = os.environ.get('LOG_ALL_REQUESTS', 'False').lower() == 'true'
    LOG_SENSITIVE_DATA = False  # Never log passwords, tokens, etc.
    
    # Content Security
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    TRUSTED_PROXIES = os.environ.get('TRUSTED_PROXIES', '').split(',') if os.environ.get('TRUSTED_PROXIES') else []

class FeatureFlags:
    """Feature flags for enabling/disabling functionality"""
    
    # Authentication features
    ENABLE_REGISTRATION = os.environ.get('ENABLE_REGISTRATION', 'False').lower() == 'true'
    ENABLE_PASSWORD_RESET = os.environ.get('ENABLE_PASSWORD_RESET', 'False').lower() == 'true'
    ENABLE_TWO_FACTOR_AUTH = os.environ.get('ENABLE_TWO_FACTOR_AUTH', 'False').lower() == 'true'
    
    # Lab features
    ENABLE_FILE_UPLOAD = os.environ.get('ENABLE_FILE_UPLOAD', 'True').lower() == 'true'
    ENABLE_PROGRESS_TRACKING = os.environ.get('ENABLE_PROGRESS_TRACKING', 'True').lower() == 'true'
    ENABLE_ASSIGNMENTS = os.environ.get('ENABLE_ASSIGNMENTS', 'True').lower() == 'true'
    
    # Administrative features
    ENABLE_USER_MANAGEMENT = os.environ.get('ENABLE_USER_MANAGEMENT', 'True').lower() == 'true'
    ENABLE_SYSTEM_MONITORING = os.environ.get('ENABLE_SYSTEM_MONITORING', 'True').lower() == 'true'
    ENABLE_AUDIT_LOGS = os.environ.get('ENABLE_AUDIT_LOGS', 'True').lower() == 'true'
    
    # API features
    ENABLE_REST_API = os.environ.get('ENABLE_REST_API', 'False').lower() == 'true'
    ENABLE_WEBHOOKS = os.environ.get('ENABLE_WEBHOOKS', 'False').lower() == 'true'
    
    # Experimental features
    ENABLE_AI_ASSISTANCE = os.environ.get('ENABLE_AI_ASSISTANCE', 'False').lower() == 'true'
    ENABLE_ADVANCED_ANALYTICS = os.environ.get('ENABLE_ADVANCED_ANALYTICS', 'False').lower() == 'true'