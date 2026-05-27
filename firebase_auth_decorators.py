"""
Firebase-based Authentication Decorators
Replace old auth decorators with Firebase-aware versions
"""

from functools import wraps
from flask import session, redirect, url_for, flash
import sys

def validate_session_user():
    """
    Validate that the current session has a valid user
    
    Returns:
        dict or None: User object if valid, None if invalid
    """
    if 'user' not in session or not session.get('user'):
        return None
    
    user = session['user']
    
    # Validate required fields
    required_fields = {'uid', 'email', 'role', 'username'}
    if not all(field in user for field in required_fields):
        session.clear()
        return None
    
    # Validate role
    valid_roles = {'student', 'faculty'}
    if user.get('role') not in valid_roles:
        session.clear()
        return None
    
    return user

def firebase_login_required(f):
    """Decorator to check if user is authenticated via Firebase"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = validate_session_user()
        if not user:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('firebase_auth.firebase_login'))
        return f(*args, **kwargs)
    return decorated_function

def firebase_faculty_required(f):
    """Decorator to ensure user is faculty"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = validate_session_user()
        if not user:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('firebase_auth.firebase_login'))
        
        if user.get('role') != 'faculty':
            flash('Faculty access required.', 'error')
            return redirect(url_for('firebase_auth.firebase_login'))
        
        return f(*args, **kwargs)
    return decorated_function

def firebase_student_required(f):
    """Decorator to ensure user is student"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = validate_session_user()
        if not user:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('firebase_auth.firebase_login'))
        
        if user.get('role') != 'student':
            flash('Student access required.', 'error')
            return redirect(url_for('firebase_auth.firebase_login'))
        
        return f(*args, **kwargs)
    return decorated_function

def firebase_role_required(required_role):
    """Decorator to check for specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = validate_session_user()
            if not user:
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('firebase_auth.firebase_login'))
            
            if user.get('role') != required_role:
                flash(f'{required_role.title()} access required.', 'error')
                return redirect(url_for('firebase_auth.firebase_login'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
