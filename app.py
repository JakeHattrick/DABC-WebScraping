from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrapeMars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    marsData = scrapeMars.scrape()
    mars.update({}, marsData, upsert=True)

    return mars


if __name__ == "__main__":
    app.run()