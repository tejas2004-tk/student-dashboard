import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db
from models.student import Student
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)

    # ✅ Ensure database folder exists
    if not os.path.exists('database'):
        os.makedirs('database')

    # ✅ Use absolute path to avoid errors
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR}/database/student.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect if user is not logged in

    @login_manager.user_loader
    def load_user(user_id):
        return Student.query.get(int(user_id))  # Fetch user by ID from database

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
