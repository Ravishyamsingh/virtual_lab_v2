"""
Assignment routes for faculty and student assignment management
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from auth import faculty_required, student_required, get_user_by_username
from assignment_manager import assignment_manager
from utils.validators import InputValidator
from utils.error_handlers import create_error_response
from datetime import datetime

assignments = Blueprint('assignments', __name__)

# Faculty Assignment Routes
@assignments.route('/faculty/assignments')
@faculty_required
def faculty_assignments():
    """Faculty assignment management page"""
    try:
        user = get_user_by_username(session['user']['username'])
        assignments_list = assignment_manager.get_assignments_by_faculty(user['username'])
        stats = assignment_manager.get_assignment_statistics()
        
        return render_template('assignments/faculty_assignments.html', 
                             assignments=assignments_list,
                             stats=stats,
                             user=user)
    except Exception as e:
        flash('Error loading assignments', 'error')
        return redirect(url_for('faculty_dashboard'))

@assignments.route('/faculty/assignments/create', methods=['GET', 'POST'])
@faculty_required
def create_assignment():
    """Create new assignment"""
    if request.method == 'POST':
        try:
            user = get_user_by_username(session['user']['username'])
            
            # Get form data
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            lab_module = request.form.get('lab_module', '').strip()
            difficulty = request.form.get('difficulty', '').strip()
            points = int(request.form.get('points', 0))
            due_days = int(request.form.get('due_days', 7))
            instructions = request.form.get('instructions', '').strip()
            resources = request.form.get('resources', '').strip().split('\n')
            resources = [r.strip() for r in resources if r.strip()]
            
            # Validate inputs
            if not all([title, description, lab_module, difficulty]):
                flash('All required fields must be filled', 'error')
                return render_template('assignments/create_assignment.html')
            
            if points < 1 or points > 100:
                flash('Points must be between 1 and 100', 'error')
                return render_template('assignments/create_assignment.html')
            
            if due_days < 1 or due_days > 365:
                flash('Due days must be between 1 and 365', 'error')
                return render_template('assignments/create_assignment.html')
            
            # Sanitize inputs
            title = InputValidator.sanitize_input(title)
            description = InputValidator.sanitize_input(description)
            instructions = InputValidator.sanitize_input(instructions)
            
            # Create assignment
            assignment_id = assignment_manager.create_assignment(
                title=title,
                description=description,
                lab_module=lab_module,
                difficulty=difficulty,
                points=points,
                due_days=due_days,
                created_by=user['username'],
                instructions=instructions,
                resources=resources
            )
            
            flash(f'Assignment "{title}" created successfully!', 'success')
            return redirect(url_for('assignments.faculty_assignments'))
            
        except ValueError as e:
            flash(str(e), 'error')
            return render_template('assignments/create_assignment.html')
        except Exception as e:
            flash('Error creating assignment', 'error')
            return render_template('assignments/create_assignment.html')
    
    # GET request - show form
    lab_modules = [
        {'value': 'mono_alphabetic', 'name': 'Mono Alphabetic Cipher'},
        {'value': 'shift_cipher', 'name': 'Shift Cipher'},
        {'value': 'one_time_pad', 'name': 'One Time Pad'},
        {'value': 'aes_algorithm', 'name': 'AES Algorithm'},
        {'value': 'des_algorithm', 'name': 'DES Algorithm'},
        {'value': 'hash_function', 'name': 'Hash Functions'},
        {'value': 'message_auth', 'name': 'Message Authentication'},
        {'value': 'dsa_algorithm', 'name': 'DSA Algorithm'}
    ]
    
    return render_template('assignments/create_assignment.html', lab_modules=lab_modules)

@assignments.route('/faculty/assignments/<assignment_id>')
@faculty_required
def faculty_view_assignment(assignment_id):
    """View assignment details and submissions"""
    try:
        user = get_user_by_username(session['user']['username'])
        assignment = assignment_manager.get_assignment(assignment_id)
        if not assignment:
            flash('Assignment not found', 'error')
            return redirect(url_for('assignments.faculty_assignments'))
        
        submissions = assignment_manager.get_submissions_for_assignment(assignment_id)
        
        return render_template('assignments/view_assignment.html',
                             assignment=assignment,
                             submissions=submissions,
                             user=user)
    except Exception as e:
        flash('Error loading assignment', 'error')
        return redirect(url_for('assignments.faculty_assignments'))

@assignments.route('/faculty/assignments/<assignment_id>/grade/<submission_id>', methods=['GET', 'POST'])
@faculty_required
def grade_submission(assignment_id, submission_id):
    """Grade a student submission"""
    try:
        user = get_user_by_username(session['user']['username'])
        assignment = assignment_manager.get_assignment(assignment_id)
        submission = assignment_manager.get_submission(submission_id)
        
        if not assignment or not submission:
            flash('Assignment or submission not found', 'error')
            return redirect(url_for('assignments.faculty_assignments'))
        
        if request.method == 'POST':
            grade = int(request.form.get('grade', 0))
            feedback = request.form.get('feedback', '').strip()
            
            if grade < 0 or grade > 100:
                flash('Grade must be between 0 and 100', 'error')
                return render_template('assignments/grade_submission.html',
                                     assignment=assignment,
                                     submission=submission,
                                     user=user)
            
            success = assignment_manager.grade_submission(
                submission_id=submission_id,
                grade=grade,
                feedback=InputValidator.sanitize_input(feedback),
                graded_by=user['username']
            )
            
            if success:
                flash('Submission graded successfully!', 'success')
                return redirect(url_for('assignments.view_submission',
                                      assignment_id=assignment_id,
                                      submission_id=submission_id))
            else:
                flash('Error grading submission', 'error')
        
        return render_template('assignments/grade_submission.html',
                             assignment=assignment,
                             submission=submission,
                             user=user)
        
    except Exception as e:
        flash('Error grading submission', 'error')
        return redirect(url_for('assignments.faculty_assignments'))

# Student Assignment Routes
@assignments.route('/student/assignments')
@student_required
def student_assignments():
    """Student assignments page"""
    try:
        user = get_user_by_username(session['user']['username'])
        if not user:
            flash('User session invalid', 'error')
            return redirect(url_for('student_dashboard'))
            
        print(f"Loading assignments for user: {user['username']}")  # Debug
        
        active_assignments = assignment_manager.get_active_assignments()
        print(f"Found {len(active_assignments)} active assignments")  # Debug
        
        student_submissions = assignment_manager.get_student_submissions(user['username'])
        print(f"Found {len(student_submissions)} student submissions")  # Debug
        
        # Add submission status to assignments
        for assignment in active_assignments:
            submission = assignment_manager.get_student_submission(
                assignment['id'], user['username']
            )
            assignment['submission'] = submission
            
            # Handle datetime parsing safely
            try:
                due_date = datetime.fromisoformat(assignment['due_date'].replace('Z', '+00:00'))
                assignment['is_overdue'] = datetime.now() > due_date
            except (ValueError, KeyError):
                assignment['is_overdue'] = False
            
            # Set assignment status for student view
            if submission:
                if submission.get('grade') is not None:
                    assignment['status'] = 'graded'
                else:
                    assignment['status'] = 'submitted'
            else:
                assignment['status'] = 'pending'
        
        print("Rendering student assignments template")  # Debug
        return render_template('assignments/student_assignments.html',
                             assignments=active_assignments,
                             submissions=student_submissions,
                             user=user)
    except Exception as e:
        print(f"Error in student_assignments: {e}")  # Debug print
        import traceback
        traceback.print_exc()  # Print full traceback
        flash('Error loading assignments', 'error')
        return redirect(url_for('student_dashboard'))

@assignments.route('/assignments/<assignment_id>')
@student_required
def student_view_assignment(assignment_id):
    """View assignment details for student"""
    try:
        user = get_user_by_username(session['user']['username'])
        print(f"DEBUG: Viewing assignment {assignment_id} for user {user['username']}")

        assignment = assignment_manager.get_assignment(assignment_id)
        print(f"DEBUG: Assignment found: {assignment is not None}")

        if not assignment:
            print(f"DEBUG: Assignment {assignment_id} not found")
            flash('Assignment not found', 'error')
            return redirect(url_for('assignments.student_assignments'))

        if not assignment['is_active']:
            print(f"DEBUG: Assignment {assignment_id} is not active")
            flash('Assignment not found', 'error')
            return redirect(url_for('assignments.student_assignments'))

        submission = assignment_manager.get_student_submission(assignment_id, user['username'])
        is_overdue = datetime.now() > datetime.fromisoformat(assignment['due_date'])

        print(f"DEBUG: Rendering view_assignment template for assignment: {assignment['title']}")
        return render_template('assignments/view_assignment.html',
                              assignment=assignment,
                              submission=submission,
                              is_overdue=is_overdue,
                              user=user)
    except Exception as e:
        print(f"DEBUG: Error in student_view_assignment: {e}")
        import traceback
        traceback.print_exc()
        flash('Error loading assignment', 'error')
        return redirect(url_for('assignments.student_assignments'))

@assignments.route('/assignments/<assignment_id>/submit', methods=['GET', 'POST'])
@student_required
def submit_assignment(assignment_id):
    """Submit assignment"""
    try:
        user = get_user_by_username(session['user']['username'])
        assignment = assignment_manager.get_assignment(assignment_id)
        
        if not assignment or not assignment['is_active']:
            flash('Assignment not found', 'error')
            return redirect(url_for('assignments.student_assignments'))
        
        # Check if already submitted
        existing_submission = assignment_manager.get_student_submission(assignment_id, user['username'])
        
        if request.method == 'POST':
            solution_text = request.form.get('solution_text', '').strip()
            
            if not solution_text:
                flash('Solution text is required', 'error')
                return render_template('assignments/submit_assignment.html',
                                     assignment=assignment,
                                     submission=existing_submission,
                                     user=user)
            
            # Sanitize content
            solution_text = InputValidator.sanitize_input(solution_text)
            
            submission_id = assignment_manager.submit_assignment(
                assignment_id=assignment_id,
                student_username=user['username'],
                solution_text=solution_text
            )
            
            flash('Assignment submitted successfully!', 'success')
            return redirect(f'/assignments/{assignment_id}/submission/{submission_id}')
        
        return render_template('assignments/submit_assignment.html',
                             assignment=assignment,
                             submission=existing_submission,
                             user=user)
        
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(f'/assignments/{assignment_id}')
    except Exception as e:
        flash('Error submitting assignment', 'error')
        return redirect(f'/assignments/{assignment_id}')

@assignments.route('/assignments/<assignment_id>/submission/<submission_id>')
@student_required
def view_submission(assignment_id, submission_id):
    """View assignment submission"""
    try:
        user = get_user_by_username(session['user']['username'])
        assignment = assignment_manager.get_assignment(assignment_id)
        submission = assignment_manager.get_submission(submission_id)
        
        if not assignment or not submission:
            flash('Assignment or submission not found', 'error')
            if user['role'] == 'faculty':
                return redirect(url_for('assignments.faculty_assignments'))
            else:
                return redirect(url_for('assignments.student_assignments'))
        
        # Check if user has permission to view this submission
        if user['role'] == 'student' and submission['student_username'] != user['username']:
            flash('You do not have permission to view this submission', 'error')
            return redirect(url_for('assignments.student_assignments'))
        
        return render_template('assignments/view_submission.html',
                             assignment=assignment,
                             submission=submission,
                             user=user)
    except Exception as e:
        flash('Error loading submission', 'error')
        if user['role'] == 'faculty':
            return redirect(url_for('assignments.faculty_assignments'))
        else:
            return redirect(url_for('assignments.student_assignments'))

# API Routes for Quick Actions
@assignments.route('/api/assignments/stats')
@faculty_required
def assignment_stats_api():
    """Get assignment statistics for dashboard"""
    try:
        stats = assignment_manager.get_assignment_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': 'Failed to load statistics'}), 500

@assignments.route('/api/assignments/recent')
@faculty_required
def recent_assignments_api():
    """Get recent assignments"""
    try:
        user = get_user_by_username(session['user']['username'])
        assignments_list = assignment_manager.get_assignments_by_faculty(user['username'])
        recent = sorted(assignments_list, key=lambda x: x['created_at'], reverse=True)[:5]
        return jsonify(recent)
    except Exception as e:
        return jsonify({'error': 'Failed to load assignments'}), 500

@assignments.route('/api/assignments/quick-create', methods=['POST'])
@faculty_required
def quick_create_assignment():
    """Quick create assignment API"""
    try:
        user = get_user_by_username(session['user']['username'])
        data = request.get_json()
        
        assignment_id = assignment_manager.create_assignment(
            title=data.get('title', 'Quick Assignment'),
            description=data.get('description', 'Assignment created via quick action'),
            lab_module=data.get('lab_module', 'shift_cipher'),
            difficulty='easy',
            points=10,
            due_days=7,
            created_by=user['username'],
            instructions=data.get('instructions', 'Complete the assignment as instructed.'),
            resources=[]
        )
        
        return jsonify({'success': True, 'assignment_id': assignment_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@assignments.route('/assignments/delete/<assignment_id>', methods=['DELETE'])
@faculty_required
def delete_assignment(assignment_id):
    """Delete an assignment"""
    try:
        success = assignment_manager.delete_assignment(assignment_id)
        if success:
            return jsonify({'success': True, 'message': 'Assignment deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete assignment'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@assignments.route('/api/faculty/submissions/recent')
@faculty_required
def get_recent_submissions():
    """Get recent submissions for faculty dashboard"""
    try:
        user = get_user_by_username(session['user']['username'])
        
        # Get all active assignments (faculty can grade any assignment)
        all_active_assignments = assignment_manager.get_active_assignments()
        active_assignment_ids = [a['id'] for a in all_active_assignments]
        
        # Get all submissions for active assignments
        all_submissions = assignment_manager.load_submissions()
        faculty_submissions = [
            s for s in all_submissions 
            if s['assignment_id'] in active_assignment_ids
        ]
        
        # Enrich submissions with assignment data and student info
        enriched_submissions = []
        for submission in faculty_submissions:
            # Get assignment details
            assignment = assignment_manager.get_assignment(submission['assignment_id'])
            if not assignment:
                continue
                
            # Get student details
            student = get_user_by_username(submission['student_username'])
            if not student:
                continue
            
            enriched_submission = {
                'id': submission['id'],
                'assignment_id': submission['assignment_id'],
                'student_username': submission['student_username'],
                'student_name': student['full_name'],
                'submitted_at': submission['submitted_at'],
                'status': submission['status'],
                'grade': submission.get('grade'),
                'feedback': submission.get('feedback'),
                'assignment': {
                    'title': assignment['title'],
                    'lab_module': assignment['lab_module'],
                    'points': assignment['points'],
                    'difficulty': assignment['difficulty']
                }
            }
            enriched_submissions.append(enriched_submission)
        
        # Sort by submission date (most recent first) and limit to 10
        enriched_submissions.sort(key=lambda x: x['submitted_at'], reverse=True)
        recent_submissions = enriched_submissions[:10]
        
        return jsonify(recent_submissions)
        
    except Exception as e:
        print(f"Error fetching recent submissions: {e}")  # Debug
        return jsonify({'error': 'Failed to load submissions'}), 500

@assignments.route('/api/submissions/<submission_id>/grade', methods=['POST'])
@faculty_required  
def api_grade_submission(submission_id):
    """API endpoint for quick grading"""
    try:
        user = get_user_by_username(session['user']['username'])
        data = request.get_json()
        
        grade = int(data.get('grade', 0))
        feedback = data.get('feedback', '')
        
        if grade < 0 or grade > 100:
            return jsonify({'error': 'Grade must be between 0 and 100'}), 400
            
        # Sanitize feedback
        feedback = InputValidator.sanitize_input(feedback)
        
        success = assignment_manager.grade_submission(
            submission_id=submission_id,
            grade=grade,
            feedback=feedback,
            graded_by=user['username']
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Grade submitted successfully'})
        else:
            return jsonify({'error': 'Failed to grade submission'}), 400
            
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred while grading'}), 500

@assignments.route('/api/submissions/bulk-grade', methods=['POST'])
@faculty_required
def api_bulk_grade():
    """API endpoint for bulk grading"""
    try:
        user = get_user_by_username(session['user']['username'])
        data = request.get_json()
        
        submission_ids = data.get('submission_ids', [])
        grade = int(data.get('grade', 0))
        feedback = data.get('feedback', '')
        
        if not submission_ids:
            return jsonify({'error': 'No submissions selected'}), 400
            
        if grade < 0 or grade > 100:
            return jsonify({'error': 'Grade must be between 0 and 100'}), 400
        
        # Sanitize feedback
        feedback = InputValidator.sanitize_input(feedback)
        
        # Grade each submission
        success_count = 0
        for submission_id in submission_ids:
            success = assignment_manager.grade_submission(
                submission_id=submission_id,
                grade=grade,
                feedback=feedback,
                graded_by=user['username']
            )
            if success:
                success_count += 1
        
        return jsonify({
            'success': True, 
            'message': f'Successfully graded {success_count}/{len(submission_ids)} submissions'
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during bulk grading'}), 500

@assignments.route('/api/submissions/bulk-approve', methods=['POST'])
@faculty_required
def api_bulk_approve():
    """API endpoint for bulk approval"""
    try:
        user = get_user_by_username(session['user']['username'])
        data = request.get_json()
        
        submission_ids = data.get('submission_ids', [])
        
        if not submission_ids:
            return jsonify({'error': 'No submissions selected'}), 400
        
        # Update status for each submission
        submissions = assignment_manager.load_submissions()
        success_count = 0
        
        for i, submission in enumerate(submissions):
            if submission['id'] in submission_ids:
                submissions[i]['status'] = 'approved'
                submissions[i]['approved_by'] = user['username']
                submissions[i]['approved_at'] = datetime.now().isoformat()
                success_count += 1
        
        # Save updated submissions
        assignment_manager.save_submissions(submissions)
        
        return jsonify({
            'success': True,
            'message': f'Successfully approved {success_count} submissions'
        })
        
    except Exception as e:
        return jsonify({'error': 'An error occurred during bulk approval'}), 500

@assignments.route('/api/submissions/export', methods=['POST'])
@faculty_required
def api_export_submissions():
    """API endpoint for exporting submissions"""
    try:
        user = get_user_by_username(session['user']['username'])
        data = request.get_json()
        
        submission_ids = data.get('submission_ids', [])
        
        if not submission_ids:
            return jsonify({'error': 'No submissions selected'}), 400
        
        # Get submissions data for export
        all_submissions = assignment_manager.load_submissions()
        export_data = []
        
        for submission in all_submissions:
            if submission['id'] in submission_ids:
                # Get assignment and student details
                assignment = assignment_manager.get_assignment(submission['assignment_id'])
                student = get_user_by_username(submission['student_username'])
                
                if assignment and student:
                    export_data.append({
                        'submission_id': submission['id'],
                        'assignment_title': assignment['title'],
                        'student_name': student['full_name'],
                        'student_username': student['username'],
                        'submitted_at': submission['submitted_at'],
                        'status': submission['status'],
                        'grade': submission.get('grade', 'Not graded'),
                        'feedback': submission.get('feedback', ''),
                        'lab_module': assignment['lab_module'],
                        'points': assignment['points']
                    })
        
        return jsonify({
            'success': True,
            'data': export_data,
            'count': len(export_data),
            'message': f'Exported {len(export_data)} submissions'
        })
        
    except Exception as e:
        return jsonify({'error': 'An error occurred during export'}), 500
