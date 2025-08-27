"""
Comprehensive error handling system for the Cryptography Virtual Lab
Provides centralized error handling, logging, and user-friendly error responses.
"""

import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from werkzeug.exceptions import HTTPException
import os

class ErrorHandler:
    """Centralized error handling class"""
    
    def __init__(self, app: Flask = None):
        self.app = app
        self.logger = None
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize error handling for Flask app"""
        self.app = app
        self.setup_logging()
        self.register_error_handlers()
    
    def setup_logging(self):
        """Setup comprehensive logging system"""
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/app.log'),
                logging.FileHandler('logs/error.log'),
                logging.StreamHandler()
            ]
        )
        
        # Create separate loggers for different purposes
        self.logger = logging.getLogger('cryptolab')
        self.security_logger = logging.getLogger('cryptolab.security')
        self.auth_logger = logging.getLogger('cryptolab.auth')
        
        # Set up file handlers for specific log types
        security_handler = logging.FileHandler('logs/security.log')
        security_handler.setFormatter(logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        ))
        self.security_logger.addHandler(security_handler)
        
        auth_handler = logging.FileHandler('logs/auth.log')
        auth_handler.setFormatter(logging.Formatter(
            '%(asctime)s - AUTH - %(levelname)s - %(message)s'
        ))
        self.auth_logger.addHandler(auth_handler)
    
    def register_error_handlers(self):
        """Register all error handlers with Flask app"""
        
        @self.app.errorhandler(400)
        def bad_request(error):
            return self.handle_client_error(error, 'Bad Request', 
                'The request could not be understood by the server.')
        
        @self.app.errorhandler(401)
        def unauthorized(error):
            return self.handle_auth_error(error, 'Unauthorized', 
                'Authentication is required to access this resource.')
        
        @self.app.errorhandler(403)
        def forbidden(error):
            return self.handle_auth_error(error, 'Forbidden', 
                'You do not have permission to access this resource.')
        
        @self.app.errorhandler(404)
        def not_found(error):
            return self.handle_client_error(error, 'Page Not Found', 
                'The requested page could not be found.')
        
        @self.app.errorhandler(405)
        def method_not_allowed(error):
            return self.handle_client_error(error, 'Method Not Allowed', 
                'The requested method is not allowed for this resource.')
        
        @self.app.errorhandler(429)
        def rate_limit_exceeded(error):
            return self.handle_client_error(error, 'Rate Limit Exceeded', 
                'Too many requests. Please try again later.')
        
        @self.app.errorhandler(500)
        def internal_server_error(error):
            return self.handle_server_error(error, 'Internal Server Error', 
                'An unexpected error occurred. Please try again later.')
        
        @self.app.errorhandler(502)
        def bad_gateway(error):
            return self.handle_server_error(error, 'Bad Gateway', 
                'The server received an invalid response.')
        
        @self.app.errorhandler(503)
        def service_unavailable(error):
            return self.handle_server_error(error, 'Service Unavailable', 
                'The service is temporarily unavailable. Please try again later.')
        
        @self.app.errorhandler(Exception)
        def handle_unexpected_error(error):
            return self.handle_server_error(error, 'Unexpected Error', 
                'An unexpected error occurred. Please try again later.')
    
    def handle_client_error(self, error: Exception, title: str, message: str) -> Tuple[str, int]:
        """Handle 4xx client errors"""
        error_id = self.log_error(error, 'CLIENT_ERROR')
        
        if request.is_json:
            return jsonify({
                'error': title,
                'message': message,
                'error_id': error_id,
                'status_code': getattr(error, 'code', 400)
            }), getattr(error, 'code', 400)
        
        return render_template('errors/client_error.html', 
                             title=title, 
                             message=message, 
                             error_id=error_id,
                             status_code=getattr(error, 'code', 400)), getattr(error, 'code', 400)
    
    def handle_auth_error(self, error: Exception, title: str, message: str) -> Tuple[str, int]:
        """Handle authentication/authorization errors"""
        error_id = self.log_security_event(error, 'AUTH_ERROR')
        
        if request.is_json:
            return jsonify({
                'error': title,
                'message': message,
                'error_id': error_id,
                'status_code': getattr(error, 'code', 401)
            }), getattr(error, 'code', 401)
        
        # Redirect to appropriate login page for auth errors
        flash(message, 'error')
        if getattr(error, 'code', 401) == 403:
            return redirect(url_for('home'))
        return redirect(url_for('student_login'))
    
    def handle_server_error(self, error: Exception, title: str, message: str) -> Tuple[str, int]:
        """Handle 5xx server errors"""
        error_id = self.log_error(error, 'SERVER_ERROR')
        
        if request.is_json:
            return jsonify({
                'error': title,
                'message': message,
                'error_id': error_id,
                'status_code': getattr(error, 'code', 500)
            }), getattr(error, 'code', 500)
        
        return render_template('errors/server_error.html', 
                             title=title, 
                             message=message, 
                             error_id=error_id,
                             status_code=getattr(error, 'code', 500)), getattr(error, 'code', 500)
    
    def log_error(self, error: Exception, error_type: str) -> str:
        """Log error with full context"""
        error_id = f"ERR_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{id(error)}"
        
        error_context = {
            'error_id': error_id,
            'error_type': error_type,
            'error_class': error.__class__.__name__,
            'error_message': str(error),
            'request_method': request.method if request else 'N/A',
            'request_url': request.url if request else 'N/A',
            'request_ip': request.remote_addr if request else 'N/A',
            'user_agent': request.headers.get('User-Agent', 'N/A') if request else 'N/A',
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc()
        }
        
        self.logger.error(f"Error {error_id}: {error_context}")
        return error_id
    
    def log_security_event(self, error: Exception, event_type: str) -> str:
        """Log security-related events"""
        error_id = f"SEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{id(error)}"
        
        security_context = {
            'error_id': error_id,
            'event_type': event_type,
            'error_class': error.__class__.__name__,
            'error_message': str(error),
            'request_method': request.method if request else 'N/A',
            'request_url': request.url if request else 'N/A',
            'request_ip': request.remote_addr if request else 'N/A',
            'user_agent': request.headers.get('User-Agent', 'N/A') if request else 'N/A',
            'timestamp': datetime.now().isoformat(),
            'session_data': dict(request.session) if request and hasattr(request, 'session') else {}
        }
        
        self.security_logger.warning(f"Security Event {error_id}: {security_context}")
        return error_id
    
    def log_auth_event(self, username: str, event_type: str, success: bool, details: str = ""):
        """Log authentication events"""
        auth_context = {
            'username': username,
            'event_type': event_type,
            'success': success,
            'details': details,
            'request_ip': request.remote_addr if request else 'N/A',
            'user_agent': request.headers.get('User-Agent', 'N/A') if request else 'N/A',
            'timestamp': datetime.now().isoformat()
        }
        
        log_level = logging.INFO if success else logging.WARNING
        self.auth_logger.log(log_level, f"Auth Event: {auth_context}")

class ValidationErrorHandler:
    """Handle validation errors specifically"""
    
    @staticmethod
    def handle_validation_error(error_message: str, field: str = None) -> Dict[str, Any]:
        """
        Handle validation errors consistently
        
        Args:
            error_message: The validation error message
            field: The field that failed validation (optional)
            
        Returns:
            Standardized error response
        """
        error_response = {
            'error': 'Validation Error',
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        }
        
        if field:
            error_response['field'] = field
        
        return error_response
    
    @staticmethod
    def handle_form_validation_errors(errors: Dict[str, str]) -> None:
        """
        Handle multiple form validation errors
        
        Args:
            errors: Dictionary of field names to error messages
        """
        for field, message in errors.items():
            flash(f"{field.title()}: {message}", 'error')

class DatabaseErrorHandler:
    """Handle database-related errors"""
    
    @staticmethod
    def handle_connection_error() -> Dict[str, Any]:
        """Handle database connection errors"""
        return {
            'error': 'Database Connection Error',
            'message': 'Unable to connect to the database. Please try again later.',
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def handle_integrity_error(details: str = "") -> Dict[str, Any]:
        """Handle database integrity constraint errors"""
        return {
            'error': 'Data Integrity Error',
            'message': 'The operation violates data integrity constraints.',
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def handle_not_found_error(resource: str) -> Dict[str, Any]:
        """Handle resource not found errors"""
        return {
            'error': 'Resource Not Found',
            'message': f'The requested {resource} was not found.',
            'timestamp': datetime.now().isoformat()
        }

def create_error_response(error_type: str, message: str, status_code: int = 400, 
                         details: Dict[str, Any] = None) -> Tuple[Dict[str, Any], int]:
    """
    Create standardized error response
    
    Args:
        error_type: Type of error
        message: Error message
        status_code: HTTP status code
        details: Additional error details
        
    Returns:
        Tuple of (error_dict, status_code)
    """
    error_response = {
        'error': error_type,
        'message': message,
        'status_code': status_code,
        'timestamp': datetime.now().isoformat()
    }
    
    if details:
        error_response['details'] = details
    
    return error_response, status_code