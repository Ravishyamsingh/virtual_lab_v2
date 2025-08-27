from flask import Blueprint, render_template
from auth import login_required

shift_cipher = Blueprint('shift_cipher', __name__)

@shift_cipher.route('/shift-cipher')
@login_required
def home():
    return render_template('pages/shift-cipher/aim.html', active_page='aim')

@shift_cipher.route('/shift-cipher/aim')
@login_required
def aim():
    return render_template('pages/shift-cipher/aim.html', active_page='aim')

@shift_cipher.route('/shift-cipher/theory')
@login_required
def theory():
    return render_template('pages/shift-cipher/theory.html', active_page='theory')

@shift_cipher.route('/shift-cipher/objective')
@login_required
def objective():
    return render_template('pages/shift-cipher/objective.html', active_page='objective')

@shift_cipher.route('/shift-cipher/procedure')
@login_required
def procedure():
    return render_template('pages/shift-cipher/procedure.html', active_page='procedure')

@shift_cipher.route('/shift-cipher/simulation')
@login_required
def simulation():
    return render_template('pages/shift-cipher/simulation.html', active_page='simulation')

@shift_cipher.route('/shift-cipher/assignment')
@login_required
def assignment():
    return render_template('pages/shift-cipher/assignment.html', active_page='assignment')

@shift_cipher.route('/shift-cipher/reference')
@login_required
def reference():
    return render_template('pages/shift-cipher/reference.html', active_page='reference')

@shift_cipher.route('/shift-cipher/feedback')
@login_required
def feedback():
    return render_template('pages/shift-cipher/feedback.html', active_page='feedback') 