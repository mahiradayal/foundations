#!/usr/bin/env python
# coding: utf-8

# # Texas Tow Trucks (`.apply` and `requests`)
# 
# We're going to scrape some [tow trucks in Texas](https://www.tdlr.texas.gov/tools_search/).

# ## Import your imports

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


driver.get("https://www.tdlr.texas.gov/tools_search/")


# ## Search for the TLDR Number `006565540C`, and scrape the information on that company
# 
# Using [license information system](https://www.tdlr.texas.gov/tools_search/), find information about the tow truck number above, displaying the
# 
# - The business name
# - Owner/operator
# - Phone number
# - License status (Active, Expired, Etc)
# - Physical address
# 
# If you can't figure a 'nice' way to locate something, your two last options might be:
# 
# - **Find a "parent" element, then dig inside**
# - **Find all of a type of element** (like we did with `td` before) and get the `[0]`, `[1]`, `[2]`, etc
# - **XPath** (inspect an element, Copy > Copy XPath)
# 
# These kinds of techniques tend to break when you're on other result pages, but... maybe not! You won't know until you try.
# 
# > - *TIP: When you use xpath, you CANNOT use double quotes or Python will get confused. Use single quotes.*
# > - *TIP: You can clean your data up if you want to, or leave it dirty to clean later*
# > - *TIP: The address part can be tough, but you have a few options. You can use a combination of `.split` and list slicing to clean it now, or clean it later in the dataframe with regular expressions. Or other options, too, probably*

# In[4]:


button = driver.find_element_by_id("mcrbutton")
button.click()
type_tdlr = driver.find_element_by_id("mcrdata")
type_tdlr.send_keys("006565540C")
search_button = driver.find_element_by_id("submit3")
search_button.click()


# In[5]:


trucks = driver.find_element_by_id("t1").find_elements_by_tag_name("table")

name = trucks[2].find_elements_by_tag_name("tr")[1].find_element_by_tag_name("td").text.strip()

owner = trucks[2].find_elements_by_tag_name("tr")[2].find_element_by_tag_name("td").text.strip()

phone = trucks[2].find_elements_by_tag_name("tr")[3].find_element_by_tag_name("td").text.strip()

license = trucks[3].find_elements_by_tag_name("td")[1].text.strip()

address = trucks[3].find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")[1].text.strip()

messy_details = {
    'Company Name': name, 
    'Owner': owner, 
    'Phone': phone,
    'Status': license,
    'Address': address
}

print(messy_details)


# # Adapt this to work inside of a single cell
# 
# Double-check that it works. You want it to print out all of the details.

# ### I did it in a single cell! 

# # Using .apply to find data about SEVERAL tow truck companies
# 
# The file `trucks-subset.csv` has information about the trucks, we'll use it to find the pages to scrape.
# 
# ### Open up `trucks-subset.csv` and save it into a dataframe

# In[6]:


df = pd.read_csv("trucks-subset.csv")


# ## Go through each row of the dataset, displaying the URL you will need to scrape for the information on that row
# 
# You don't have to actually use the search form for each of these - look at the URL you're on, it has the number in it!
# 
# For example, one URL might look like `https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber=006565540C`.
# 
# - *TIP: Use .apply and a function*
# - *TIP: You'll need to build this URL from pieces*
# - *TIP: You probably don't want to `print` unless you're going to fix it for the next question 
# - *TIP: pandas won't showing you the entire url! Run `pd.set_option('display.max_colwidth', None)` to display aaaalll of the text in a cell*

# In[7]:


df.head()


# In[34]:


def make_url(row):
    tdlr = row['TDLR Number']
    url = '%s%s' % ("https://www.tdlr.texas.gov/tools_search/mccs_display.asp?mcrnumber=",tdlr)
    return pd.Series([url], index = ['url'])


# ### Save this URL into a new column of your dataframe, called `url`
# 
# - *TIP: Use a function and `.apply`*
# - *TIP: Be sure to use `return`*

# In[19]:


