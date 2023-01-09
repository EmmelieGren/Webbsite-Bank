from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

from model import db, seedData

 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:my-secret-pw@localhost/bank'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)
 
 

@app.route("/")
def startpage():
    return "hej"
    # trendingCategories = Category.query.all()
    # return render_template("index.html", trendingCategories=trendingCategories)

@app.route("/category/<id>")
def category(id):
    return "hej2"
    # products = Product.query.all()
    # return render_template("category.html", products=products)


if __name__  == "__main__":
    with app.app_context():
        upgrade()
    
        seedData(db)
        app.run()

