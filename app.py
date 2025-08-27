from flask import Flask, render_template, redirect, url_for, session, request, flash
from config import get_config, FeatureFlags
from auth import check_credentials, login_required, load_users, faculty_required, student_required, get_user_by_username
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
import os

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    config_class.init_app(app)
    
    # Initialize error handling
    error_handler = ErrorHandler(app)
    
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
    """Landing page that redirects based on user role or shows login options"""
    try:
        if 'user' in session and session['user']:
            user = get_user_by_username(session['user']['username'])
            if user:
                if user['role'] == 'faculty':
                    return redirect(url_for('faculty_dashboard'))
                else:
                    return redirect(url_for('student_dashboard'))
        
        # Show login selection page
        return render_template('login_selection.html')
    except Exception as e:
        error_handler = get_error_handler()
        if error_handler:
            error_handler.log_error(e, 'HOME_PAGE_ERROR')
        flash('An error occurred. Please try again.', 'error')
        return render_template('login_selection.html')

@app.route('/student')
@student_required
def student_dashboard():
    """Student dashboard with access to learning materials and assignments"""
    try:
        user = get_user_by_username(session['user']['username'])
        if not user:
            flash('User session invalid. Please log in again.', 'error')
            return redirect(url_for('student_login'))
        
        # Get student-specific statistics
        from assignment_manager import assignment_manager
        
        # Get student assignments and statistics
        active_assignments = assignment_manager.get_active_assignments()
        student_submissions = assignment_manager.get_student_submissions(user['username'])
        
        # Calculate student statistics
        pending_assignments = 0
        completed_assignments = 0
        total_grade = 0
        graded_count = 0
        
        for assignment in active_assignments:
            submission = assignment_manager.get_student_submission(assignment['id'], user['username'])
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
@faculty_required
def faculty_dashboard():
    """Faculty dashboard with administrative features and real-time data"""
    try:
        user = get_user_by_username(session['user']['username'])
        if not user:
            flash('User session invalid. Please log in again.', 'error')
            return redirect(url_for('faculty_login'))
        
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
        return redirect(url_for('faculty_login'))

@app.route('/student-login', methods=['GET', 'POST'])
@validate_login_data
def student_login():
    """Student login route with enhanced validation and security"""
    error_handler = get_error_handler()
    
    # Clear any existing session
    if 'user' in session:
        session.pop('user', None)
    
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            # Additional validation
            is_valid, error_msg = InputValidator.validate_username(username)
            if not is_valid:
                if error_handler:
                    error_handler.log_auth_event(username, 'STUDENT_LOGIN_INVALID_USERNAME', False, error_msg)
                flash(error_msg, 'error')
                return render_template('login.html', error=error_msg)
            
            if not password:
                if error_handler:
                    error_handler.log_auth_event(username, 'STUDENT_LOGIN_NO_PASSWORD', False, 'Password not provided')
                flash('Password is required', 'error')
                return render_template('login.html', error='Password is required')
            
            # Sanitize username
            username = InputValidator.sanitize_input(username)
            
            user = check_credentials(username, password)
            if user and user['role'] == 'student':
                session['user'] = {
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'role': user['role']
                }
                session.permanent = True
                
                if error_handler:
                    error_handler.log_auth_event(username, 'STUDENT_LOGIN_SUCCESS', True, f'Student {user["full_name"]} logged in')
                flash(f'Welcome back, {user["full_name"]}!', 'success')
                return redirect(url_for('student_dashboard'))
            elif user and user['role'] != 'student':
                if error_handler:
                    error_handler.log_auth_event(username, 'STUDENT_LOGIN_WRONG_ROLE', False, f'User has role: {user["role"]}')
                flash('Please use the faculty login for instructor access.', 'error')
                return render_template('login.html', error='Please use the faculty login for instructor access.')
            else:
                if error_handler:
                    error_handler.log_auth_event(username, 'STUDENT_LOGIN_INVALID_CREDENTIALS', False, 'Invalid credentials provided')
                flash('Invalid username or password.', 'error')
                return render_template('login.html', error='Invalid username or password')
                
        except Exception as e:
            if error_handler:
                error_handler.log_error(e, 'STUDENT_LOGIN_EXCEPTION')
            flash('An error occurred. Please try again.', 'error')
            return render_template('login.html', error='An error occurred. Please try again.')
    
    return render_template('login.html')

@app.route('/faculty-login', methods=['GET', 'POST'])
@validate_login_data
def faculty_login():
    """Faculty login route with enhanced validation and security"""
    error_handler = get_error_handler()
    
    # Clear any existing session
    if 'user' in session:
        session.pop('user', None)
    
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            # Additional validation
            is_valid, error_msg = InputValidator.validate_username(username)
            if not is_valid:
                if error_handler:
                    error_handler.log_auth_event(username, 'FACULTY_LOGIN_INVALID_USERNAME', False, error_msg)
                flash(error_msg, 'error')
                return render_template('faculty_login.html', error=error_msg)
            
            if not password:
                if error_handler:
                    error_handler.log_auth_event(username, 'FACULTY_LOGIN_NO_PASSWORD', False, 'Password not provided')
                flash('Password is required', 'error')
                return render_template('faculty_login.html', error='Password is required')
            
            # Sanitize username
            username = InputValidator.sanitize_input(username)
            
            user = check_credentials(username, password)
            if user and user['role'] == 'faculty':
                session['user'] = {
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user['full_name'],
                    'role': user['role']
                }
                session.permanent = True
                
                if error_handler:
                    error_handler.log_auth_event(username, 'FACULTY_LOGIN_SUCCESS', True, f'Faculty {user["full_name"]} logged in')
                flash(f'Welcome back, {user["full_name"]}!', 'success')
                return redirect(url_for('faculty_dashboard'))
            elif user and user['role'] != 'faculty':
                if error_handler:
                    error_handler.log_auth_event(username, 'FACULTY_LOGIN_WRONG_ROLE', False, f'User has role: {user["role"]}')
                flash('Please use the student login for learner access.', 'error')
                return render_template('faculty_login.html', error='Please use the student login for learner access.')
            else:
                if error_handler:
                    error_handler.log_auth_event(username, 'FACULTY_LOGIN_INVALID_CREDENTIALS', False, 'Invalid credentials provided')
                flash('Invalid username or password.', 'error')
                return render_template('faculty_login.html', error='Invalid username or password')
                
        except Exception as e:
            if error_handler:
                error_handler.log_error(e, 'FACULTY_LOGIN_EXCEPTION')
            flash('An error occurred. Please try again.', 'error')
            return render_template('faculty_login.html', error='An error occurred. Please try again.')
    
    return render_template('faculty_login.html')

# Legacy login route - redirect to student login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Legacy login route - redirects to student login"""
    return redirect(url_for('student_login'))

@app.route('/logout')
def logout():
    """Logout route for both faculty and students with audit logging"""
    error_handler = get_error_handler()
    user_role = None
    username = None
    
    try:
        if 'user' in session and session['user']:
            username = session['user'].get('username', 'Unknown')
            user = get_user_by_username(username)
            if user:
                user_role = user['role']
        
        # Log logout event
        if username and error_handler:
            error_handler.log_auth_event(username, 'LOGOUT', True, f'User logged out from {user_role} role')
        
        # Clear session
        session.clear()
        flash('You have been logged out successfully.', 'info')
        
        # Redirect to appropriate login page
        if user_role == 'faculty':
            return redirect(url_for('faculty_login'))
        else:
            return redirect(url_for('student_login'))
            
    except Exception as e:
        if error_handler:
            error_handler.log_error(e, 'LOGOUT_ERROR')
        session.clear()  # Clear session anyway for security
        flash('Logged out successfully.', 'info')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
