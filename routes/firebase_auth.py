"""
Firebase Authentication Routes
Handles Firebase login, signup, and session management
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from firebase_config import verify_firebase_token, FIREBASE_WEB_CONFIG
from firebase_db import FirebaseDB
from datetime import datetime
from functools import wraps
import os

# Allowed roles - prevent role escalation
ALLOWED_ROLES = {'student', 'faculty'}

# Optional allowlists for faculty assignment (comma-separated)
FACULTY_EMAIL_ALLOWLIST = {
    email.strip().lower()
    for email in os.getenv('FACULTY_EMAIL_ALLOWLIST', '').split(',')
    if email.strip()
}
FACULTY_DOMAIN_ALLOWLIST = {
    domain.strip().lower()
    for domain in os.getenv('FACULTY_DOMAIN_ALLOWLIST', '').split(',')
    if domain.strip()
}

def is_faculty_allowed(email):
    """Return True if the email is allowed to self-assign faculty."""
    if not email:
        return False

    email = email.strip().lower()
    if email in FACULTY_EMAIL_ALLOWLIST:
        return True

    if '@' in email:
        domain = email.split('@', 1)[1]
        if domain in FACULTY_DOMAIN_ALLOWLIST:
            return True

    return False

firebase_auth_bp = Blueprint('firebase_auth', __name__)

def require_json(f):
    """Decorator to verify request is JSON and has Content-Type set"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 400
        return f(*args, **kwargs)
    return decorated_function

