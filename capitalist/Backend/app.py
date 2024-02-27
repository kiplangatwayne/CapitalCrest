from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import routes_app
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capital_crest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize the SQLAlchemy database
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register routes and pass the db object
app.register_blueprint(routes_app, db=db)

if __name__ == '__main__':
    app.run(debug=True)
