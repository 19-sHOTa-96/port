from flask import Flask

class HelloExtension:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request()        


hello = HelloExtension()

def create_app():
    app = Flask(__name__)
    hello.init_app(app)
    return app

create_app()