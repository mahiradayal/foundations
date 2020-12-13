#!/usr/bin/env python
# coding: utf-8

# # North Korean News
# 
# Scrape the North Korean news agency http://kcna.kp
# 
# Save a CSV called `nk-news.csv`. This file should include:
# 
# * The **article headline**
# * The value of **`onclick`** (they don't have normal links)
# * The **article ID** (for example, the article ID for `fn_showArticle("AR0125885", "", "NT00", "L")` is `AR0125885`
# 
# The last part is easiest using pandas. Be sure you don't save the index!
# 
# * _**Tip:** If you're using requests+BeautifulSoup, you can always look at response.text to see if the page looks like what you think it looks like_
# * _**Tip:** Check your URL to make sure it is what you think it should be!_
# * _**Tip:** Does it look different if you scrape with BeautifulSoup compared to if you scrape it with Selenium?_
# * _**Tip:** For the last part, how do you pull out part of a string from a longer string?_
# * _**Tip:** `expand=False` is helpful if you want to assign a single new column when extracting_
# * _**Tip:** `(` and `)` mean something special in regular expressions, so you have to say "no really seriously I mean `(`" by using `\(` instead_
# * _**Tip:** if your `.*` is taking up too much stuff, you can try `.*?` instead, which instead of "take as much as possible" it means "take only as much as needed"_

# In[1]:


import pandas as pd
import requests
import time 
from bs4 import BeautifulSoup


# In[2]:


my_url = "http://kcna.kp/kcna.user.home.retrieveHomeInfoList.kcmsf"
raw_html = requests.get(my_url).content
soup_doc = BeautifulSoup(raw_html, "html.parser")


# In[3]:


print(soup_doc)


# ### h3 and h4 are the two tags that contain article headlines. 

# In[4]:


items = soup_doc.find_all('a', class_='titlebet') 
news = []

for item in items: 
    headlines = item.text.strip()
    click = item['onclick']
     
    news.append({
        'Headline' : headlines, 
        'Onclick' : click
    })
print(news)


# In[5]:


df = pd.DataFrame(news)
df.head()


# In[6]:


df.reset_index(drop=True, inplace=True)


# In[7]:


df['Article_ID'] = df['Onclick'].str.contains(r"fn_showArticle\(\"(\w+)\",*?", na=False)

for article in df['Article_ID']:
     df['Article_ID'] = df['Onclick'].str.extract(r"fn_showArticle\(\"(\w+)\",*?", expand=False)[0]

df.head()


# In[8]:


df.to_csv('nk-news.csv', index = False)

