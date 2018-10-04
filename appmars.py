# Use MongoDB with Flask templating to create a new HTML page that displays all of the information 
# that was scraped from the URLs above.
# a. Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called 
#   `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
# b. Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
# c. Store the return value in Mongo as a Python dictionary.
# d. Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
# e. Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data 
#    in the appropriate HTML elements. Use the following as a guide for what the final product should look like, 
#    but feel free to create your own design.

# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scraping
#from mars_scraping.py import mars_scrape
#from mars_scraping.py import init_browser

# create instance of Flask app
# Use PyMongo to set up mongo connection; define db and collection

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
# mars_db is the database; mars_data is the collection

@app.route("/")
def index():
    # Get the data from mobgodb.
    mars_mission_data = mongo.db.mars_data_coll.find_one()

    # return template and data
    return render_template("index.html", mars_mission_data=mars_mission_data)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
    # Run scraped functions
    mars_mission_data = mars_scraping.mars_scrape()

    # Insert mars_mission_data into database
    mongo.db.mars_data.update({},mars_mission_data,upsert = True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
