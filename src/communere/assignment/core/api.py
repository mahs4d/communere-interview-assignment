from flask import Flask

from .di import Container
from .errors import ApiError
from ..auth.api import blueprint as auth_blueprint
from ..project.api import blueprint as project_blueprint


def create_flask_app():
    app = Flask(__name__)
    app.container = Container()

    app.register_error_handler(ApiError, lambda e: ({'message': e.message}, e.status))

    app.register_blueprint(project_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
