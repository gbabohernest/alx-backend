#!/usr/bin/env python3
"""Defines a mock logging in behavior"""

from flask import Flask, request, render_template, g
from flask_babel import Babel
from typing import Union

app = Flask(__name__)
babel = Babel(app)

# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Babel Configuration class.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Pick the best language translation
       to use for a request
    """
    # local param is in request args
    if 'locale' in request.args:
        requested_locale = request.args['locale']
        # requested locale is supported?
        if requested_locale in app.config['LANGUAGES']:
            return requested_locale

    # local param is not present | support, use Default behaviour
    return request.accept_languages.best_match(
        app.config['LANGUAGES'])


@app.before_request
def before_request():
    """Find a user if any and set it as a global on flask.g.user."""
    user_id = request.args.get('login_as')
    if user_id:
        user = get_user()
        if user:
            # Set user as a global on flask.g.user
            g.user = user
        else:
            g.user = None
    else:
        g.user = None


def get_user(user_id: int) -> Union[dict, None]:
    """Get user from mock user table."""
    try:
        user_id = request.args.get('login_as')
        if user_id:
            return users.get(int(user_id))
    except ValueError:
        return None


@app.route('/', methods=['GET'], strict_slashes=True)
def index():
    """Render the index page."""
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(debug=True)