df['url'] = df.apply(lambda row: make_url(row), axis=1)
pd.set_option('display.max_colwidth', None)


# In[17]:


df.head()


# ## Go through each row of the dataset, printing out information about each tow truck company.
# 
# Now will be **scraping** inside of your function.
# 
# - The business name
# - Owner/operator
# - Phone number
# - License status (Active, Expired, Etc)
# - Physical address
# 
# Just print it out for now.
# 
# - *TIP: use .apply*
# - *TIP: You'll be using the code you wrote before, but converted into a function*
# - *TIP: Remember how the TDLR Number is in the URL? You don't need to do the form submission if you don't want!*
# - *TIP: Make sure you adjust any variables so you don't scrape the same page again and again*

# In[20]:


for weblink in df['url']: 
    
    my_url = weblink
    driver.get(my_url)
    
    trucks = driver.find_element_by_id("t1").find_elements_by_tag_name("table")

    name = trucks[2].find_elements_by_tag_name("tr")[1].find_element_by_tag_name("td").text.strip()
    
    owner = trucks[2].find_elements_by_tag_name("tr")[2].find_element_by_tag_name("td").text.strip()
    
    phone = trucks[2].find_elements_by_tag_name("tr")[3].find_element_by_tag_name("td").text.strip()
    
    license = trucks[3].find_elements_by_tag_name("td")[1].text.strip()
    
    address = trucks[3].find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")[1].text.strip()

    messy_details = {
        'Company Name': name, 
        'Owner': owner, 
        'Phone': phone,
        'Status': license,
        'Address': address
    }

    print(messy_details)


# ## Scrape the following information for each row of the dataset, and save it into new columns in your dataframe.
# 
# - The business name
# - Owner/operator
# - Phone number
# - License status (Active, Expired, Etc)
# - Physical address
# 
# It's basically what we did before, but using the function a little differently.
# 
# - *TIP: Same as above, but you'll be returning a `pd.Series` and the `.apply` line is going to be a lot longer*
# - *TIP: Save it to a new dataframe!*
# - *TIP: Make sure you change your `df` variable names correctly if you're cutting and pasting - there are a few so it can get tricky*

# In[35]:


def make_list(row):
        
    my_url = row['url']
                
    driver.get(my_url)

    trucks = driver.find_element_by_id("t1").find_elements_by_tag_name("table")

    name = trucks[2].find_elements_by_tag_name("tr")[1].find_element_by_tag_name("td").text.strip()

    owner = trucks[2].find_elements_by_tag_name("tr")[2].find_element_by_tag_name("td").text.strip()

    phone = trucks[2].find_elements_by_tag_name("tr")[3].find_element_by_tag_name("td").text.strip()

    license = trucks[3].find_elements_by_tag_name("td")[1].text.strip()

    address = trucks[3].find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("td")[1].text.strip()

    result = pd.Series([name, owner, phone, license, address], index =['Name', 'Owner', 'Phone', 'License_status', 'Address'])
        
    return(result)


# In[36]:


all_trucks = df.apply(lambda x: make_list(x), axis = 1)


# In[37]:


all_trucks


# ### Save your dataframe as a CSV named `tow-trucks-extended.csv`

# In[27]:


df2 = pd.DataFrame(all_trucks)

df2.to_csv('tow-trucks-extended.csv', index = False)


# ### Re-open your dataframe to confirm you didn't save any extra weird columns

# ### I didn't clean it with Regex to get rid of the titles before each item but works fine otherwise: 

# In[28]:


df2 = pd.read_csv("tow-trucks-extended.csv")
df2.head()


# ## Process the entire `tow-trucks.csv` file
# 
# We just did it on a short subset so far. Now try it on all of the tow trucks. **Save as the same filename as before**

# In[29]:


df2 = pd.read_csv("tow-trucks.csv")


# In[41]:


df2['url'] = df2.apply(lambda row: make_url(row), axis=1)
all_df2 = df.apply(lambda x: make_list(x), axis = 1)


# In[43]:


df2.to_csv('tow-trucks-extended.csv', index = False)

