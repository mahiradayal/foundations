#!/usr/bin/env python
# coding: utf-8

# # Texas Licenses
# 
# I originally got this dataset from the [License Files page](https://www.license.state.tx.us/licensesearch/licfile.asp) from the Texas Department of Licensing and Regulation, but they've changed around since then! I'm pretty sure it's [this dataset](https://www.opendatanetwork.com/dataset/data.texas.gov/7358-krk7), but we'll just use a local version instead of the most current.

# # PART ONE: OPENING UP OUR DATASET

# ## 0. Do your setup
# 
# Import what you need to import, etc.

# In[1]:


import pandas as pd


# ## 1. Open the file
# 
# We'll start with `licfile.csv`, which is a list of licenses.

# In[2]:


df = pd.read_csv("/Users/mahiradayal/computing/hw-8/licensing/licfile.csv")
df.head(5)


# ## 2. That looks terrible, let's add column names.
# 
# It apparently doesn't have headers! **Read the file in again, but setting your own column names**. Their [current data dictionary might not perfectly match](https://www.opendatanetwork.com/dataset/data.texas.gov/7358-krk7), but you can use it to understand what the columns are. For the dataset we're using, the order goes like this:
# 
# * LICTYPE
# * LICNUMBER
# * BIZCOUNTY
# * BIZNAME
# * BIZLINE1
# * BIZLINE2
# * BIZCITYSTATE
# * BIZTELEPHONE
# * EXPIRATION
# * OWNER
# * MAILLINE1
# * MAILLINE2
# * MAILCITYSTATE
# * MAILCOUNTYCODE
# * MAILCOUNTY
# * MAILZIP
# * TELEPHONE
# * LICSUBTYPE
# * CEFLAG
# 
# **Note:** You can rename the columns to things that make sense - "expiration" is a little more manageable than "LICENSE EXPIRATION DATE (MMDDCCYY)". I've named my License Type column LICTYPE, so if you haven't you'll have to change the rest of my sample code to match.

# In[3]:


col_names=["LICTYPE", "LICNUMBER", "BIZCOUNTY", "BIZNAME", "BIZLINE1", "BIZLINE2", "BIZCITYSTATE", "BIZTELEPHONE", "EXPIRATION", "OWNER", "MAILLINE1", "MAILLINE2", "MAILCITYSTATE", "MAILCOUNTYCODE", "MAILCOUNTY", "MAILZIP", "TELEPHONE", "LICSUBTYPE", "CEFLAG"]
df = pd.read_csv("/Users/mahiradayal/computing/hw-8/licensing/licfile.csv", names=col_names)


# # 3. Force string columns to be strings
# 
# The county code and expiration dates are being read in as numbers, which is going to cause some trouble later on. You can force a column to be a certain type (most usually strings) when reading it in with the following code:
# 
#     df = pd.read_csv("your-filename.csv", dtype={"colname1": str, "colname2": str})
# 
# You don't need to do it for every column, just the ones you want to force!
# 
# **Re-import the file, forcing the expiration date, license number, mailing address county code, mailing zip code and telephone to all be strings.**

# In[4]:


df = pd.read_csv("/Users/mahiradayal/computing/hw-8/licensing/licfile.csv", names=col_names, dtype={"EXPIRATION": str, "LICNUMBER": str, "MAILCOUNTYCODE": str, "MAILZIP": str, "TELEPHONE": str})


# Check the data types of your columns to be sure! If you do it right they'll be `object` (not `str`, oddly).

# In[5]:


df.dtypes


# ## 4. Convert those expiration dates from MMDDYYYY to YYYY-MM-DD
# 
# You can use list slicing with `.str` (we did `dt.per_name.str[:4]` for the home data stuff once), `pd.to_datetime`, or a hundred other methods.

# In[6]:


df['EXPIRATION'] = pd.to_datetime(df.EXPIRATION, format= "%d%m%Y", errors="coerce")


# Check the first five expirations to make sure they look right.

# In[7]:


df.EXPIRATION.head(5)


# # PART TWO: LOOKING AT LICENSES

# ## 5. What are the top 10 most common licenses?

# In[8]:


