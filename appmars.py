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
import pymongo 
import mars_scraping

#from mars_scraping.py import init_browser
# create instance of Flask app


#------------------------------------------------------------------------------------#
# Flask Setup #
#------------------------------------------------------------------------------------#
app = Flask(__name__)

# Use PyMongo to set up mongo connection; define db and collection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
#mongo = PyMongo(app)
#------------------------------------------------------------------------------------#
# Local MongoDB connection #
#------------------------------------------------------------------------------------#
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
## create / Use database
db = client.mars_db
## create/use collection. 
coll = db.mars_data_coll

#------------------------------------------------------------------------------------#
# MLab MongoDB connection #
#------------------------------------------------------------------------------------#
#conn = 'mongodb://mars_admin:marsvsk9=@ds255332.mlab.com:55332/healthi_db'
#client = pymongo.MongoClient(conn,ConnectTimeoutMS=30000)
##Database connection
#db = client.get_default_database()
###db = client.get_database('healthi_db')

# create route that renders index.html template and finds documents from mongo
# mars_db is the database; mars_data is the collection
@app.route("/")
def index():
    # Get the data from mongodb.
    mars_mission_data = coll.find_one()

    # return template and data
    return render_template("index.html", mars_mission_data=mars_mission_data)

#import python function from mars_scraping.py
from mars_scraping import mars_scrape
# Route that will trigger scrape function.
@app.route("/scrape")
def scrape():
    # Run scrape function.
    mars_mission_data = mars_scrape()
    #print (f'in scrape function. will take a few min to  execute  - {type(mars_mission_data)}')
    #print (f'printing {mars_mission_data}')  

    # Insert mars_mission_data into database
    coll.update({"id": 1}, {"$set": mars_mission_data}, upsert = True)

    # Redirect back to home page
    #return redirect("/", code=302)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
