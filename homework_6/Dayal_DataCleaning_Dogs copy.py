#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd
import numpy as np


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", nrows=30000)
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[3]:


index = df.index
print(len(index))


# In[4]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[5]:


# Each row is a different dog. Owner zip code is where the dog's owner lives, Spayed or Neutered shows whether the dog has been spayed or neutered.


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# In[6]:


# Are the dogs only M and F or are there some that haven't been categorized? 
# how many missing records are there for Animal Third Color? 
# How many dogs are over 10 years old? 
# How many licenses are expiring in the next 6 months? 


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[7]:


df.columns = df.columns.str.replace(' ', '_')
df.groupby("Primary_Breed").Primary_Breed.count().sort_values(ascending=False).head(10).plot(kind='barh')


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[8]:


df.groupby("Primary_Breed").Primary_Breed.count().sort_values(ascending=False).head(11)[1:].plot(kind='barh')


# ## What are the most popular dog names?

# In[9]:


df.columns = df.columns.str.replace(' ', '_')
df.groupby("Animal_Name").Animal_Name.count().sort_values(ascending=False).head(20)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[10]:


df.columns = df.columns.str.replace(' ', '_')
df[df.Animal_Name == "Mahira"]


# In[11]:


df[df.Animal_Name == "Max"].Animal_Name.count()


# In[12]:


df[df.Animal_Name == "Maxwell"].Animal_Name.count()


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[13]:


df.Guard_or_Trained.value_counts(normalize=True, dropna=True)*100


# ## What are the actual numbers?

# In[14]:


df.Guard_or_Trained.value_counts(dropna=True)


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[61]:


df.Guard_or_Trained.value_counts(dropna= False)
#The other dogs aren't a yes or no and we find them under NaN. 


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[68]:


df.Guard_or_Trained.fillna("No", inplace = True)

df.Guard_or_Trained.head(10)


# ## What are the top dog breeds for guard dogs? 

# In[69]:


df[df.Guard_or_Trained == "Yes"].groupby('Primary_Breed').Primary_Breed.value_counts().sort_values(ascending=False).head(5)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[76]:


df["Year"] =     df['Animal_Birth'].apply(lambda birth: birth.year)
    


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[ ]:


df["Age"] =     2020-df.Year


# In[ ]:


df.Age.mean()


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[32]:


dy = pd.read_csv("zipcodes-neighborhoods.csv", nrows=30000)
dy = dy.merge(df, left_on="zip", right_on="Owner_Zip_Code")
dy.head(5)


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[33]:


#dy.groupby("borough").Animal_Name.count().sort_values(ascending=False).head(50)


dy[(dy.Animal_Name != "Unknown")].groupby("borough").Animal_Name.value_counts().groupby(level=0).nlargest(1)


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[103]:


dy[(dy.Primary_Breed != "Unknown")].groupby("neighborhood").Primary_Breed.value_counts().groupby(level=0).nlargest(1)


# In[ ]:





# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[28]:


dy[(dy.Primary_Breed != "Unknown")].groupby("Primary_Breed").Spayed_or_Neut.count().sort_values()


# In[29]:


dy[(dy.Primary_Breed != "Unknown")].groupby("Animal_Gender").Spayed_or_Neut.count().sort_values()


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[93]:



colors = dy.isin({"Animal_Dominant_Color": ["BLACK", "WHITE", "GREY"], "Animal_Secondary_Color": ["BLACK", "WHITE", "GREY"], "Animal_Third_Color": ["BLACK", "WHITE", "GREY"]})

df["monochrome"] =  colors.apply(lambda dog: dog["Animal_Dominant_Color"]== True | dog["Animal_Secondary_Color"]== True | dog["Animal_Third_Color"]== True , axis=1)

df.head(5) 


# ## How many dogs are in each borough? Plot it in a graph.

# In[30]:


dy.groupby('borough').borough.value_counts().plot(kind="barh")


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[162]:


dz = pd.read_csv("boro_population.csv", nrows=30000)
dz = dz.merge(dy, left_on="borough", right_on="borough")

total = dz.groupby('borough').population.count()/dy.groupby('borough').borough.count()
print (total)


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[106]:


dy[(dy.Primary_Breed != "Unknown")].groupby("borough").Primary_Breed.value_counts().groupby(level=0).nlargest(5).plot(kind='barh')


# ## What percentage of dogs are not guard dogs?

# In[157]:


# Number of dogs = 30000
index = df.index
number_dogs = (len(index))

df[df.Guard_or_Trained == "No"].Guard_or_Trained.value_counts()
# Not guard dogs = 29983 

# Percentage = 

print((29983/30000)*100)


# In[ ]:




