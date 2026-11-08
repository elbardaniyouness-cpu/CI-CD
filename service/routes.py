"""
Counter Service routes

Endpoints:
    GET    /health              - health check
    GET    /                    - service info
    GET    /counters            - list all counters
    POST   /counters/<name>     - create a counter
    GET    /counters/<name>     - read a counter
    PUT    /counters/<name>     - increment a counter
    DELETE /counters/<name>     - delete a counter
"""
from flask import jsonify, abort
from service import app
from service.common import status

COUNTER = {}


@app.route("/health")
def health():
    """Health check"""
    return jsonify(status="OK"), status.HTTP_200_OK


@app.route("/")
def index():
    """Service information"""
    app.logger.info("Request for Base URL")
    return jsonify(
        name="Counter Service",
        version="1.0",
        url="/counters",
    ), status.HTTP_200_OK


@app.route("/counters", methods=["GET"])
def list_counters():
    """List all counters"""
    app.logger.info("Request to list all counters...")
    counters = [dict(name=name, counter=value) for name, value in COUNTER.items()]
    return jsonify(counters)


@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Create a new counter"""
    app.logger.info("Request to Create counter: %s...", name)
    if name in COUNTER:
        abort(status.HTTP_409_CONFLICT, f"Counter {name} already exists")
    COUNTER[name] = 0
    return jsonify(name=name, counter=0), status.HTTP_201_CREATED


@app.route("/counters/<name>", methods=["GET"])
def read_counter(name):
    """Read a counter"""
    app.logger.info("Request to Read counter: %s...", name)
    if name not in COUNTER:
        abort(status.HTTP_404_NOT_FOUND, f"Counter {name} does not exist")
    return jsonify(name=name, counter=COUNTER[name])


@app.route("/counters/<name>", methods=["PUT"])
def update_counter(name):
    """Increment a counter"""
    app.logger.info("Request to Update counter: %s...", name)
    if name not in COUNTER:
        abort(status.HTTP_404_NOT_FOUND, f"Counter {name} does not exist")
    COUNTER[name] += 1
    return jsonify(name=name, counter=COUNTER[name])


@app.route("/counters/<name>", methods=["DELETE"])
def delete_counter(name):
    """Delete a counter"""
    app.logger.info("Request to Delete counter: %s...", name)
    COUNTER.pop(name, None)
    return "", status.HTTP_204_NO_CONTENT


def reset_counters():
    """Remove all counters (used by tests)"""
    COUNTER.clear()
