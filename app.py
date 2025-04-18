from flask import Flask
from routes import register_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    register_routes(app)
    
    CORS(app, resources={r"/api/*": {"origins": ["https://next-finance-tracker-six.vercel.app", "http://127.0.0.1:3000"]}})

    @app.route('/')
    def index():
        return "App is running!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
