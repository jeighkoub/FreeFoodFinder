import flask
import WebInterface

@WebInterface.app.route('/hello/', methods=['GET'])
def helloworld():
    return 'Hello World!'