#!/usr/bin/env python
# coding: utf-8

# # Texas Cosmetologist Violations
# 
# Texas has a system for [searching for license violations](https://www.tdlr.texas.gov/cimsfo/fosearch.asp). You're going to search for cosmetologists!

# ## Setup: Import what you'll need to scrape the page
# 
# We'll be using Selenium for this, *not* BeautifulSoup and requests.

# In[1]:


import pandas as pd
get_ipython().system('pip install html5lib')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# ## Starting your search
# 
# Starting from [here](https://www.tdlr.texas.gov/cimsfo/fosearch.asp), search for **cosmetologist violations** for people with the last name **Nguyen**.

# In[2]:


driver = webdriver.Chrome()


# In[3]:


driver.get("https://www.tdlr.texas.gov/cimsfo/fosearch.asp")


# In[4]:


license_box = driver.find_element_by_id("pht_status")
license_box.click()
license_box.find_element_by_xpath("//option[@value='COS']").click() 
nguyen = driver.find_element_by_id("pht_lnm")
nguyen.send_keys("Nguyen")
submit_button = driver.find_element_by_name("B1")
submit_button.click()


# ## Scraping
# 
# Once you are on the results page, do this.

# ### Loop through each result and print the entire row
# 
# Okay wait, that's a heck of a lot. Use `[:10]` to only do the first ten (`listname[:10]` gives you the first ten).

# In[5]:


rows_ten = driver.find_elements_by_tag_name("tr")[:10]
for row in rows_ten:
    print(row.text)


# ### Loop through each result and print each person's name
# 
# You'll get an error because the first one doesn't have a name. How do you make that not happen?! If you want to ignore an error, you use code like this:
# 
# ```python
# try:
#    # try to do something
# except:
#    # Instead of stopping on an error, it'll jump down here instead
#    print("It didn't work')
# ```
# 
# It should help you out. If you don't want to print anything, you can type `pass` instead of the `print` statement. Most people use `pass`, but it's also nice to print out debug statements so you know when/where it's running into errors.
# 
# **Why doesn't the first one have a name?**

# In[6]:


rows = driver.find_elements_by_tag_name("tr")

for row in rows:
    try:
        name = row.find_elements_by_class_name("results_text")[0]
        print (name.text)
    except:
        print('No name')


# ## Loop through each result, printing each violation description ("Basis for order")
# 
# > - *Tip: You'll get an error even if you're ALMOST right - which row is causing the problem?*
# > - *Tip: You can get the HTML of something by doing `.get_attribute('innerHTML')` - it might help you diagnose your issue.*
# > - *Tip: Or I guess you could just skip the one with the problem...*

# In[38]:


for row in rows:
    try:
        violation = row.find_elements_by_tag_name("td")[2]
        print (violation.text)
    except:
        pass


# In[ ]:





# ## Loop through each result, printing the complaint number
# 
# - TIP: Think about the order of the elements

# In[8]:


for row in rows:
    try:
        complaint = row.find_elements_by_class_name("results_text")[5]
        print (complaint.text)
    except:
        pass


# ## Saving the results
# 
# ### Loop through each result to create a list of dictionaries
# 
# Each dictionary must contain
# 
# - Person's name
# - Violation description
# - Violation number
# - License Numbers
# - Zip Code
# - County
# - City
# 
# Create a new dictionary for each result (except the header).
# 
# > *Tip: If you want to ask for the "next sibling," you can't use `find_next_sibling` in Selenium, you need to use `element.find_element_by_xpath("following-sibling::div")` to find the next div, or `element.find_element_by_xpath("following-sibling::*")` to find the next anything.

# In[9]:


for row in rows:
    try:
        license = row.find_elements_by_class_name("results_text")[4]
    except:
        pass
    try:
        zipcode = row.find_elements_by_class_name("results_text")[3]
    except:
        pass
    try:
        county = row.find_elements_by_class_name("results_text")[2]
    except:
        pass
    try:
        city = row.find_elements_by_class_name("results_text")[1]
    except:
        pass


# In[10]:


results=[]

for row in rows:
    
    dict = {
    'Name': name.text,
    'Violation': violation.text,
    'Violation_Num': complaint.text, 
    'License': license.text,
    'Zip-Code': zipcode.text,
    'County': county.text ,
    'City': city.text,
    }
    results.append(dict)


# ### Save that to a CSV
# 
# - Tip: Use `pd.DataFrame` to create a dataframe, and then save it to a CSV.

# In[11]:


df = pd.DataFrame(results)


# In[12]:


df.to_csv('results.csv', index = False)


# ### Open the CSV file and examine the first few. Make sure you didn't save an extra weird unnamed column.

# In[13]:


pd.read_csv('results.csv', nrows=20)  


# ## Let's do this an easier way
# 
# Use Selenium and `pd.read_html` to get the table as a dataframe.

# In[14]:


tables = pd.read_html('results.csv')
df_easy = pd.DataFrame(tables)


# In[ ]:




