from flask import Blueprint, render_template

dsa_algorithm = Blueprint('dsa_algorithm', __name__, url_prefix='/dsa-algorithm')

@dsa_algorithm.route('/aim')
def aim():
    return render_template('pages/dsa-algorithm/aim.html')

@dsa_algorithm.route('/theory')
def theory():
    return render_template('pages/dsa-algorithm/theory.html')

@dsa_algorithm.route('/objective')
def objective():
    return render_template('pages/dsa-algorithm/objective.html')

@dsa_algorithm.route('/procedure')
def procedure():
    return render_template('pages/dsa-algorithm/procedure.html')

@dsa_algorithm.route('/simulation')
def simulation():
    return render_template('pages/dsa-algorithm/simulation.html')

@dsa_algorithm.route('/assignment')
def assignment():
    return render_template('pages/dsa-algorithm/assignment.html')

@dsa_algorithm.route('/reference')
def reference():
    return render_template('pages/dsa-algorithm/reference.html')

@dsa_algorithm.route('/feedback')
def feedback():
    return render_template('pages/dsa-algorithm/feedback.html')
