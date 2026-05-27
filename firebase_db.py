"""
Firebase Realtime Database Operations
Handles all user data synchronization with Firebase
"""

from firebase_config import get_firebase_ref, db
from datetime import datetime
import json

class FirebaseDB:
    """Handles Firebase Realtime Database operations"""
    
    # Database paths
    USERS_PATH = 'users'
    ASSIGNMENTS_PATH = 'assignments'
    SUBMISSIONS_PATH = 'submissions'
    ACTIVITIES_PATH = 'activities'
    
    @staticmethod
    def save_user(uid, user_data):
        """
        Save user to Firebase Database
        
        Args:
            uid: Firebase UID
            user_data: Dictionary containing user information
        """
        try:
            ref = get_firebase_ref(f'{FirebaseDB.USERS_PATH}/{uid}')
            user_data['last_updated'] = datetime.now().isoformat()
            user_data['created_at'] = user_data.get('created_at', datetime.now().isoformat())
            ref.set(user_data)
            return True
        except Exception as e:
            print(f"Error saving user: {str(e)}")
            return False
    
    @staticmethod
    def get_user(uid):
        """
        Retrieve user from Firebase
        
        Args:
            uid: Firebase UID
            
        Returns:
            dict: User data or None
        """
        try:
            ref = get_firebase_ref(f'{FirebaseDB.USERS_PATH}/{uid}')
            if not ref:
                return None

            data = ref.get()
            return data if data else None
        except Exception as e:
            print(f"Error fetching user: {str(e)}")
            return None

    @staticmethod
    def get_all_users():
        """Retrieve all users from Firebase"""
        try:
            ref = get_firebase_ref(FirebaseDB.USERS_PATH)
            if not ref:
                return []

            data = ref.get()
            if not data:
                return []

            if isinstance(data, dict):
                return list(data.values())
            if isinstance(data, list):
                return data
            return []
        except Exception as e:
            print(f"Error fetching users: {str(e)}")
            return []
    
    @staticmethod
    def update_user(uid, updates):
        """
        Update user data
        
        Args:
            uid: Firebase UID
            updates: Dictionary with updates
        """
        try:
            ref = get_firebase_ref(f'{FirebaseDB.USERS_PATH}/{uid}')
            updates['last_updated'] = datetime.now().isoformat()
            ref.update(updates)
            return True
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return False
    
    @staticmethod
    def save_assignment(assignment_id, assignment_data, faculty_uid):
        """
        Save assignment to database
        
        Args:
            assignment_id: Assignment ID
            assignment_data: Assignment details
            faculty_uid: Faculty UID who created it
        """
        try:
            ref = get_firebase_ref(f'{FirebaseDB.ASSIGNMENTS_PATH}/{assignment_id}')
            assignment_data['created_by'] = faculty_uid
            assignment_data['created_at'] = datetime.now().isoformat()
            ref.set(assignment_data)
            return True
        except Exception as e:
            print(f"Error saving assignment: {str(e)}")
            return False
    
    @staticmethod
    def get_user_assignments(uid):
        """Get all assignments for a user"""
        try:
            ref = get_firebase_ref(FirebaseDB.ASSIGNMENTS_PATH)
            if not ref:
                return []

            assignments = ref.get()
            if not assignments:
                return []

            if isinstance(assignments, dict):
                return list(assignments.values())
            if isinstance(assignments, list):
                return assignments
            return []
        except Exception as e:
            print(f"Error fetching assignments: {str(e)}")
            return []
    
    @staticmethod
    def save_submission(submission_id, submission_data, student_uid):
        """
        Save student submission
        
        Args:
            submission_id: Submission ID
            submission_data: Submission details
            student_uid: Student UID
        """
        try:
            ref = get_firebase_ref(f'{FirebaseDB.SUBMISSIONS_PATH}/{submission_id}')
            submission_data['student_uid'] = student_uid
            submission_data['submitted_at'] = datetime.now().isoformat()
            ref.set(submission_data)
            return True
        except Exception as e:
            print(f"Error saving submission: {str(e)}")
            return False
    
    @staticmethod
    def get_student_submissions(student_uid):
        """Get all submissions by a student"""
        try:
            ref = get_firebase_ref(FirebaseDB.SUBMISSIONS_PATH)
            if not ref:
                return []

            submissions = ref.get()
            if not submissions:
                return []

            if isinstance(submissions, dict):
                values = submissions.values()
            elif isinstance(submissions, list):
                values = submissions
            else:
                return []

            return [
                sub for sub in values
                if sub.get('student_uid') == student_uid
            ]
        except Exception as e:
            print(f"Error fetching submissions: {str(e)}")
            return []
    
    @staticmethod
    def grade_submission(submission_id, grade, feedback, faculty_uid):
        """
        Grade a student submission
        
        Args:
            submission_id: Submission ID
            grade: Grade/score
            feedback: Teacher feedback
            faculty_uid: Faculty UID
        """
        try:
            ref = get_firebase_ref(f'{FirebaseDB.SUBMISSIONS_PATH}/{submission_id}')
            ref.update({
                'grade': grade,
                'feedback': feedback,
                'graded_by': faculty_uid,
                'graded_at': datetime.now().isoformat(),
                'status': 'graded'
            })
            return True
        except Exception as e:
            print(f"Error grading submission: {str(e)}")
            return False
    
    @staticmethod
    def save_activity(uid, activity_type, activity_data):
        """
        Log user activity
        
        Args:
            uid: User UID
            activity_type: Type of activity
            activity_data: Activity details
        """
        try:
            activity_id = db.reference(f'{FirebaseDB.ACTIVITIES_PATH}/{uid}').push().key
            ref = get_firebase_ref(f'{FirebaseDB.ACTIVITIES_PATH}/{uid}/{activity_id}')
            
            activity = {
                'type': activity_type,
                'timestamp': datetime.now().isoformat(),
                **activity_data
            }
            ref.set(activity)
            return True
        except Exception as e:
            print(f"Error saving activity: {str(e)}")
            return False
    
    @staticmethod
    def get_user_statistics(uid):
        """
        Get user statistics from database
        
        Args:
            uid: User UID
            
        Returns:
            dict: User statistics
        """
        try:
            ref = get_firebase_ref(f'{FirebaseDB.USERS_PATH}/{uid}')
            if not ref:
                return {}

            user = ref.get()
            if not user:
                return {}
            
            submissions = FirebaseDB.get_student_submissions(uid)
            
            stats = {
                'total_assignments_submitted': len(submissions),
                'assignments_graded': len([s for s in submissions if s.get('status') == 'graded']),
                'average_grade': 0,
                'last_activity': user.get('last_updated')
            }
            
            graded_submissions = [s for s in submissions if s.get('grade') is not None]
            if graded_submissions:
                total_grade = sum([s.get('grade', 0) for s in graded_submissions])
                stats['average_grade'] = round(total_grade / len(graded_submissions), 2)
            
            return stats
        except Exception as e:
            print(f"Error fetching statistics: {str(e)}")
            return {}
