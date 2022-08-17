from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from .models import db

# import blueprints
from .auth.routes import auth
from .poke.routes import poke

from .models import User
from .models import Pokemon

app = Flask(__name__)
login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# register blueprints
app.register_blueprint(auth)
app.register_blueprint(poke)

app.config.from_object(Config)

# initialize our database to work with our app

db.init_app(app)
migrate = Migrate(app, db)
login.init_app(app)


login.login_view = 'auth.logMeIn'


from . import routes
from . import models