df.groupby('LICTYPE').LICTYPE.value_counts().sort_values(ascending=False).head(10)


# ## 6. What are the top 10 least common?

# In[9]:


df.groupby('LICTYPE').LICTYPE.value_counts().sort_values().head(10)


# ## 7. Try to select everyone who is any type of electrician.
# 
# You're going to get an error about `"cannot index with vector containing NA / NaN values"`. Let's work our way in there.

# In[10]:


df[df['LICTYPE'].str.contains("Electrician", na=False)]


# ## 8. How many of the rows of LICTYPE are NaN?

# In[11]:


df.LICTYPE.isnull().sum(axis = 0)


# In[12]:


#Just checking
len(df.LICTYPE)


# Over 7000 licenses don't have types! As a result, when we look for license types with electricians - aka do `df['LICTYPE'].str.contains("Electrician")` - we get three results:
# 
# * `True` means `LICTYPE` exists and contains `"Electrician"`
# * `False` means `LICTYPE` exists and does not contain `"Electrician"`
# * `NaN` means `LICTYPE` does not exist for that row

# ## 9. Actually getting everyone who is an electrician

# In[13]:


electrician = df[df['LICTYPE'].str.contains("Electrician").eq(True)]
electrician.head()


# This doesn't work when trying to select electricians, though, as NaN is a no-go for a filter. We *could* filter out everywhere the LICTYPE is null, but we could also cheat a little and say "replace all of the `NaN` values with `False` values."
# 
# `.fillna(False)` will take every `NaN` and replace it with `False`. 

# In[14]:


df['LICTYPE'] = df.LICTYPE.fillna(False)


# ## 10. What's the most popular kind of electrician?

# In[15]:


electrician.groupby('LICTYPE').LICTYPE.value_counts().sort_values(ascending=False).head(1)


# ## 11. Graph it, with the largest bar on top.

# In[16]:


electrician.groupby('LICTYPE').LICTYPE.value_counts().sort_values().plot(kind='barh')


# ## 12. How many sign electricians are there?
# 
# There are a few ways to do this one.

# In[17]:


electrician[electrician['LICTYPE'].str.contains("Sign").eq(True)].LICTYPE.count()


# # PART THREE: LOOKING AT LAST NAMES

# ## 13. Extract every owner's last name
# 
# You want everything before the comma. We've done this before (in a few different ways!).
# 
# * **Hint:** If you get an error about missing or `NaN` data, you might use `.fillna('')` to replace every empty owner name with an empty string. This might not happen to you, though, depending on how you do it!
# 
# * **Hint:** You probably want to do `expand=False` on your extraction to make sure it comes out as a series instead of a dataframe.

# In[18]:


df['OWNER'] = df.OWNER.fillna('')


# In[19]:


df.OWNER.head(5)


# In[20]:


df['LASTNAME'] = df.OWNER.dropna().str.split(',').str[0]


# ## 14. Save the last name into a new column
# 
# Then check to make sure it exists, and you successfully saved it into the dataframe.

# In[21]:


df['LASTNAME'] = df.OWNER.dropna().str.split(',').str[0]


# In[22]:


df.head(5)


# # 15. What are the ten most popular last names?

# In[23]:


df.groupby('LASTNAME').LASTNAME.value_counts().sort_values(ascending=False).head(10)


# ## 16. What are the most popular licenses for people with the last name Nguyen? Tran? Le?
# 
# Those are the top 3 last names in Vietnam.

# In[24]:


df[df.LASTNAME == 'NGUYEN'].groupby('LICTYPE').LICTYPE.value_counts().sort_values(ascending=False).head(5)


# In[25]:


df[df.LASTNAME == 'TRAN'].groupby('LICTYPE').LICTYPE.value_counts().sort_values(ascending=False).head(5)


# In[26]:


df[df.LASTNAME == 'LE'].groupby('LICTYPE').LICTYPE.value_counts().sort_values(ascending=False).head(5)


# The background of this [is interesting](https://www.npr.org/2019/05/19/724452398/how-vietnamese-americans-took-over-the-nails-business-a-documentary) and [tragic](https://www.nytimes.com/2015/05/10/nyregion/at-nail-salons-in-nyc-manicurists-are-underpaid-and-unprotected.html).

