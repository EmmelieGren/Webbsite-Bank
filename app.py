from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData, Customer

 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/bank'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 
 

@app.route("/")
def startpage():
    return render_template("index.html")

@app.route("/category/<id>")
def category(id):
    return "hej2"
    # products = Product.query.all()
    # return render_template("category.html", products=products)

@app.route("/customers")
def customersPage():
    customers = Customer.query.all()
    return render_template("customers.html", customers = customers)


@app.route("/customer/<id>")
def customer(id):
    customer = Customer.query.filter_by(Id=id).first()
    return render_template("customer.html", customer=customer)


if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
        seedData(db)
        app.run()