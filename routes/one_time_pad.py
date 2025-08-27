from flask import Blueprint, render_template
from auth import login_required

one_time_pad = Blueprint('one_time_pad', __name__)

@one_time_pad.route('/one-time-pad')
@login_required
def home():
    return render_template('pages/one-time-pad/aim.html', active_page='aim')

@one_time_pad.route('/one-time-pad/aim')
@login_required
def aim():
    return render_template('pages/one-time-pad/aim.html', active_page='aim')

@one_time_pad.route('/one-time-pad/theory')
@login_required
def theory():
    return render_template('pages/one-time-pad/theory.html', active_page='theory')

@one_time_pad.route('/one-time-pad/objective')
@login_required
def objective():
    return render_template('pages/one-time-pad/objective.html', active_page='objective')

@one_time_pad.route('/one-time-pad/procedure')
@login_required
def procedure():
    return render_template('pages/one-time-pad/procedure.html', active_page='procedure')

@one_time_pad.route('/one-time-pad/simulation')
@login_required
def simulation():
    return render_template('pages/one-time-pad/simulation.html', active_page='simulation')

@one_time_pad.route('/one-time-pad/assignment')
@login_required
def assignment():
    return render_template('pages/one-time-pad/assignment.html', active_page='assignment')

@one_time_pad.route('/one-time-pad/reference')
@login_required
def reference():
    return render_template('pages/one-time-pad/reference.html', active_page='reference')

@one_time_pad.route('/one-time-pad/feedback')
@login_required
def feedback():
    return render_template('pages/one-time-pad/feedback.html', active_page='feedback')