def apply_rate_limit(max_calls, time_window_seconds):
    """Apply rate limiting to a route using manual tracking"""
    from time import time
    
    # Simple in-memory rate limit tracking
    request_history = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = get_remote_address()
            endpoint_key = f'{request.endpoint}_{client_ip}'
            current_time = time()
            
            # Initialize if not exists
            if endpoint_key not in request_history:
                request_history[endpoint_key] = []
            
            # Clean old entries outside the time window
            request_history[endpoint_key] = [
                req_time for req_time in request_history[endpoint_key]
                if current_time - req_time < time_window_seconds
            ]
            
            # Check if limit exceeded
            if len(request_history[endpoint_key]) >= max_calls:
                return jsonify({
                    'success': False,
                    'error': f'Too many requests. Maximum {max_calls} attempts per {time_window_seconds} seconds allowed.',
                    'retry_after': int(time_window_seconds)
                }), 429
            
            # Record this request
            request_history[endpoint_key].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_remote_address():
    """Get remote client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

@firebase_auth_bp.route('/login')
def firebase_login():
    """Firebase login page - Modern UI"""
    # Redirect to dashboard if already logged in
    if 'user' in session and session.get('user'):
        user = session['user']
        if user.get('role') == 'faculty':
            return redirect(url_for('faculty_dashboard'))
        return redirect(url_for('student_dashboard'))
    
    return render_template('new_firebase_login.html', 
                         firebase_config=FIREBASE_WEB_CONFIG)

@firebase_auth_bp.route('/api/check-session', methods=['GET'])
def check_session():
    """Check if user has a valid backend session
    Returns success if session exists, 401 if not
    """
    try:
        if 'user' in session and session.get('user'):
            user = session['user']
            return jsonify({
                'success': True,
                'user': user.get('email'),
                'role': user.get('role'),
                'redirect': f"/{user.get('role')}" if user.get('role') else '/student'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No active session'
            }), 401
    except Exception as e:
        print(f"Session check error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Session check failed'
        }), 500

@firebase_auth_bp.route('/api/authenticate', methods=['POST'])
@require_json
@apply_rate_limit(max_calls=5, time_window_seconds=60)  # 5 attempts per 60 seconds (brute force protection)
def authenticate():
    """
    Authenticate user with Firebase token
    Verify token and save user to database
    Rate limit: 5 attempts per minute per IP
    """
    try:
        data = request.get_json()
        token = data.get('token', '').strip()
        user_type = data.get('userType', 'student').lower().strip()
        
        # Validate input
        if not token:
            return jsonify({
                'success': False,
                'error': 'Token is required'
            }), 400
        
        # Prevent role escalation - only allow predefined roles
        if user_type not in ALLOWED_ROLES:
            return jsonify({
                'success': False,
                'error': f'Invalid user type. Must be one of: {", ".join(ALLOWED_ROLES)}'
            }), 400
        
        # Verify Firebase token with error handling
        try:
            print(f"🔐 Verifying token (length: {len(token)} chars)")
            decoded_token = verify_firebase_token(token)
            print(f"✅ Token verified successfully. UID: {decoded_token.get('uid')}")
        except Exception as e:
            print(f"❌ Token verification error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': f'Invalid or expired token: {str(e)}'
            }), 401
        
        if not decoded_token:
            return jsonify({
                'success': False,
                'error': 'Token verification failed. Please login again.'
            }), 401
        
        # Extract user information
        uid = decoded_token.get('uid')
        email = decoded_token.get('email', '').strip()
        display_name = decoded_token.get('name', email.split('@')[0] if email else 'User')
        
        if not uid or not email:
            return jsonify({
                'success': False,
                'error': 'Invalid token data. Missing uid or email.'
            }), 400
        
        # Get or create user in Firebase Database
        user_data = FirebaseDB.get_user(uid)

        # Determine effective role (never trust client role for escalation)
        if user_data and user_data.get('role') in ALLOWED_ROLES:
            effective_role = user_data.get('role')
        else:
            if user_type == 'faculty' and not is_faculty_allowed(email):
                return jsonify({
                    'success': False,
                    'error': 'Faculty access requires approval. Please contact the administrator.'
                }), 403
            effective_role = 'faculty' if user_type == 'faculty' else 'student'

        if not user_data:
            # First time login - create user record
            user_data = {
                'uid': uid,
                'email': email,
                'display_name': display_name,
                'role': effective_role,
                'profile_picture': decoded_token.get('picture', ''),
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat(),
                'login_count': 1,
                'status': 'active',
                'email_verified': decoded_token.get('email_verified', False)
            }
            if not FirebaseDB.save_user(uid, user_data):
                return jsonify({
                    'success': False,
                    'error': 'Failed to create user record. Please try again.'
                }), 500
        else:
            # Update last login info - role only updated if missing or invalid
            updates = {
                'last_login': datetime.now().isoformat(),
                'login_count': (user_data.get('login_count', 0) + 1),
                'email_verified': decoded_token.get('email_verified', False)
            }
            # Only update role if it was never set or invalid
            if user_data.get('role') not in ALLOWED_ROLES:
                updates['role'] = effective_role
            
            if not FirebaseDB.update_user(uid, updates):
                return jsonify({
                    'success': False,
                    'error': 'Failed to update user record. Please try again.'
                }), 500
            
            # Refresh user_data after update
            user_data = FirebaseDB.get_user(uid)
        
        # Log activity
        try:
            FirebaseDB.save_activity(uid, 'LOGIN', {
                'email': email,
                'user_type': effective_role,
                'ip_address': request.remote_addr
            })
        except Exception as e:
            print(f"Activity logging error: {str(e)}")
            # Don't fail login if activity logging fails
        
        # Store in Flask session with security measures
        role_for_session = user_data.get('role') if user_data else effective_role
        session['user'] = {
            'uid': uid,
            'email': email,
            'username': email.split('@')[0],
            'display_name': display_name,
            'role': role_for_session,  # Use role from database
            'profile_picture': user_data.get('profile_picture', '')
        }
        session['firebase_token'] = token
        session.permanent = True
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': session['user'],
            'redirect': '/faculty' if role_for_session == 'faculty' else '/student'
        }), 200
        
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Authentication failed. Please try again later.'
        }), 500

@firebase_auth_bp.route('/api/logout', methods=['POST'])
@require_json
@apply_rate_limit(max_calls=10, time_window_seconds=60)  # 10 attempts per 60 seconds
def logout():
    """Logout user and clear session
    Rate limit: 10 attempts per minute per IP
    """
    try:
        # Log logout activity before clearing session
        if 'user' in session and session.get('user'):
            uid = session['user'].get('uid')
            if uid:
                try:
                    FirebaseDB.save_activity(uid, 'LOGOUT', {
                        'email': session['user'].get('email'),
                        'ip_address': request.remote_addr
                    })
                except Exception as e:
                    print(f"Logout activity logging error: {str(e)}")
        
        # Clear session data
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        print(f"Logout error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error during logout. Session may still be active.'
        }), 500

@firebase_auth_bp.route('/api/profile', methods=['GET'])
def get_profile():
    """Get current user profile"""
    try:
        if 'user' not in session or not session.get('user'):
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        uid = session['user'].get('uid')
        if not uid:
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
        
        user_data = FirebaseDB.get_user(uid)
        
        if user_data:
            # Filter sensitive data before returning
            safe_user_data = {
                'uid': user_data.get('uid'),
                'email': user_data.get('email'),
                'display_name': user_data.get('display_name'),
                'role': user_data.get('role'),
                'profile_picture': user_data.get('profile_picture'),
                'bio': user_data.get('bio', ''),
                'created_at': user_data.get('created_at'),
                'last_login': user_data.get('last_login')
            }
            return jsonify({
                'success': True,
                'user': safe_user_data
            }), 200
        else:
            return jsonify({'success': False, 'error': 'User not found'}), 404
            
    except Exception as e:
        print(f"Get profile error: {str(e)}")
        return jsonify({'success': False, 'error': 'Error retrieving profile'}), 500

@firebase_auth_bp.route('/api/profile', methods=['PUT'])
@require_json
def update_profile():
    """Update user profile"""
    try:
        if 'user' not in session or not session.get('user'):
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        uid = session['user'].get('uid')
        if not uid:
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
        
        data = request.get_json()
        
        # Only allow updating specific fields - prevent privilege escalation
        allowed_fields = ['display_name', 'bio', 'profile_picture']
        updates = {}
        
        for field in allowed_fields:
            if field in data:
                value = data[field]
                # Validate field values
                if field == 'display_name' and value:
                    if len(value) > 255:
                        return jsonify({'success': False, 'error': 'Display name too long (max 255 chars)'}), 400
                    updates['display_name'] = value.strip()
                elif field == 'bio' and value:
                    if len(value) > 1000:
                        return jsonify({'success': False, 'error': 'Bio too long (max 1000 chars)'}), 400
                    updates['bio'] = value.strip()
                elif field == 'profile_picture' and value:
                    # Basic URL validation
                    if not value.startswith(('http://', 'https://', 'data:')):
                        return jsonify({'success': False, 'error': 'Invalid profile picture URL'}), 400
                    updates['profile_picture'] = value
        
        if not updates:
            return jsonify({'success': False, 'error': 'No valid fields to update'}), 400
        
        if not FirebaseDB.update_user(uid, updates):
            return jsonify({'success': False, 'error': 'Failed to update profile'}), 500
        
        # Update session
        if 'display_name' in updates:
            session['user']['display_name'] = updates['display_name']
        
        updated_user = FirebaseDB.get_user(uid)
        safe_user_data = {
            'uid': updated_user.get('uid'),
            'email': updated_user.get('email'),
            'display_name': updated_user.get('display_name'),
            'role': updated_user.get('role'),
            'profile_picture': updated_user.get('profile_picture'),
            'bio': updated_user.get('bio', '')
        }
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': safe_user_data
        }), 200
            
    except Exception as e:
        print(f"Update profile error: {str(e)}")
        return jsonify({'success': False, 'error': 'Error updating profile'}), 500

@firebase_auth_bp.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get user statistics"""
    try:
        if 'user' not in session or not session.get('user'):
            return jsonify({'success': False, 'error': 'Not authenticated'}), 401
        
        uid = session['user'].get('uid')
        if not uid:
            return jsonify({'success': False, 'error': 'Invalid session'}), 401
        
        stats = FirebaseDB.get_user_statistics(uid)
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
    except Exception as e:
        print(f"Get statistics error: {str(e)}")
        return jsonify({'success': False, 'error': 'Error retrieving statistics'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
