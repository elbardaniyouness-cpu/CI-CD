"""
Counter Service

Package initializer: creates the Flask app and wires up routes and logging.
"""
from flask import Flask

app = Flask(__name__)

# Import the routes after the Flask app is created
# pylint: disable=wrong-import-position, cyclic-import
from service import routes  # noqa: F401, E402
from service.common import log_handlers  # noqa: E402

log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  C O U N T E R   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")
