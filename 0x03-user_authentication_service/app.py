#!/usr/bin/env python3
"""Simple flask app
"""
import flask
from auth import Auth

app = flask.Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def root():
    """root route"""
    return flask.jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def user_route():
    """users route"""
    req = flask.request
    email = req.form.get('email')
    password = req.form.get('password')
    try:
        AUTH.register_user(email=email, password=password)
    except ValueError as v:
        return flask.jsonify({"message": "email already registered"}), 400
    return flask.jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """creates a new session for user and store in cookie"""
    email = flask.request.form.get('email')
    password = flask.request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        res = flask.make_response(flask.jsonify({
            "email": email,
            "message": "logged in"
        }))
        res.set_cookie("session_id", session_id)
        return res
    else:
        flask.abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """destroys user session"""
    session_id = flask.request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return flask.redirect(flask.url_for('root'))
    return flask.make_response(), 403


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """returns user profile based on cookie value"""
    session_id = flask.request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return flask.jsonify({"email": user.email})
    return flask.make_response(), 403


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_pwd_rest_token():
    """responds with password reset token"""
    try:
        email = flask.request.form.get('email')
        token = AUTH.get_reset_password_token(email)
        return flask.jsonify({"email": email, "reset_token": token})
    except Exception:
        return flask.make_response(), 403


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_pwd():
    """updates user password"""
    try:
        email = flask.request.form.get('email')
        reset_token = flask.request.form.get('reset_token')
        new_pwd = flask.request.form.get('password')
        AUTH.update_password(reset_token, new_pwd)
        return flask.jsonify({"email": email, "message": "Password updated"})
    except Exception:
        return flask.make_response(), 403


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")
