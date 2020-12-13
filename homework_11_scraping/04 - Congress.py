#!/usr/bin/env python
# coding: utf-8

# # Scraping one page per row
# 
# Let's say we're interested in our members of Congress, because who isn't? Read in `congress.csv`.

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


df = pd.read_csv("congress.csv")


# # Let's scrape one
# 
# The `slug` is the part of the URL that's particular to that member of Congress. So `/james-abdnor/A000009` really means `https://www.congress.gov/member/james-abdnor/A000009`.
# 
# Scrape his name, birthdaye, party, whether he's currently in congress, and his bill count (don't worry if the bill count is dirty, you can clean it up later).

# In[3]:


my_url = "https://www.congress.gov/member/james-abdnor/A000009"
raw_html = requests.get(my_url).content
soup_doc = BeautifulSoup(raw_html, "html.parser")


# In[4]:


print(soup_doc)


# In[5]:


details = soup_doc.find_all('div', class_='featured')

name = details[0].find_all('h1')[0].contents[0]

birthdate = details[0].find_all('h1')[0].find_all('span')[0].text.strip()

party = soup_doc.find_all('div', class_="overview-member-column-profile member_profile")[0].find_all('td')[0].text.strip()

bills = soup_doc.find_all('span', class_='results-number')[0].text.strip()

all_details = {
    'Name': name, 
    'Year': birthdate, 
    'Party': party, 
    'Bills_messy': bills
}

print(all_details)


# # Build a function
# 
# Write a function called `scrape_page` that makes a URL out of the the `slug`, like we're going to use `.apply`.

# In[40]:


df.head() 


# In[7]:


def scrape_page(df):
    return df.apply(lambda x:'%s%s' % ("https://www.congress.gov/member/",x['slug']),axis=1)

scrape_page(df)


# # Do the scraping
# 
# Rewrite `scrape_page` to actually scrape the URL. You can use your scraping code from up above. Start by testing with just one row (I put a sample call below) and then expand to your whole dataframe.
# 
# Save the results as `scraped_df`.
# 
# * **Hint:** Be sure to use `return`!
# * **Hint:** Make sure you return a `pd.Series`

# In[31]:


def scrape_page(row):
    
    my_url =  ('%s%s' % ("https://www.congress.gov/member/", row['slug']))    
    raw_html = requests.get(my_url).content
    soup_doc = BeautifulSoup(raw_html, "html.parser")
    
    member = soup_doc.find('div', class_='container')

    featured = member.find('div', class_='featured')

    name = featured.find('h1').contents[0]

    birthdate = featured.find('span', class_='birthdate').text.strip()

    party = member.find('div', class_="overview-member-column-profile member_profile").find('td').text.strip()

    bills = member.find('span', class_='results-number').text.strip()
    
    result = pd.Series([name, birthdate, party, bills], index =['Name', 'Year', 'Party', 'Bills'])

    return(result)


# In[32]:


# Test with this
scrape_page({'slug': 'neil-abercrombie/A000014'})


# In[37]:


all_names = df.apply(lambda x: scrape_page(x), axis = 1)
joined_table = df.join(all_names, rsuffix='_scraped')


# In[38]:


joined_table


# ## Join with your original dataframe
# 
# Join your new data with your original data, adding the `_scraped` suffix on the new columns. You can use either `.join` or `.merge`, but be sure to read the docs to know the difference!

# ### Did my join up there ^ I would move it but that took HOURS to run and I refuse to touch it ever again 

# ## Save it
# 
# Save your combined results to `congress-plus-scraped.csv`.

# In[42]:


df_joined = pd.DataFrame(joined_table)
df_joined.head()


# In[82]:


df_joined['Bill_Count'] = df_joined['Bills'].str.extract(r"\w* of (.*)", expand=False)
del df_joined['Bills']

df_joined.head(2)


# In[83]:


df_joined.to_csv('congress-plus-scraped.csv', index = False)


# In[ ]:




