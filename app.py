from flask import Flask
from routes import register_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    register_routes(app)
    CORS(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
