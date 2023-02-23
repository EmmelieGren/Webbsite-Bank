from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData
from random import randint
import os 

from areas.customerpage import customerBluePrint
from areas.transactionpage import transactionBluePrint
from areas.staffpages import staffBluePrint
from areas.index import indexBluePrint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/bank'
#app.config['SECRET_KEY'] = os.urandom(32)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"

db.app = app
db.init_app(app)
migrate = Migrate(app,db)


app.register_blueprint(customerBluePrint)
app.register_blueprint(transactionBluePrint)
app.register_blueprint(staffBluePrint)
app.register_blueprint(indexBluePrint)


if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData(app,db)
        app.run(debug = True)