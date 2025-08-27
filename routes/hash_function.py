from flask import Blueprint, render_template
from functools import wraps
from auth import login_required

hash_function = Blueprint('hash_function', __name__, url_prefix='/hash-function')

@hash_function.route('/')
@login_required
def home():
    return render_template('pages/hash-function/aim.html')

@hash_function.route('/aim')
@login_required
def aim():
    return render_template('pages/hash-function/aim.html')

@hash_function.route('/theory')
@login_required
def theory():
    return render_template('pages/hash-function/theory.html')

@hash_function.route('/objective')
@login_required
def objective():
    return render_template('pages/hash-function/objective.html')

@hash_function.route('/procedure')
@login_required
def procedure():
    return render_template('pages/hash-function/procedure.html')

@hash_function.route('/simulation')
@login_required
def simulation():
    return render_template('pages/hash-function/simulation.html')

@hash_function.route('/assignment')
@login_required
def assignment():
    return render_template('pages/hash-function/assignment.html')

@hash_function.route('/reference')
@login_required
def reference():
    return render_template('pages/hash-function/reference.html')

@hash_function.route('/feedback')
@login_required
def feedback():
    return render_template('pages/hash-function/feedback.html')
