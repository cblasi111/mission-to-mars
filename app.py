from flask import Flask, render_template
# Import scrape_mars
import scrape_mars

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
mongo = PyMongo(app, uri='mongodb://localhost:27017/mission_to_mars')

# Set route
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape 
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mongo.db.mars.update({}, mars_data, upsert = True)
    return redirect("http://127.0.0.1:5000//", code=302)

if __name__ == "__main__":
    app.run(debug=True)
