#!/usr/bin/env python
# coding: utf-8

# # Cryptocurrency prices
# 
# * **Filename:**  `cryptocurrencies.csv`
# * **Description:** Cryptocurrency prices for a handful of coins over time.
# * **Source:** https://coinmarketcap.com/all/views/all/ but from a million years ago (I cut and pasted, honestly)
# 
# ### Make a chart of bitcoin's high, on a weekly basis
# 
# You might want to do the cherry blossoms homework first, or at least read the part about `format=` and `pd.to_datetime`.
# 
# *Yes, that's the entire assignment. It isn't an exciting dataset, but it's just dirty enough to make charting this a useful experience.*

# In[1]:


import pandas as pd


# In[2]:


df = pd.read_csv("/Users/mahiradayal/computing/hw-8/cryptocurrency/cryptocurrencies.csv")
df


# In[3]:


import datetime as dt


# In[4]:


df['date'] = pd.to_datetime(df.date, format="%d-%b-%y", errors="coerce").dropna()
df.date


# In[5]:


df['week'] = df.date.dt.strftime("%W")
df.week.sort_values().head(-5)


# In[6]:


df['high']=df['high'].str.replace(',','')
df.high.head()


# In[29]:


df["high"]=df["high"].astype(float)


# In[30]:


df.dtypes


# In[31]:


df.groupby('week').high.agg('max').plot(y='week', x ='max', kind='barh', figsize = (10,10))


# In[ ]:




