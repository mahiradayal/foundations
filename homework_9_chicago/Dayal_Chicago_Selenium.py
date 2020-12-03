#!/usr/bin/env python
# coding: utf-8

# ## Logging on
# 
# Use Selenium to visit https://webapps1.chicago.gov/buildingrecords/ and accept the agreement.
# 
# > Think about when you use `.find_element_...` and when you use `.find_elementSSS_...`

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


driver = webdriver.Chrome()


# In[3]:


driver.get("https://webapps1.chicago.gov/buildingrecords/")


# In[4]:


agree = driver.find_element_by_id("rbnAgreement1")
agree.click()
submit_button = driver.find_element_by_id("submit")
submit_button.click()


# ## Searching
# 
# Search for **400 E 41ST ST**.

# In[5]:


address = driver.find_element_by_id("fullAddress")
address.send_keys("400 E 41ST ST")


# In[6]:


submit = driver.find_element_by_id("submit")
submit.click()


# ## Saving tables with pandas
# 
# Use pandas to save a CSV of all **permits** to `Permits - 400 E 41ST ST.csv`. Note that there are **different sections of the page**, not just one long permits table.

# ## Help! 
# How do I use pandas without a URL? Does with pandas just mean the SAVING part? I made a dictionary and used Selenium. 

# In[7]:


rows = driver.find_elements_by_tag_name("tr")[:33]

results = []

for row in rows:
    try:
        permit = row.find_elements_by_tag_name("td")[0]
        date = row.find_elements_by_tag_name("td")[1]
        descr = row.find_elements_by_tag_name("td")[2]
    except:
        continue 
        
    permits = {
        'Permit': permit.text, 
        'Date': date.text,
        'Description': descr.text
    }
    results.append(permits)
print(results)


# In[8]:


df = pd.DataFrame(results)
df.to_csv('Permits - 400 E 41ST ST.csv', index = False)


# ## Saving tables the long way
# 
# Save a CSV of all DOB inspections to `Inspections - 400 E 41ST ST.csv`, but **you also need to save the URL to the inspection**. As a result, you won't be able to use pandas, you'll need to use a loop and create a list of dictionaries.
# 
# You can use Selenium (my recommendation) or you can feed the source to BeautifulSoup. You should have approximately 157 rows.
# 
# You'll probably need to find the table first, then the rows inside, then the cells inside of each row. You'll probably use lots of list indexing. I might recommend XPath for finding the table.
# 
# *Tip: If you get a "list index out of range" error, it's probably due to an issue involving `thead` vs `tbody` elements. What are they? What are they for? What's in them? There are a few ways to troubleshoot it.*

# In[9]:


items = driver.find_elements_by_tag_name("tr")[37:193]

rows = []
for item in items:
    tds = item.find_elements_by_tag_name("td")
    insp = tds[0]
    url = tds[0].find_element_by_tag_name("a").get_attribute('href')
    date = tds[1]
    status = tds[2]
    descr = tds[3]
 
        
    row = {
        'insp': insp.text, 
        'url': url,
        'date': date.text, 
        'status': status.text, 
        "description": descr.text
    }
    
    rows.append(row)
print(rows)


# In[10]:


dob = pd.DataFrame(rows)
dob.to_csv('Inspections - 400 E 41ST ST.csv', index = False)


# In[11]:


dob.head(5)


# ### Loopity loops
# 
# > If you used Selenium for the last question, copy the code and use it as a starting point for what we're about to do!
# 
# If you click the inspection number, it'll open up a new window that shows you details of the violations from that visit. Count the number of violations for each visit and save it in a new column called **num_violations**.
# 
# Save this file as `Inspections - 400 E 41ST ST - with counts.csv`.
# 
# Since it opens in a new window, we have to say "Hey Selenium, pay attention to that new window!" We do that with `driver.switch_to.window(driver.window_handles[-1])` (each window gets a `window_handle`, and we're just asking the driver to switch to the last one.). A rough sketch of what your code will look like is here:
# 
# ```python
# # Click the link that opens the new window
# 
# # Switch to the new window/tab
# driver.switch_to.window(driver.window_handles[-1])
# 
# # Do your scraping in here
# 
# # Close the new window/tab
# driver.close()
# 
# # Switch back to the original window/tab
# driver.switch_to.window(driver.window_handles[0])
# ```
# 
# You'll want to play around with them individually before you try it with the whole set - the ones that pass are very different pages than the ones with violations! There are a few ways to get the number of violations, some easier than others.

# In[12]:


## Chrome hates me and it doesn't let me do more than a couple at a time - so here it is for part of the list. 
## I can do more when I expand the list range! 

items = driver.find_elements_by_tag_name("tr")[37:60]

rows = []

for item in items:
    
    tds = item.find_elements_by_tag_name("td")
    insp = tds[0]
    url = tds[0].find_element_by_tag_name("a").get_attribute('href')
    date = tds[1]
    status = tds[2]
    descr = tds[3]

    row = {
        'insp': insp.text, 
        'url': url,
        'date': date.text, 
        'status': status.text, 
        "description": descr.text
    }
    
    if url is None: 
        continue  
    
    tds[0].click()
    
    time.sleep(0.5)
    
    driver.switch_to.window(driver.window_handles[-1])
    
    items_2 = driver.find_elements_by_tag_name("tr")
    
    row['num_violations'] = len(items_2)
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    rows.append(row)


# In[17]:


new_dob = pd.DataFrame(rows)
new_dob.to_csv('Inspections - 400 E 41ST ST - with counts.csv', index = False)


# In[ ]:





# In[ ]:





# In[ ]:




