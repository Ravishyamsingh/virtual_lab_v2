from flask import Blueprint, render_template, request, jsonify
from auth import login_required
from .ciphers.mono_alphabetic_cipher import MonoAlphabeticCipher

mono_alphabetic = Blueprint('mono_alphabetic', __name__)
cipher = MonoAlphabeticCipher()

@mono_alphabetic.route('/mono-alphabetic')
@login_required
def home():
    return render_template('pages/mono-alphabetic/aim.html', active_page='aim')

@mono_alphabetic.route('/mono-alphabetic/encrypt', methods=['POST'])
@login_required
def encrypt():
    """API endpoint for encryption"""
    data = request.get_json()
    plaintext = data.get('text', '')
    if not plaintext:
        return jsonify({'error': 'No text provided'}), 400
    
    ciphertext, frequencies = cipher.encrypt(plaintext)
    return jsonify({
        'ciphertext': ciphertext,
        'frequencies': frequencies,
        'key': cipher.get_substitution_table()
    })

@mono_alphabetic.route('/mono-alphabetic/decrypt', methods=['POST'])
@login_required
def decrypt():
    """API endpoint for decryption"""
    data = request.get_json()
    ciphertext = data.get('text', '')
    custom_key = data.get('key', None)
    
    if not ciphertext:
        return jsonify({'error': 'No text provided'}), 400
    
    if custom_key:
        try:
            cipher.set_key(custom_key)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
    
    plaintext, frequencies = cipher.decrypt(ciphertext)
    return jsonify({
        'plaintext': plaintext,
        'frequencies': frequencies,
        'key': cipher.get_substitution_table()
    })

@mono_alphabetic.route('/mono-alphabetic/aim')
@login_required
def aim():
    return render_template('pages/mono-alphabetic/aim.html', active_page='aim')

@mono_alphabetic.route('/mono-alphabetic/theory')
@login_required
def theory():
    return render_template('pages/mono-alphabetic/theory.html', active_page='theory')

@mono_alphabetic.route('/mono-alphabetic/objective')
@login_required
def objective():
    return render_template('pages/mono-alphabetic/objective.html', active_page='objective')

@mono_alphabetic.route('/mono-alphabetic/procedure')
@login_required
def procedure():
    return render_template('pages/mono-alphabetic/procedure.html', active_page='procedure')

@mono_alphabetic.route('/mono-alphabetic/simulation')
@login_required
def simulation():
    return render_template('pages/mono-alphabetic/simulation.html', active_page='simulation')

@mono_alphabetic.route('/mono-alphabetic/assignment')
@login_required
def assignment():
    return render_template('pages/mono-alphabetic/assignment.html', active_page='assignment')

@mono_alphabetic.route('/mono-alphabetic/reference')
@login_required
def reference():
    return render_template('pages/mono-alphabetic/reference.html', active_page='reference')

@mono_alphabetic.route('/mono-alphabetic/feedback')
@login_required
def feedback():
    return render_template('pages/mono-alphabetic/feedback.html', active_page='feedback') 