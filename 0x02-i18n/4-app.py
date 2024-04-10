#!/usr/bin/env python3
"""This models creates a basic Flask App
   that get locale from request.
"""

from flask_babel import Babel
from flask import Flask, request, render_template

app = Flask(__name__)
babel = Babel(app)


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


@app.route('/', methods=['GET'], strict_slashes=True)
def index():
    """Get user local language"""
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run(debug=True)
