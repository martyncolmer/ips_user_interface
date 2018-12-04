from flask import Flask, redirect, url_for, session
import logging
import getpass
from logging import StreamHandler
import pika

from . import settings


class RabbitMQHandler(logging.StreamHandler):

    def __init__(self):

        logging.StreamHandler.__init__(self)

        # Credentials are the login details for the test Rabbit server
        rabbit_credentials = pika.PlainCredentials('sst_user', 'XECnWyQ5z')

        # Parameters to point to the Rabbit server
        rabbit_parameters = pika.ConnectionParameters(
            host='rabbitmq-d-01',
            port=5672,
            virtual_host='/',
            credentials=rabbit_credentials)

        # Establish a connection with the RabbitMQ server.
        self.connection = pika.BlockingConnection(rabbit_parameters)

        self.exchange_name = 'log'
        self.exchange_type = 'direct'
        self.queue = 'IPS_rabbit_test'
        self.channel = self.connection.channel()

        if (self.exchange_name != ''):
            self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)

            self.channel.queue_declare(queue=self.queue, durable=False, auto_delete=True)
            self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue)

    def emit(self, record):
        self.acquire()
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.queue, body=self.format(record))
        self.release()


def create_app(test_config=None):

    # Create and configure the app
    app = Flask(__name__)

    app.config.from_object(settings)

    # initialize the log handler
    rabbit_mq_handler = RabbitMQHandler()
    # set the log handler level
    rabbit_mq_handler.setLevel(logging.INFO)

    app.logger = logging.getLogger('pika')

    # set the app logger level
    app.logger.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s , %(funcName)s , %(levelname)s , %(message)s')
    rabbit_mq_handler.setFormatter(formatter)

    app.logger.addHandler(rabbit_mq_handler)

    app.logger.disabled = True

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