# ## 17. Now do all of that in one line - most popular licenses for Nguyen, Tran and Le - without using `&`

# In[27]:


df[df.LASTNAME.isin(["NGUYEN", "TRAN", "LE"])].groupby('LICTYPE').LICTYPE.value_counts().sort_values(ascending=False).head(5)


# ## 19. Most popular license for anyone with a last name that ENDS in `-ko`
# 
# The answer is not `.str.contains('ko')`, but it isn't necessarily too different.
# 
# * One way involves a `.str.` method that check if a string ends with something,
# * the other way involves a regular expression that has a "end of the string" marker (similar to how we've used `^` for the start of a string before)
# 
# If you're thinking about the latter, I might take a look at [this page](http://www.rexegg.com/regex-quickstart.html) under "Anchors and Boundaries". 

# In[28]:


df['KO'] = df.LASTNAME.str.endswith('KO', na=False)
POP_KO = df[df.KO == True].groupby('LICTYPE').LICTYPE.value_counts().sort_values(ascending=False).head(1)
POP_KO


# ## 20. Get that as a percentage

# In[29]:


TOTAL = df[df.KO == True].groupby('LICTYPE').LICTYPE.value_counts().sum()
PERCENTAGE = (POP_KO/TOTAL)*100
print(round(PERCENTAGE))


# # PART FOUR: LOOKING AT FIRST NAMES

# ## 21. Extract the owner's first name
# 
# First, a little example of how regular expressions work with pandas.

# In[30]:


# Build a dataframe
sample_df = pd.DataFrame([
    { 'name': 'Mary', 'sentence': "I am 90 years old" },
    { 'name': 'Jack', 'sentence': "I am 4 years old" },
    { 'name': 'Anne', 'sentence': "I am 27 years old" },
    { 'name': 'Joel', 'sentence': "I am 13 years old" },
])
# Look at the dataframe
sample_df


# In[31]:


# Given the sentence, "I am X years old", extract digits from the middle using ()
# Anything you put in () will be saved as an output.
# If you do expand=True it makes you a dataframe, but we don't want that.
sample_df['sentence'].str.extract("I am (\d+) years old", expand=False)


# In[32]:


# Save it into a new column
sample_df['age'] = sample_df['sentence'].str.extract("I am (\d+) years old", expand=False)
sample_df.head()


# **Now let's think about how we're going to extract the first names.** Begin by looking at a few full names.

# In[33]:


df['OWNER'].head(10)


# What can you use to find the first name? It helps to say "this is to the left and this is to the right, and I'm going to take anything in the middle."
# 
# Once you figure out how to extract it, you can do a `.head(10)` to just look at the first few.

# In[34]:


df['OWNER'].str.extract(r"([A-Za-z]+), ([A-Za-z]+) ([A-Za-z]*)", expand=True)[1]


# ## 22. Saving the owner's first name
# 
# Save the name to a new column, `FIRSTNAME`.

# In[35]:


df['FIRSTNAME'] = df['OWNER'].str.extract(r"([A-Za-z]+), ([A-Za-z]+) ([A-Za-z]*)", expand=True)[1]


# # 23. Examine everyone without a first name
# 
# I purposefully didn't do a nicer regex in order to have some screwed-up results. **How many people are there without an entry in the first name column?**
# 
# Your numbers might be different than mine.

# In[36]:


df[df.FIRSTNAME.isnull()].OWNER.count()


# What do their names look like?

# In[37]:


# NaN


# ## 24. If it's a problem, you can fix it (if you'd like!)
# 
# Maybe you have another regular expression that works better with JUST these people? It really depends on how you've put together your previous regex!
# 
# If you'd like to use a separate regex for this group, you can use code like this:
# 
# `df.loc[df.FIRSTNAME.isnull(), 'FIRSTNAME'] = .....`
# 
# That will only set the `FIRSTNAME` for people where `FIRSTNAME` is null.

# In[194]:


df.loc[df.FIRSTNAME.isnull(), 'FIRSTNAME'] = 'NA'


# How many empty first names do we have now?

# In[195]:


df[df.FIRSTNAME.isnull()].OWNER.count()


# My code before only worked for people with middle names, but now it got people without middle names, too. Looking much better!

# ## 25. Most popular first names?

# In[38]:


df.groupby('FIRSTNAME').FIRSTNAME.value_counts().sort_values(ascending=False).head(5)


# ## 26. Most popular first names for a Cosmetology Operator, Cosmetology Esthetician, Cosmetologist, and anything that seems similar?
# 
# If you get an error about "cannot index vector containing NA / NaN values" remember `.fillna(False)` or `na=False` - if a row doesn't have a license, it doesn't give a `True`/`False`, so we force all of the empty rows to be `False`.

# In[39]:


df[df.LICTYPE.str.contains("Cosmetolog", na=False)].groupby('FIRSTNAME').FIRSTNAME.value_counts().sort_values(ascending=False).head(10)


# ## 27. Most popular first names for anything involving electricity?

# In[40]:


df[df.LICTYPE.str.contains("Electric", na=False)].groupby('FIRSTNAME').FIRSTNAME.value_counts().sort_values(ascending=False).head(10)


# ## 28. Can we be any more obnoxious in this assignment?
# 
# A terrible thing that data analysts are often guilty of is using names to make assumptions about people. Beyond stereotypes involving last names, first names are often used to predict someone's race, ethnic background, or gender.
# 
# And if that isn't bad enough: if we were looking for Python libraries to do this sort of analysis, we'd come across [sex machine](https://github.com/ferhatelmas/sexmachine/). Once upon a time there was Ruby package named sex machine and everyone was like "come on are you six years old? is this how we do things?" and the guy was like "you're completely right I'm renaming it to [gender detector](https://github.com/bmuller/gender_detector)" and the world was Nice and Good again.
# 
# How'd it happen? [On Github, in a pull request!](https://github.com/bmuller/gender_detector/pull/14) Neat, right?
# 
# But yeah: apparently Python didn't get the message.
# 
# The sexmachine package doesn't work on Python 3 because it's from 300 BC, so we're going to use a Python 3 fork with the less problematic name [gender guesser](https://pypi.python.org/pypi/gender-guesser/).
# 
# #### Use `pip` or `pip3` to install gender-guesser.

# In[41]:


get_ipython().system('pip install gender-guesser')


# #### Run this code to test to see that it works

# In[42]:


import gender_guesser.detector as gender

detector = gender.Detector(case_sensitive=False)
detector.get_gender('David')


# In[43]:


detector.get_gender('Jose')


# In[44]:


detector.get_gender('Maria')


# #### Use it on a dataframe

# In[45]:


df['FIRSTNAME'].fillna('').apply(lambda FIRSTNAME: detector.get_gender(FIRSTNAME)).head()


# ## 29. Calculate the gender of everyone's first name and save it to a column
# 
# Confirm by see how many people of each gender we have

# In[46]:


df['GENDER'] = df['FIRSTNAME'].fillna('').apply(lambda FIRSTNAME: detector.get_gender(FIRSTNAME))


# In[47]:


df.groupby('GENDER').GENDER.value_counts()


# ## 30. We like our data to be in tidy binary categories
# 
# * Combine the `mostly_female` into `female` 
# * Combine the `mostly_male` into `male`
# * Replace `andy` (androgynous) and `unknown` with `NaN`
# 
# you can get NaN not by making a string, but with `import numpy as np` and then using `np.nan`.

# In[48]:


import numpy as np


# In[49]:


df['GENDER'] = df.GENDER.str.replace('mostly_female', 'female')
df['GENDER'] = df.GENDER.str.replace('mostly_male', 'male')
df['GENDER'] = df.GENDER.replace('andy', np.nan)
df['GENDER'] = df.GENDER.replace('unknown', np.nan)


# ## 31. Do men or women have more licenses? What is the percentage of unknown genders?

# In[50]:


df.groupby('GENDER').GENDER.value_counts()


# In[51]:


# Men have more licenses

Percentage_Unknown = 100 * df.GENDER.isnull().sum() / len(df)
print(Percentage_Unknown)


