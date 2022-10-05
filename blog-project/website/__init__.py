from flask import Flask
from os import path
from flask_login import LoginManager
from website.filters import fromnow, trim

app = Flask(__name__)
app.config['SECRET_KEY'] = "helloworld"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def create_app():

    from .views import views
    from .auth import auth
    from .models import User
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    add_filters(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def add_filters(app):
    app.jinja_env.filters['timesago'] = fromnow
    app.jinja_env.filters['trim'] = trim

