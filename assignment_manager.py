"""
Assignment Management System for Cryptography Virtual Lab
Handles creation, management, and tracking of student assignments.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import uuid

@dataclass
class Assignment:
    """Assignment data structure"""
    id: str
    title: str
    description: str
    lab_module: str
    difficulty: str  # 'easy', 'medium', 'hard'
    points: int
    due_date: str
    created_by: str
    created_at: str
    instructions: str
    resources: List[str]
    is_active: bool = True

@dataclass
class StudentSubmission:
    """Student submission data structure"""
    id: str
    assignment_id: str
    student_username: str
    submitted_at: str
    content: str
    files: List[str]
    status: str  # 'submitted', 'graded', 'late'
    grade: Optional[int] = None
    feedback: Optional[str] = None
    graded_by: Optional[str] = None
    graded_at: Optional[str] = None

class AssignmentManager:
    """Manages assignments and submissions"""
    
    def __init__(self):
        self.assignments_file = 'data/assignments.json'
        self.submissions_file = 'data/submissions.json'
        self._ensure_data_files()
    
    def _ensure_data_files(self):
        """Ensure assignment data files exist"""
        os.makedirs('data', exist_ok=True)
        
        if not os.path.exists(self.assignments_file):
            with open(self.assignments_file, 'w') as f:
                json.dump({'assignments': []}, f, indent=2)
        
        if not os.path.exists(self.submissions_file):
            with open(self.submissions_file, 'w') as f:
                json.dump({'submissions': []}, f, indent=2)
    
    def load_assignments(self) -> List[Dict[str, Any]]:
        """Load all assignments"""
        try:
            with open(self.assignments_file, 'r') as f:
                data = json.load(f)
                return data.get('assignments', [])
        except Exception:
            return []
    
    def save_assignments(self, assignments: List[Dict[str, Any]]):
        """Save assignments to file"""
        try:
            with open(self.assignments_file, 'w') as f:
                json.dump({'assignments': assignments}, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save assignments: {str(e)}")
    
    def load_submissions(self) -> List[Dict[str, Any]]:
        """Load all submissions"""
        try:
            with open(self.submissions_file, 'r') as f:
                data = json.load(f)
                return data.get('submissions', [])
        except Exception:
            return []
    
    def save_submissions(self, submissions: List[Dict[str, Any]]):
        """Save submissions to file"""
        try:
            with open(self.submissions_file, 'w') as f:
                json.dump({'submissions': submissions}, f, indent=2)
        except Exception as e:
            raise Exception(f"Failed to save submissions: {str(e)}")
    
    def create_assignment(self, title: str, description: str, lab_module: str, 
                         difficulty: str, points: int, due_days: int, 
                         created_by: str, instructions: str, 
                         resources: List[str] = None) -> str:
        """Create a new assignment"""
        assignment_id = str(uuid.uuid4())
        due_date = (datetime.now() + timedelta(days=due_days)).isoformat()
        
        assignment = Assignment(
            id=assignment_id,
            title=title,
            description=description,
            lab_module=lab_module,
            difficulty=difficulty,
            points=points,
            due_date=due_date,
            created_by=created_by,
            created_at=datetime.now().isoformat(),
            instructions=instructions,
            resources=resources or [],
            is_active=True
        )
        
        assignments = self.load_assignments()
        assignments.append(asdict(assignment))
        self.save_assignments(assignments)
        
        return assignment_id
    
    def get_assignment(self, assignment_id: str) -> Optional[Dict[str, Any]]:
        """Get assignment by ID"""
        assignments = self.load_assignments()
        for assignment in assignments:
            if assignment['id'] == assignment_id:
                return assignment
        return None
    
    def get_assignments_by_module(self, lab_module: str) -> List[Dict[str, Any]]:
        """Get assignments for a specific lab module"""
        assignments = self.load_assignments()
        return [a for a in assignments if a['lab_module'] == lab_module and a['is_active']]
    
    def get_active_assignments(self) -> List[Dict[str, Any]]:
        """Get all active assignments"""
        assignments = self.load_assignments()
        return [a for a in assignments if a['is_active']]
    
    def get_assignments_by_faculty(self, faculty_username: str) -> List[Dict[str, Any]]:
        """Get assignments created by a faculty member"""
        assignments = self.load_assignments()
        return [a for a in assignments if a['created_by'] == faculty_username]
    
    def update_assignment(self, assignment_id: str, updates: Dict[str, Any]) -> bool:
        """Update an assignment"""
        assignments = self.load_assignments()
        for i, assignment in enumerate(assignments):
            if assignment['id'] == assignment_id:
                assignments[i].update(updates)
                self.save_assignments(assignments)
                return True
        return False
    
    def deactivate_assignment(self, assignment_id: str) -> bool:
        """Deactivate an assignment"""
        return self.update_assignment(assignment_id, {'is_active': False})
    
    def submit_assignment(self, assignment_id: str, student_username: str,
                         solution_text: str = None, content: str = None, files: List[str] = None) -> str:
        """Submit an assignment"""
        submission_id = str(uuid.uuid4())
        
        # Handle both solution_text and content parameters for backward compatibility
        submission_content = solution_text or content or ""
        
        # Check if assignment exists and is active
        assignment = self.get_assignment(assignment_id)
        if not assignment or not assignment['is_active']:
            raise ValueError("Assignment not found or inactive")
        
        # Check if already submitted
        existing_submission = self.get_student_submission(assignment_id, student_username)
        if existing_submission:
            raise ValueError("Assignment already submitted")
        
        # Determine if submission is late
        due_date = datetime.fromisoformat(assignment['due_date'])
        is_late = datetime.now() > due_date
        
        submission = StudentSubmission(
            id=submission_id,
            assignment_id=assignment_id,
            student_username=student_username,
            submitted_at=datetime.now().isoformat(),
            content=submission_content,
            files=files or [],
            status='late' if is_late else 'submitted'
        )
        
        submissions = self.load_submissions()
        submissions.append(asdict(submission))
        self.save_submissions(submissions)
        
        return submission_id
    
    def get_student_submission(self, assignment_id: str, student_username: str) -> Optional[Dict[str, Any]]:
        """Get student's submission for an assignment"""
        submissions = self.load_submissions()
        for submission in submissions:
            if (submission['assignment_id'] == assignment_id and 
                submission['student_username'] == student_username):
                return submission
        return None
    
    def get_submissions_for_assignment(self, assignment_id: str) -> List[Dict[str, Any]]:
        """Get all submissions for an assignment"""
        submissions = self.load_submissions()
        return [s for s in submissions if s['assignment_id'] == assignment_id]
    
    def get_student_submissions(self, student_username: str) -> List[Dict[str, Any]]:
        """Get all submissions by a student"""
        submissions = self.load_submissions()
        return [s for s in submissions if s['student_username'] == student_username]
    
    def grade_submission(self, submission_id: str, grade: int, feedback: str, 
                        graded_by: str) -> bool:
        """Grade a submission"""
        submissions = self.load_submissions()
        for i, submission in enumerate(submissions):
            if submission['id'] == submission_id:
                submissions[i].update({
                    'grade': grade,
                    'feedback': feedback,
                    'graded_by': graded_by,
                    'graded_at': datetime.now().isoformat(),
                    'status': 'graded'
                })
                self.save_submissions(submissions)
                return True
        return False
    
    def get_submission(self, submission_id: str) -> Optional[Dict[str, Any]]:
        """Get submission by ID"""
        submissions = self.load_submissions()
        for submission in submissions:
            if submission['id'] == submission_id:
                return submission
        return None
    
    def get_assignment_statistics(self) -> Dict[str, Any]:
        """Get assignment statistics"""
        assignments = self.load_assignments()
        submissions = self.load_submissions()
        
        active_assignments = [a for a in assignments if a['is_active']]
        total_submissions = len(submissions)
        graded_submissions = len([s for s in submissions if s['status'] == 'graded'])
        
        return {
            'total_assignments': len(active_assignments),
            'total_submissions': total_submissions,
            'graded_submissions': graded_submissions,
            'pending_grading': total_submissions - graded_submissions,
            'assignments_by_module': self._get_assignments_by_module_stats(active_assignments),
            'recent_submissions': self._get_recent_submissions(submissions, 5)
        }
    
    def _get_assignments_by_module_stats(self, assignments: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get assignment count by module"""
        stats = {}
        for assignment in assignments:
            module = assignment['lab_module']
            stats[module] = stats.get(module, 0) + 1
        return stats
    
    def _get_recent_submissions(self, submissions: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """Get recent submissions"""
        sorted_submissions = sorted(submissions, 
                                  key=lambda x: x['submitted_at'], 
                                  reverse=True)
        return sorted_submissions[:limit]
    
    def delete_assignment(self, assignment_id: str) -> bool:
        """Delete an assignment and all related submissions"""
        # Delete the assignment
        assignments = self.load_assignments()
        initial_count = len(assignments)
        assignments = [a for a in assignments if a['id'] != assignment_id]
        
        if len(assignments) == initial_count:
            return False  # Assignment not found
        
        self.save_assignments(assignments)
        
        # Delete related submissions
        submissions = self.load_submissions()
        submissions = [s for s in submissions if s['assignment_id'] != assignment_id]
        self.save_submissions(submissions)
        
        return True
    
    def create_sample_assignments(self):
        """Create sample assignments for testing"""
        sample_assignments = [
            {
                'title': 'Caesar Cipher Analysis',
                'description': 'Analyze and break a Caesar cipher using frequency analysis',
                'lab_module': 'shift_cipher',
                'difficulty': 'easy',
                'points': 10,
                'due_days': 7,
                'instructions': 'Use the provided ciphertext to determine the shift value and decrypt the message. Show your work including frequency analysis.',
                'resources': ['Frequency Analysis Guide', 'Caesar Cipher Reference']
            },
            {
                'title': 'Mono-Alphabetic Cipher Challenge',
                'description': 'Decrypt a mono-alphabetic substitution cipher',
                'lab_module': 'mono_alphabetic',
                'difficulty': 'medium',
                'points': 15,
                'due_days': 10,
                'instructions': 'Decrypt the given ciphertext using frequency analysis and pattern recognition. Document your methodology.',
                'resources': ['Letter Frequency Tables', 'Pattern Analysis Guide']
            },
            {
                'title': 'AES Implementation Project',
                'description': 'Implement basic AES encryption/decryption',
                'lab_module': 'aes_algorithm',
                'difficulty': 'hard',
                'points': 25,
                'due_days': 14,
                'instructions': 'Implement AES-128 encryption and decryption. Test with provided test vectors.',
                'resources': ['AES Specification', 'Implementation Guide', 'Test Vectors']
            },
            {
                'title': 'Hash Function Security Analysis',
                'description': 'Analyze the security properties of different hash functions',
                'lab_module': 'hash_function',
                'difficulty': 'medium',
                'points': 20,
                'due_days': 12,
                'instructions': 'Compare MD5, SHA-1, and SHA-256. Discuss vulnerabilities and use cases.',
                'resources': ['Hash Function Comparison', 'Security Analysis Framework']
            }
        ]
        
        for assignment_data in sample_assignments:
            self.create_assignment(
                created_by='admin',
                **assignment_data
            )

# Global assignment manager instance
assignment_manager = AssignmentManager()