# ## 32. What are the popular unknown- or ambiguous gender first names?
# 
# Yours might be different! Mine is a combination of actual ambiguity, cultural bias and dirty data.

# In[52]:


df[df.GENDER.isnull() == True].groupby('FIRSTNAME').FIRSTNAME.value_counts().sort_values(ascending=False).head(5)


# ## 33. Manually check a few, too 
# 
# Using [a list of "gender-neutral baby names"](https://www.popsugar.com/family/Gender-Neutral-Baby-Names-34485564), pick a few names and check what results the library gives you.

# In[53]:


detector.get_gender('Harper')


# In[54]:


detector.get_gender('Jesse')


# In[55]:


detector.get_gender('Madison')


# 
# ## 34. What are the most popular licenses for men? For women?

# In[56]:


df[df.GENDER == 'male'].groupby('LICTYPE').LICTYPE.value_counts().sort_values(ascending=False).head(5)


# In[57]:


df[df.GENDER == 'female'].groupby('LICTYPE').LICTYPE.value_counts().sort_values(ascending=False).head(5)


# ## 35. What is the gender breakdown for Property Tax Appraiser? How about anything involving Tow Trucks?
# 
# If you're in need, remember your good friend `.fillna(False)` to get rid of NaN values, or `.na=False` with `.str.contains`.

# In[58]:


df[df['LICTYPE'].str.contains("Property Tax Appraiser", na=False)].groupby('GENDER').GENDER.value_counts().sort_values(ascending=False).head()


# In[59]:


df[df['LICTYPE'].str.contains("Tow Truck", na=False)].groupby('GENDER').GENDER.value_counts().sort_values(ascending=False).head()


# (By the way, what are those tow truck jobs?)

# In[60]:


df[df['LICTYPE'].str.contains("Tow Truck", na=False)].groupby('LICTYPE').LICTYPE.value_counts().head()


# ## 33. Graph them!
# 
# And let's **give them titles** so we know which is which.

# In[61]:


df[df['LICTYPE'].str.contains("Tow Truck", na=False)].groupby('GENDER').GENDER.value_counts().sort_values(ascending=False).plot(xlabel='Gender', title='Tow Truck Breakdown', kind='barh')


# In[62]:


df[df['LICTYPE'].str.contains("Property Tax Appraiser", na=False)].groupby('GENDER').GENDER.value_counts().sort_values(ascending=False).plot(xlabel='Gender', title='Property Tax Appraiser Breakdown', kind='barh')


# ## 34. Calcuate the supposed gender bias for profession
# 
# I spent like an hour on this and then realized a super easy way to do it. Welcome to programming! I'll do this part for you.

# In[63]:


# So when you do .value_counts(), it gives you an index and a value
df[df['GENDER'] == 'male'].LICTYPE.value_counts().head()


# We did `pd.concat` to combine dataframes, but you can also use it to combine series (like the results of `value_counts()`). If you give it a few `value_counts()` and give it some column names it'll make something real nice.

# In[64]:


# All of the values_counts() we will be combining
vc_series = [
    df[df['GENDER'] == 'male'].LICTYPE.value_counts(),
    df[df['GENDER'] == 'female'].LICTYPE.value_counts(),
    df[df['GENDER'].isnull()].LICTYPE.value_counts()
]
# You need axis=1 so it combines them as columns
gender_df = pd.concat(vc_series, axis=1)
gender_df.head()


# In[65]:


# Turn "A/C Contractor" etc into an actual column instead of an index
gender_df.reset_index(inplace=True)
gender_df.head()


# In[66]:


# Rename the columns appropriately
gender_df.columns = ["license", "male", "female", "unknown"]
# Clean up the NaN by replacing them with zeroes
gender_df.fillna(0, inplace=True)
gender_df.head()


# ## 35. Add new columns for total licenses, percent known (not percent unknown!), percent male (of known), percent female (of known)
# 
# And replace any `NaN`s with `0`.

# In[67]:


gender_df['Total_Licenses'] = gender_df.male + gender_df.female + gender_df.unknown


# In[68]:


gender_df['Percent_Known'] = ((gender_df.male + gender_df.female)/gender_df.Total_Licenses)*100


# In[69]:


gender_df['Percent_Male_Known'] = ((gender_df.male/(gender_df.male + gender_df.female))*100)


# In[70]:


gender_df['Percent_Female_Known'] = ((gender_df.female/(gender_df.male + gender_df.female))*100)


# In[71]:


gender_df.head(5)


# ## 35. What 10 licenses with more than 2,000 people and over 75% "known" gender has the most male owners? The most female?

# In[110]:


gender_df[(gender_df.Total_Licenses > 2000) & (gender_df.Percent_Known > 75)].sort_values(by='male', ascending=False).head(10)


# In[111]:


gender_df[(gender_df.Total_Licenses > 2000) & (gender_df.Percent_Known > 75)].sort_values(by='female', ascending=False).head(10)


# ## 36. Let's say you have to call a few people about being in a profession dominated by the other gender. What are their phone numbers?
# 
# This will involve doing some research in one dataframe, then the other one. I didn't put an answer here because I'm interested in what you come up with!

# In[119]:


merged = gender_df.merge(df, left_on="license", right_on="LICTYPE")
merged[merged.Percent_Female_Known>50].head(10)['TELEPHONE']


# ## Okay, let's take a break for a second.
# 
# We've been diving pretty deep into this gender stuff after an initial "oh but it's not great" kind of thing.
# 
# **What issues might come up with our analysis?** Some might be about ethics or discrimination, while some might be about our analysis being misleading or wrong. Go back and take a critical look at what we've done since we started working on gender, and summarize your thoughts below.

# In[72]:


# The gender generator could be inaccurate (especially for the "mostly male" and "mosty female"
# Unknown really doesn't mean anything, and there are so many unknowns that it could change 
# basically all our results. Plus, male and female is binary and gender is not binary. 


# If you found problems with our analysis, **how could we make improvements?**

# In[73]:


# Find a way to not lump everything together as unknown! 


# In[74]:


# There were some names that were actually business names, so use str contains to remove
# names containing INC and LTD so they don't mess with the gender results. 


# ## PART FIVE: Violations
# 
# ### 37. Read in **violations.csv** as `violations_df`, make sure it looks right

# In[75]:


violations_df = pd.read_csv("/Users/mahiradayal/computing/hw-8/licensing/violations.csv", na_values=None)
violations_df.dtypes


# In[76]:


df.dtypes


# ### 38. Combine with your original licenses dataset dataframe to get phone numbers and addresses for each violation. Check that it is 90 rows, 28 columns.

# In[130]:


violations_merged = violations_df.merge(df, left_on="licenseno", right_on="LICNUMBER")
#violations_merged.shape
violations_merged.head(5)


# ## 39. Find each violation involving a failure with records. Use a regular expression.

# In[150]:


violations_merged[violations_merged['basis'].str.contains(r"fail")==True]


# ## 40. How much money was each fine? Use a regular expression and .str.extract
# 
# Unfortunately large and helpful troubleshooting tip: `$` means "end of a line" in regex, so `.extract` isn't going to accept it as a dollar sign. You need to escape it by using `\$` instead.

# In[164]:


violations_merged['order'].str.extract("Respondent is assessed an administrative penalty in the amount of \$(\w+,?\w+).", expand=False)  


# ## 41. Clean those results (no commas, no dollar signs, and it should be an integer) and save it to a new column called `fine`
# 
# `.replace` is for *entire cells*, you're interested in `.str.replace`, which treats each value like a string, not like a... pandas thing.
# 
# `.astype(int)` will convert it into an integer for you.

# In[188]:


violations_merged['fine'] = violations_merged['order'].str.extract("Respondent is assessed an administrative penalty in the amount of \$(\w+,?\w+).", expand=False)  
violations_merged['fine'] = violations_merged['fine'].apply(lambda x: x.replace(',', ''))
violations_merged['fine'].astype(int)
violations_merged['fine'].head(20)


# ## 42. Which orders results in the top fines?

# In[193]:


violations_merged.sort_values(by=['money'], ascending=False).head()


# ## 43. Are you still here???
# 
# I'm sure impressed.

# In[78]:


# Everything hurts and I don't remember what sunlight looks like. 

