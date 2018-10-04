# coding: utf-8
# # Web scraping to get data for the Mars Mission.
# Import Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd 
import time
import datetime
from pprint import pprint

#define  function for exec path for chromedriver.exe.  
def init_browser():
    executable_path = {'executable_path': 'C:/ChromeSafe/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def mars_scrape():
    # # Initialize PyMongo to work with MongoDBs
    # conn = 'mongodb://localhost:27017'
    # client = pymongo.MongoClient(conn)
    
    #Create empty dictionay to store all the mars information.
    mars_info_dict=dict()

    # # Part  1.	### NASA Mars News
    #Define url and browse the site using chrome. 
    url = 'https://mars.nasa.gov/news/'
    browser = init_browser()
    browser.visit(url)
    html = browser.html
    #create soup object and use beautiful soup to parse html. 
    soup1 = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    ## Mars space images 
    #* Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    #* Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a 
    #* variable called `featured_image_url`. Make sure to find the image url to the full size `.jpg` image.
    #* Make sure to save a complete url string for this image.
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    full_image = browser.find_by_id('full_image')
    full_image.click()
    # Scrape information from html for https://mars.nasa.gov/news/. class is "content_title' for news title.
    try :
        result_title = soup1.find('ul', class_="item_list").find('li',class_="slide").find('div',class_="content_title").text
        #Class is class="article_teaser_body" for para text. 
        news_body = soup1.find('ul',class_="item_list").find('li',class_="slide").find('div',class_="article_teaser_body").text
        print("The news title is " + result_title)
        #print(f"The news_title is: {news_title}") 
        print("The news body is " + news_body)
        #print(f"The News Body is: {news_body}") 

    except  AttributeError as Atterror:
        print(Atterror)
    #Append results from part 1 into the final mars_info dictionary.
    
    mars_info_dict["Mars_news_title"] = result_title
    mars_info_dict["Mars_news_body"] = news_body
    pprint(mars_info_dict)

    ## end of part 1 to retrieve news  title and a news body. 

    # # Part 2.	### JPL Mars Space Images - Featured Image

    # In[6]:


    #click on the link for "more info"
    time.sleep(15)
    link_more_info = browser.find_link_by_partial_text('more info')
    link_more_info.click()

    #Retrieve  the  html from the page. Parse htnl using bs4 and find the path for the  full size image.
    fullimg_html2 = browser.html
    soup2 = BeautifulSoup(fullimg_html2, "html.parser")
    fullimg_href = soup2.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov" + fullimg_href

    print(featured_image_url)


    # In[21]:


    #Append featured image url to the Mars dictionary.
    mars_info_dict["Mars_featured_image_url"] = featured_image_url


    # In[22]:


    pprint(mars_info_dict)


    # # Part 3 . ### Mars Weather tweet

    # In[8]:


    ##* Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather 
    ##  tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')


    # In[9]:


    #print(soup.prettify())
    #Save the tweet text for the weather report as a variable called `mars_weather`.
    mars_weather = soup3.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather


    # In[23]:


    #Add weather tweet to the mars_info dict.
    mars_info_dict["Mars_tweet_weather"] = mars_weather


    # In[24]:


    pprint(mars_info_dict)


    # # Part 4.	### Mars Facts

    # In[10]:


    # Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use Pandas to scrape the table containing facts 
    # about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string
    url4 = "http://space-facts.com/mars/"
    df_marsfacts_all = pd.read_html(url4)
    df_marsfacts = df_marsfacts_all[0]
    #df_marsfacts


    # In[11]:


    # Provide appropriate column names for the dataframe. 
    df_marsfacts.columns = ['Mars_Facts', 'Values']

    #convert to html
    df_marsfacts.to_html("mars_facts.html", index=False)


    # In[25]:


    #set index for better retrieval. 
    df_marsfacts.set_index("Mars_Facts")
    #Add another html version of the Mars facts tables.
    mars_facts_html = df_marsfacts.to_html(classes="mars_facts table table-striped")
    mars_info_dict["Mars_facts_table"] = mars_facts_html


    # In[26]:


    pprint(mars_info_dict)


    # # Part 5.	### Mars Hemispheres
    # 

    # In[12]:


    # Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)
    # to obtain high resolution images for each of Mar's hemispheres.
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the 
    # hemisphere name. 
    # Use a Python dictionary to store the data using the keys `img_url` and `title`. append the dictionary with the image url 
    # string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    # use splinter and soup to retrieve html and convert to soup object. 
    url5 =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/"
    browser.visit(url5)
    time.sleep(10)
    html5 = browser.html
    soup5 = BeautifulSoup(html5, "html.parser")


    # In[15]:


    #parse soup object for images of the 4 hemispheres .
    class_collap_results = soup5.find('div', class_="collapsible results")
    hemis_items = class_collap_results.find_all('div',class_='item')


    # In[16]:


    #hemis_items


    # In[17]:


    #loop thru to find tile and the image urls to append to lists. 
    hemis_img_urls_list=list()
    img_urls_list = list()
    title_list = list()
    for h in hemis_items:
        #save title
        h_title = h.h3.text
        title_list.append(h_title)
        
        # find the href link.
        h_href  = "https://astrogeology.usgs.gov" + h.find('a',class_='itemLink product-item')['href']
        
        #print(h_title,h_href)
        
        #browse the link from each page
        browser.visit(h_href)
        time.sleep(5)
        #Retrieve the  image links and store in a list. 
        html5   = browser.html
        soup_img = BeautifulSoup(html5, 'html.parser')
        h_img_url = soup_img.find('div', class_='downloads').find('li').a['href']
        print("h_img_url" + h_img_url)
        img_urls_list.append(h_img_url)
        
        # create a dictionary with  each image and title and append to a list. 
        hemispheres_dict = dict()
        hemispheres_dict['title'] = h_title
        hemispheres_dict['img_url'] = h_img_url
        
        hemis_img_urls_list.append(hemispheres_dict)
        
    print(hemis_img_urls_list)
    print(title_list)
    print(img_urls_list)


    # In[27]:


    #print(len(hemis_img_urls_list))
    #Add hemispheres list  to the mars_info dictionary.
    mars_info_dict["Hemisphere_image_urls"] = hemis_img_urls_list


    # In[28]:


    pprint(mars_info_dict)


    # In[31]:


    #Generate date time and store in the dictionary.
    cur_datetime = datetime.datetime.utcnow()
    mars_info_dict["Date_time"] = cur_datetime


    # In[32]:
    pprint(mars_info_dict)

    #Return final dictionary with all the mars information that was scraped in the 5 steps above. 
    return {
        "News_Title": mars_info_dict["Mars_news_title"],
        "News_Summary" :mars_info_dict["Mars_news_body"],
        "Featured_Image" : mars_info_dict["Mars_featured_image_url"],
        "Weather_Tweet" : mars_info_dict["Mars_tweet_weather"],
        "Facts" : mars_facts_html,
        "Hemisphere_Image_urls": hemis_img_urls_list,
        "Date" : mars_info_dict["Date_time"],
    }

# End of Main scrape function  

#Mainline code to test function mars_scrape()
#mars_data_result = mars_scrape()
#pprint(mars_data_result)

