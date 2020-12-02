#!/usr/bin/env python
# coding: utf-8

# # Scraping basics for Selenium
# 
# If you feel comfortable with scraping, you're free to skip this notebook.

# ## Part 0: Imports
# 
# Import what you need to use Selenium, and start up a new Chrome to use for scraping. You might want to copy from the [Selenium snippets](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-snippets/) page.
# 
# **You only need to do `driver = webdriver.Chrome()` once,** every time you do it you'll open a new Chrome instance. You'll only need to run it again if you close the window (or want another Chrome, for some reason).

# In[90]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
get_ipython().system('pip install lxml')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# In[4]:


driver = webdriver.Chrome()


# In[5]:


driver.get("http://jonathansoma.com/lede/static/by-class.html")


# ## Part 1: Scraping by class
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-class.html, printing out the title, subhead, and byline.

# In[20]:


titles = driver.find_elements_by_class_name("title")
for title in titles: 
    print(title.text.strip())


# In[21]:


subheads = driver.find_elements_by_class_name("subhead")
for subhead in subheads:
    print(subhead.text.strip())


# In[22]:


bylines = driver.find_elements_by_class_name("byline")
for byline in bylines:
    print(byline.text.strip())


# ## Part 2: Scraping using tags
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-tag.html, printing out the title, subhead, and byline.

# In[18]:


titles = driver.find_elements_by_tag_name("h1")
for title in titles:
    print(title.text.strip())


# In[17]:


subheads = driver.find_elements_by_tag_name("h3")
for subhead in subheads:
    print(subhead.text.strip())


# In[19]:


bylines = driver.find_elements_by_tag_name("p")
for byline in bylines:
    print(byline.text.strip())


# ## Part 3: Scraping using a single tag
# 
# Scrape the content at http://jonathansoma.com/lede/static/by-list.html, printing out the title, subhead, and byline.
# 
# > **This will be important for the next few:** if you scrape multiples, you have a list. Even though it's Seleninum, you can use things like `[0]`, `[1]`, `[-1]` etc just like you would for a normal list.

# In[62]:


contents = driver.find_elements_by_tag_name("body")
content = contents[0]
content.text.split("\n")[0]


# In[63]:


contents = driver.find_elements_by_tag_name("body")
content = contents[0]
content.text.split("\n")[1]


# In[64]:


contents = driver.find_elements_by_tag_name("body")
content = contents[0]
content.text.split("\n")[2]


# ## Part 4: Scraping a single table row
# 
# Scrape the content at http://jonathansoma.com/lede/static/single-table-row.html, printing out the title, subhead, and byline.

# In[82]:


driver.get("http://jonathansoma.com/lede/static/single-table-row.html")


# In[152]:


title = driver.find_elements_by_tag_name('td')[0].text
print (title)


# In[154]:


subhead = driver.find_elements_by_tag_name('td')[1].text
print (subhead)


# In[153]:


byline = driver.find_elements_by_tag_name('td')[2].text
print (byline)


# ## Part 5: Saving into a dictionary
# 
# Scrape the content at http://jonathansoma.com/lede/static/single-table-row.html, saving the title, subhead, and byline into a single dictionary called `book`.
# 
# > Don't use pandas for this one!

# In[157]:


book = {
    'title': title,
    'subhead': subhead,
    'byline': byline
}


# ## Part 6: Scraping multiple table rows
# 
# Scrape the content at http://jonathansoma.com/lede/static/multiple-table-rows.html, printing out each title, subhead, and byline.
# 
# > You won't use pandas for this one, either!

# In[158]:


driver.get("http://jonathansoma.com/lede/static/multiple-table-rows.html")


# In[194]:


table_rows = driver.find_elements_by_tag_name('tr')
for table_row in table_rows: 
    tds = table_row.find_elements_by_tag_name("td")
    book = {
        'title': tds[0].text, 
        'subhead': tds[1].text,
        'byline': tds[2].text
    }
    print(book)


# ## Part 7: Scraping an actual table
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html, creating a list of dictionaries.
# 
# > Don't use pandas here, either!

# In[183]:


driver.get("http://jonathansoma.com/lede/static/the-actual-table.html")


# In[199]:


table_rows = driver.find_elements_by_tag_name('tr')
for table_row in table_rows: 
    tds = table_row.find_elements_by_tag_name("td")
    book = {
        'title': tds[0].text, 
        'subhead': tds[1].text,
        'byline': tds[2].text
    }
    book_list= [book]
    print(book_list)


# ## Part 8: Scraping multiple table rows into a list of dictionaries
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html, creating a pandas DataFrame.
# 
# > There are two ways to do this one! One uses just pandas, the other one uses the result from Part 7.

# In[211]:


book_list = []
table_rows = driver.find_elements_by_tag_name('tr')
for table_row in table_rows: 
    tds = table_row.find_elements_by_tag_name("td")
    book = {
        'title': tds[0].text, 
        'subhead': tds[1].text,
        'byline': tds[2].text
    }
    book_list.append(book)
print(book_list)
df = pd.DataFrame(book_list)


# In[213]:


df.head()


# ## Part 9: Scraping into a file
# 
# Scrape the content at http://jonathansoma.com/lede/static/the-actual-table.html and save it as `output.csv`

# In[219]:


df.to_csv('output.csv', index = False)

