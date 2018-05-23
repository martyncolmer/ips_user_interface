from flask import Flask, render_template, redirect, url_for

from . import settings


def create_app(test_config=None):

    # Create and configure the app
    app = Flask(__name__)

    app.config.from_object(settings)

    if test_config:
        # Override default Settings with test config if passed in
        app.config.from_mapping(test_config)

    # Register Blueprints
    from . import dashboard
    app.register_blueprint(dashboard.bp)

    # Register Simple Index Page
    @app.route('/')
    def index():
        return render_template('index.html')

    return app