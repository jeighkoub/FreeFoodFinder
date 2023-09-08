"""
index (main) view.

URLs include:
/
"""
import flask
import WebInterface


@WebInterface.app.route('/', methods=['GET'])
def show_index():
    """Display / route."""

    return flask.render_template("index.html")

