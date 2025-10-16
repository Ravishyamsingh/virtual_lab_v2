


import json
from functools import wraps
from flask import session, redirect, url_for, flash

def load_users():
    with open('data/users.json', 'r') as file:
        return json.load(file)['users']

def check_credentials(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user  # Return the full user object instead of just True
    return None

def get_user_by_username(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'] is None:
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated_function

def faculty_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'] is None:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('faculty_login'))
        
        user = get_user_by_username(session['user']['username'])
        if not user or user['role'] != 'faculty':
            flash('Faculty access required.', 'error')
            return redirect(url_for('faculty_login'))
        
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'] is None:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('student_login'))
        
        user = get_user_by_username(session['user']['username'])
        if not user or user['role'] != 'student':
            flash('Student access required.', 'error')
            return redirect(url_for('student_login'))
        
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session or session['user'] is None:
                flash('Please log in to access this page.', 'error')
                if required_role == 'faculty':
                    return redirect(url_for('faculty_login'))
                else:
                    return redirect(url_for('student_login'))
            
            user = get_user_by_username(session['user']['username'])
            if not user or user['role'] != required_role:
                flash(f'{required_role.title()} access required.', 'error')
                if required_role == 'faculty':
                    return redirect(url_for('faculty_login'))
                else:
                    return redirect(url_for('student_login'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
