"""
Input validation utilities for the Cryptography Virtual Lab
Provides comprehensive validation for user inputs, authentication, and data integrity.
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from functools import wraps
from flask import request, jsonify, flash

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

class InputValidator:
    """Comprehensive input validation class"""
    
    # Regex patterns for validation
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PASSWORD_PATTERN = re.compile(r'^.{6,128}$')  # At least 6 characters, max 128
    NAME_PATTERN = re.compile(r'^[a-zA-Z\s]{2,50}$')
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Validate username format and requirements
        
        Args:
            username: Username to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not username:
            return False, "Username is required"
        
        if not isinstance(username, str):
            return False, "Username must be a string"
        
        username = username.strip()
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(username) > 20:
            return False, "Username must be no more than 20 characters long"
        
        if not InputValidator.USERNAME_PATTERN.match(username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password strength and requirements
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password:
            return False, "Password is required"
        
        if not isinstance(password, str):
            return False, "Password must be a string"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if len(password) > 128:
            return False, "Password must be no more than 128 characters long"
        
        # Check for at least one letter and one number (basic strength)
        if not re.search(r'[a-zA-Z]', password):
            return False, "Password must contain at least one letter"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email format
        
        Args:
            email: Email to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return False, "Email is required"
        
        if not isinstance(email, str):
            return False, "Email must be a string"
        
        email = email.strip().lower()
        
        if len(email) > 254:  # RFC 5321 limit
            return False, "Email address is too long"
        
        if not InputValidator.EMAIL_PATTERN.match(email):
            return False, "Invalid email format"
        
        return True, ""
    
    @staticmethod
    def validate_full_name(name: str) -> Tuple[bool, str]:
        """
        Validate full name format
        
        Args:
            name: Full name to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name:
            return False, "Full name is required"
        
        if not isinstance(name, str):
            return False, "Full name must be a string"
        
        name = name.strip()
        
        if len(name) < 2:
            return False, "Full name must be at least 2 characters long"
        
        if len(name) > 50:
            return False, "Full name must be no more than 50 characters long"
        
        if not InputValidator.NAME_PATTERN.match(name):
            return False, "Full name can only contain letters and spaces"
        
        return True, ""
    
    @staticmethod
    def validate_role(role: str) -> Tuple[bool, str]:
        """
        Validate user role
        
        Args:
            role: Role to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid_roles = ['student', 'faculty', 'admin']
        
        if not role:
            return False, "Role is required"
        
        if not isinstance(role, str):
            return False, "Role must be a string"
        
        role = role.strip().lower()
        
        if role not in valid_roles:
            return False, f"Role must be one of: {', '.join(valid_roles)}"
        
        return True, ""
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """
        Sanitize input string to prevent XSS and injection attacks
        
        Args:
            input_str: String to sanitize
            
        Returns:
            Sanitized string
        """
        if not isinstance(input_str, str):
            return str(input_str)
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00', '\r', '\n']
        sanitized = input_str
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized.strip()
    
    @staticmethod
    def validate_json_structure(data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, str]:
        """
        Validate JSON data structure
        
        Args:
            data: Dictionary to validate
            required_fields: List of required field names
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(data, dict):
            return False, "Data must be a valid JSON object"
        
        missing_fields = []
        for field in required_fields:
            if field not in data:
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        return True, ""

def validate_login_data(f):
    """
    Decorator to validate login form data
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            # Validate username
            is_valid, error = InputValidator.validate_username(username)
            if not is_valid:
                flash(error, 'error')
                return f(*args, **kwargs)
            
            # Validate password (basic validation for login)
            if not password:
                flash('Password is required', 'error')
                return f(*args, **kwargs)
            
            if len(password) > 128:
                flash('Password is too long', 'error')
                return f(*args, **kwargs)
            
            # Sanitize inputs
            request.form = request.form.copy()
            request.form['username'] = InputValidator.sanitize_input(username)
            request.form['password'] = password  # Don't sanitize password as it might contain special chars
        
        return f(*args, **kwargs)
    return decorated_function

def validate_api_request(required_fields: List[str]):
    """
    Decorator to validate API request data
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == 'POST':
                try:
                    data = request.get_json()
                    if not data:
                        return jsonify({'error': 'Invalid JSON data'}), 400
                    
                    # Validate structure
                    is_valid, error = InputValidator.validate_json_structure(data, required_fields)
                    if not is_valid:
                        return jsonify({'error': error}), 400
                    
                    # Sanitize string inputs
                    for key, value in data.items():
                        if isinstance(value, str):
                            data[key] = InputValidator.sanitize_input(value)
                    
                except Exception as e:
                    return jsonify({'error': 'Invalid request format'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

class SecurityValidator:
    """Security-focused validation utilities"""
    
    @staticmethod
    def is_safe_redirect_url(url: str) -> bool:
        """
        Check if a redirect URL is safe (prevents open redirect attacks)
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is safe for redirect
        """
        if not url:
            return False
        
        # Only allow relative URLs or URLs from the same domain
        if url.startswith('/') and not url.startswith('//'):
            return True
        
        # Block external URLs
        if url.startswith(('http://', 'https://', '//')):
            return False
        
        return True
    
    @staticmethod
    def validate_file_upload(filename: str, allowed_extensions: List[str]) -> Tuple[bool, str]:
        """
        Validate file upload security
        
        Args:
            filename: Name of uploaded file
            allowed_extensions: List of allowed file extensions
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not filename:
            return False, "Filename is required"
        
        # Check for directory traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            return False, "Invalid filename"
        
        # Check file extension
        if '.' not in filename:
            return False, "File must have an extension"
        
        extension = filename.rsplit('.', 1)[1].lower()
        if extension not in allowed_extensions:
            return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        
        return True, ""