#!/usr/bin/env python3
"""Simple flask app
"""
import flask
from auth import Auth

app = flask.Flask(__name__)
auth = Auth()


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
        auth.register_user(email=email, password=password)
    except ValueError as v:
        return flask.jsonify({"message": "email already registered"}), 400
    return flask.jsonify({"email": email, "message": "user created"})

# @app.route('')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")
