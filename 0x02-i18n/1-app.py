#!/usr/bin/env python3
"""This models creates a basic Flask App
   with Babel configurations.
"""

from flask_babel import Babel
from flask import Flask, render_template

app = Flask(__name__)
babel = Babel(app)


class Config:
    """Babel Configuration with
       LANGUAGES class attribute
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@app.route('/', methods=['GET'], strict_slashes=True)
def index():
    """Basic route with Babel config"""
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(debug=True)
