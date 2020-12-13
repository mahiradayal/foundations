#!/usr/bin/env python
# coding: utf-8

# # School Board Minutes
# 
# Scrape all of the school board minutes from http://www.mineral.k12.nv.us/pages/School_Board_Minutes
# 
# Save a CSV called `minutes.csv` with the date and the URL to the file. The date should be formatted as YYYY-MM-DD.
# 
# **Bonus:** Download the PDF files
# 
# **Bonus 2:** Use [PDF OCR X](https://solutions.weblite.ca/pdfocrx/index.php) on one of the PDF files and see if it can be converted into text successfully.
# 
# * **Hint:** If you're just looking for links, there are a lot of other links on that page! Can you look at the link to know whether it links or minutes or not? You'll want to use an "if" statement.
# * **Hint:** You could also filter out bad links later on using pandas instead of when scraping
# * **Hint:** If you get a weird error that you can't really figure out, you can always tell Python to just ignore it using `try` and `except`, like below. Python will try to do the stuff inside of 'try', but if it hits an error it will skip right out.
# * **Hint:** Remember the codes at http://strftime.org
# * **Hint:** If you have a date that you've parsed, you can use `.dt.strftime` to turn it into a specially-formatted string. You use the same codes (like %B etc) that you use for converting strings into dates.
# 
# ```python
# try:
#   blah blah your code
#   your code
#   your code
# except:
#   pass
# ```
# 
# * **Hint:** You can use `.apply` to download each pdf, or you can use one of a thousand other ways. It'd be good `.apply` practice though!

# In[1]:


import pandas as pd
import requests
import time 
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# In[2]:


from selenium.webdriver.chrome.options import Options


options = Options()
options.add_experimental_option('prefs',  {
    "plugins.always_open_pdf_externally": True
    }
)
url = "http://www.mineral.k12.nv.us/files/4.17.18.pdf"
driver = webdriver.Chrome(options=options)
driver.get(url)


# In[3]:


driver.get("http://www.mineral.k12.nv.us/pages/School_Board_Minutes")


# In[4]:


minutes = driver.find_elements_by_tag_name("p")[8:80]

all_minutes = []

for minute in minutes: 
    try: 
        # date = minute.find_elements_by_tag_name("a")[0].find_elements_by_tag_name("span")[0].text.strip()
        date = minute.find_elements_by_tag_name("a")[0].text.strip()
        url = minute.find_elements_by_tag_name("a")[0].get_attribute('href')
    except: 
        date  = minute.text.strip()
        url = "None"
    
    values = {
        'Date': date, 
        'URL': url,
    }
    
    all_minutes.append(values)

df = pd.DataFrame(all_minutes)


# In[5]:


df.head()


# In[6]:


import datetime as dt


# In[7]:


df['Dates'] = pd.to_datetime(df['Date'], format="%B %d, %Y", errors="coerce")
df = df.dropna(subset=['Dates'])
del df['Date']
df.head()


# ### I did not want to actually flood my computer with PDFs, but 100% understand and can make a loop to click on each of the links in a try except block (to pass the ones with no links).

# ## The PDF OCR thing works fine! 
