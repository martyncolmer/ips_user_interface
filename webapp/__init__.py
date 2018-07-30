from flask import Flask, render_template, redirect, url_for
import logging
from logging.handlers import RotatingFileHandler
import inspect

from . import settings


def create_app(test_config=None):

    # Create and configure the app
    app = Flask(__name__)

    app.config.from_object(settings)

    # initialize the log handler
    log_handler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)

    # set the log handler level
    log_handler.setLevel(logging.INFO)

    # set the app logger level
    app.logger.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)

    app.logger.addHandler(log_handler)

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
