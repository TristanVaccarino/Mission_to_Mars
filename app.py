# URL to Canvas page: https://courses.bootcampspot.com/courses/976/pages/10-dot-5-1-use-flask-to-create-a-web-app?module_item_id=358770

# Call Dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# initialize app
app = Flask(__name__)

# setup Mongo Flask mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set app main route
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Set the scrape route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
   app.run()