from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData
from random import randint
import os 

from flask_security import hash_password
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v3 as fsqla

from areas.customerpage import customerBluePrint
from areas.transactionpage import transactionBluePrint
from areas.staffpages import staffBluePrint
from areas.index import indexBluePrint


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/bank'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Apres123:Algebra123@mlibank.mysql.database.azure.com/mlibank'

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"


db.app = app
db.init_app(app)
migrate = Migrate(app,db)


fsqla.FsModels.set_db_info(db)
class Role(db.Model, fsqla.FsRoleMixin):
    pass
class User(db.Model, fsqla.FsUserMixin):
    pass
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
app.security = Security(app, user_datastore)


app.register_blueprint(customerBluePrint)
app.register_blueprint(transactionBluePrint)
app.register_blueprint(staffBluePrint)
app.register_blueprint(indexBluePrint)


if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData(app,db)
        app.run(debug=True)

