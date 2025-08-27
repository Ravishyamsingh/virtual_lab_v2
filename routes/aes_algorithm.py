from flask import Blueprint, render_template

aes_algorithm = Blueprint('aes_algorithm', __name__, url_prefix='/aes-algorithm')

@aes_algorithm.route('/aim')
def aim():
    return render_template('pages/aes-algorithm/aim.html')

@aes_algorithm.route('/theory')
def theory():
    return render_template('pages/aes-algorithm/theory.html')

@aes_algorithm.route('/objective')
def objective():
    return render_template('pages/aes-algorithm/objective.html')

@aes_algorithm.route('/procedure')
def procedure():
    return render_template('pages/aes-algorithm/procedure.html')

@aes_algorithm.route('/simulation')
def simulation():
    return render_template('pages/aes-algorithm/simulation.html')

@aes_algorithm.route('/assignment')
def assignment():
    return render_template('pages/aes-algorithm/assignment.html')

@aes_algorithm.route('/reference')
def reference():
    return render_template('pages/aes-algorithm/reference.html')

@aes_algorithm.route('/feedback')
def feedback():
    return render_template('pages/aes-algorithm/feedback.html')
