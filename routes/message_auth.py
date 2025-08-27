from flask import Blueprint, render_template

message_auth = Blueprint('message_auth', __name__)

@message_auth.route('/message-authentication/aim')
def aim():
    return render_template('pages/message-authentication/aim.html')

@message_auth.route('/message-authentication/objective')
def objective():
    return render_template('pages/message-authentication/objective.html')

@message_auth.route('/message-authentication/theory')
def theory():
    return render_template('pages/message-authentication/theory.html')

@message_auth.route('/message-authentication/procedure')
def procedure():
    return render_template('pages/message-authentication/procedure.html')

@message_auth.route('/message-authentication/simulation')
def simulation():
    return render_template('pages/message-authentication/simulation.html')

@message_auth.route('/message-authentication/assignment')
def assignment():
    return render_template('pages/message-authentication/assignment.html')

@message_auth.route('/message-authentication/reference')
def reference():
    return render_template('pages/message-authentication/reference.html')

@message_auth.route('/message-authentication/feedback')
def feedback():
    return render_template('pages/message-authentication/feedback.html')
