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
    from . import dashboard, system_info, new_run, manage_run, export
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(system_info.bp)
    app.register_blueprint(new_run.bp)
    app.register_blueprint(manage_run.bp)
    app.register_blueprint(export.bp)

    # Register Simple Index Page
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.dashboard_view'))

    return app