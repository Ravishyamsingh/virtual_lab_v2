from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from flask_session import Session
from config import get_config, FeatureFlags
from dashboard_stats import get_dashboard_stats, get_recent_activities, get_lab_modules_info, get_student_list, get_quick_actions
from utils.error_handlers import ErrorHandler
from utils.validators import validate_login_data, InputValidator
from routes.mono_alphabetic import mono_alphabetic
from routes.shift_cipher import shift_cipher
from routes.one_time_pad import one_time_pad
from routes.hash_function import hash_function
from routes.des_algorithm import des_algorithm
from routes.aes_algorithm import aes_algorithm
from routes.message_auth import message_auth
from routes.dsa_algorithm import dsa_algorithm
from routes.assignments import assignments
from routes.firebase_auth import firebase_auth_bp
from firebase_db import FirebaseDB
from firebase_config import FIREBASE_WEB_CONFIG
from firebase_auth_decorators import firebase_student_required, firebase_faculty_required
import os

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    config_class.init_app(app)
    
    # Initialize Flask-Session for secure session handling
    Session(app)
    
    # Initialize error handling
    error_handler = ErrorHandler(app)
    
    # Handle rate limit exceeded errors (429)
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            'success': False,
            'error': 'Too many requests. Please try again later.'
        }), 429
    
    # Register Firebase Authentication Blueprint
    app.register_blueprint(firebase_auth_bp)
    
    # Register blueprints
    app.register_blueprint(mono_alphabetic)
    app.register_blueprint(shift_cipher)
    app.register_blueprint(one_time_pad)
    app.register_blueprint(hash_function)
    app.register_blueprint(des_algorithm)
    app.register_blueprint(aes_algorithm)
    app.register_blueprint(message_auth)
    app.register_blueprint(dsa_algorithm)
    app.register_blueprint(assignments)
    
    # Store error handler in app context for access in routes
    app.error_handler = error_handler
    
    return app

# Create app instance
app = create_app()

# Get error handler from app context
def get_error_handler():
    return getattr(app, 'error_handler', None)

# Routes
@app.route('/')
def home():
    """Landing page that redirects based on user role or shows Firebase login"""
    try:
        if 'user' in session and session.get('user'):
            user_role = session['user'].get('role', 'student')
            if user_role == 'faculty':
                return redirect(url_for('faculty_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        
        # Redirect to Firebase login
        return redirect(url_for('firebase_auth.firebase_login'))
    except Exception as e:
        error_handler = get_error_handler()
        if error_handler:
            error_handler.log_error(e, 'HOME_PAGE_ERROR')
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('firebase_auth.firebase_login'))

@app.route('/student')
@firebase_student_required
def student_dashboard():
    """Student dashboard with access to learning materials and assignments"""
    try:
        user = session['user']
        
        # Get student-specific statistics
        from assignment_manager import assignment_manager
        
        # Get student assignments and statistics
        active_assignments = assignment_manager.get_active_assignments()
        student_submissions = assignment_manager.get_student_submissions(user.get('username', ''))
        
        # Calculate student statistics
        pending_assignments = 0
        completed_assignments = 0
        total_grade = 0
        graded_count = 0
        
        for assignment in active_assignments:
            submission = assignment_manager.get_student_submission(assignment['id'], user.get('username', ''))
            if submission:
                completed_assignments += 1
                if submission.get('grade') is not None:
                    total_grade += submission['grade']
                    graded_count += 1
            else:
                pending_assignments += 1
        
        average_grade = round(total_grade / graded_count) if graded_count > 0 else 0
        progress_percentage = round((completed_assignments / len(active_assignments)) * 100) if active_assignments else 0
        
        stats = {
            'completed_labs': completed_assignments,
            'pending_assignments': pending_assignments,
            'average_grade': average_grade,
            'progress_percentage': progress_percentage
        }
        
        # Get recent assignments for sidebar
        recent_assignments = []
        for assignment in active_assignments[:3]:
            submission = assignment_manager.get_student_submission(assignment['id'], user['username'])
            assignment_data = assignment.copy()
            if submission:
                assignment_data['status'] = submission.get('status', 'submitted')
            else:
                assignment_data['status'] = 'pending'
            recent_assignments.append(assignment_data)
        
        # Get recent grades
        recent_grades = []
        for submission in student_submissions:
            if submission.get('grade') is not None:
                assignment = assignment_manager.get_assignment(submission['assignment_id'])
                if assignment:
                    recent_grades.append({
                        'assignment_title': assignment['title'],
                        'module': assignment['lab_module'],
                        'grade': submission['grade']
                    })
        recent_grades = recent_grades[:3]
        
        # Get lab modules info
        lab_modules = get_lab_modules_info()
        
        return render_template('student_dashboard.html',
                             user=user,
                             user_role='student',
                             stats=stats,
                             recent_assignments=recent_assignments,
                             recent_grades=recent_grades,
                             lab_modules=lab_modules)
    except Exception as e:
        error_handler = get_error_handler()
        if error_handler:
            error_handler.log_error(e, 'STUDENT_DASHBOARD_ERROR')
        flash('An error occurred loading the dashboard. Please try again.', 'error')
        return redirect(url_for('student_login'))

@app.route('/faculty')
@firebase_faculty_required
def faculty_dashboard():
    """Faculty dashboard with administrative features and real-time data"""
    try:
        user = session['user']
        
        # Get real-time dashboard statistics
        stats = get_dashboard_stats()
        recent_activities = get_recent_activities()
        lab_modules = get_lab_modules_info()
        student_list = get_student_list()
        quick_actions = get_quick_actions()
        
        return render_template('faculty_dashboard.html',
                             user=user,
                             user_role='faculty',
                             stats=stats,
                             recent_activities=recent_activities,
                             lab_modules=lab_modules,
                             student_list=student_list,
                             quick_actions=quick_actions)
    except Exception as e:
        error_handler = get_error_handler()
        if error_handler:
            error_handler.log_error(e, 'FACULTY_DASHBOARD_ERROR')
        flash('An error occurred loading the dashboard. Please try again.', 'error')
        return redirect(url_for('firebase_auth.firebase_login'))

@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    """Redirect to Firebase login"""
    return redirect(url_for('firebase_auth.firebase_login'))

@app.route('/faculty-login', methods=['GET', 'POST'])
def faculty_login():
    """Redirect to Firebase login"""
    return redirect(url_for('firebase_auth.firebase_login'))

# Legacy login route - redirect to Firebase login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Legacy login route - redirects to Firebase login"""
    return redirect(url_for('firebase_auth.firebase_login'))

@app.route('/logout')
def logout():
    """Logout route for Firebase authenticated users"""
    error_handler = get_error_handler()
    
    try:
        if 'user' in session and session['user']:
            uid = session['user'].get('uid')
            email = session['user'].get('email', 'Unknown')
            
            # Log logout activity to Firebase
            if uid:
                FirebaseDB.save_activity(uid, 'LOGOUT', {'email': email})
            
            # Log via error handler if available
            if error_handler:
                error_handler.log_auth_event(email, 'LOGOUT', True, f'User logged out')
        
        # Clear session
        session.clear()
        
    except Exception as e:
        if error_handler:
            error_handler.log_error(e, 'LOGOUT_ERROR')
        session.clear()
    
    # Redirect to a logout confirmation page that will sign out Firebase
    return redirect(url_for('logout_page'))

@app.route('/logout-page')
def logout_page():
    """Logout page that signs out Firebase client-side before redirecting to login"""
    return render_template('logout_confirmation.html', firebase_config=FIREBASE_WEB_CONFIG)

if __name__ == '__main__':
    app.run(debug=True)
