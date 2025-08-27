from flask import Blueprint, render_template

des_algorithm = Blueprint('des_algorithm', __name__, url_prefix='/des-algorithm')

@des_algorithm.route('/aim')
def aim():
    return render_template('pages/des-algorithm/aim.html')

@des_algorithm.route('/theory')
def theory():
    return render_template('pages/des-algorithm/theory.html')

@des_algorithm.route('/objective')
def objective():
    return render_template('pages/des-algorithm/objective.html')

@des_algorithm.route('/procedure')
def procedure():
    return render_template('pages/des-algorithm/procedure.html')

@des_algorithm.route('/simulation')
def simulation():
    return render_template('pages/des-algorithm/simulation.html')

@des_algorithm.route('/assignment')
def assignment():
    return render_template('pages/des-algorithm/assignment.html')

@des_algorithm.route('/reference')
def reference():
    return render_template('pages/des-algorithm/reference.html')

@des_algorithm.route('/feedback')
def feedback():
    return render_template('pages/des-algorithm/feedback.html')
