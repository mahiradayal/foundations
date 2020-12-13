#!/usr/bin/env python
# coding: utf-8

# # Rock and Mineral Clubs
# 
# Scrape all of the rock and mineral clubs listed at https://rocktumbler.com/blog/rock-and-mineral-clubs/ (but don't just cut and paste!)
# 
# Save a CSV called `rock-clubs.csv` with the name of the club, their URL, and the city they're located in.
# 
# **Bonus**: Add a column for the state. There are a few ways to do this, but knowing that `element.parent` goes 'up' one element might be helpful.
# 
# * _**Hint:** The name of the club and the city are both inside of td elements, and they aren't distinguishable by class. Instead you'll just want to ask for all of the tds and then just ask for the text from the first or second one._
# * _**Hint:** If you use BeautifulSoup, you can select elements by attributes other than class or id - instead of `doc.find_all({'class': 'cat'})` you can do things like `doc.find_all({'other_attribute': 'blah'})` (sorry for the awful example)._
# * _**Hint:** If you love `pd.read_html` you might also be interested in `pd.concat` and potentially `list()`. But you'll have to clean a little more!_

# In[2]:


import pandas as pd
import requests
import time 
from bs4 import BeautifulSoup


# In[3]:


my_url = "https://rocktumbler.com/blog/rock-and-mineral-clubs/"
raw_html = requests.get(my_url).content
soup_doc = BeautifulSoup(raw_html, "html.parser")


# In[4]:


print(soup_doc)


# In[147]:


## Did this before I read the bonus, so I'll let it stay here. 

clubs = soup_doc.find_all('tr', bgcolor='#FFFFFF')

club_list=[]

for club in clubs: 
    name = club.find_all('a')[0].text
    link = club.find_all('a')[0]['href']
    location = club.find_all('td')[1].text
     
    club_list.append({
        'Name' : name, 
        'Link' : link, 
        'Location': location
    })


# In[212]:


sections = soup_doc.find_all('section')[1:]

full_list= []

for section in sections:
    try: 
        name = section.find_all('a')[0].text
        link = section.find_all('a')[0]['href']
        location = section.find_all('td')[2].text
        section_state = section.find_all('h3')[0].text
    except: 
        continue
    
    full_list.append({
        'Name' : name, 
        'Link' : link, 
        'Location': location, 
        'State_Club': section_state
    })

df = pd.DataFrame(full_list)


# In[213]:


df.head()


# In[220]:


df['State'] = df['State_Club'].str.extract(r"^(\w+)", expand=False)
del df['State_Club']

df.head()


# In[221]:


df.to_csv('rock-clubs.csv', index = False)


# In[ ]:




