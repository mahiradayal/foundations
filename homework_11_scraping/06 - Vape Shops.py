#!/usr/bin/env python
# coding: utf-8

# # Scraping Maryland Business Licenses with Selenium
# 
# Maryland has a [great portal](https://jportal.mdcourts.gov/license/pbPublicSearch.jsp) for searching business licenses, but the only problem is you have to check a box in order to get in.
# 
# 1. Try to visit [the public search page](https://jportal.mdcourts.gov/license/pbPublicSearch.jsp)
# 2. Get redirected to a "I agree to this" page. Click that you've read the disclaimer, click Enter the Site.
# 3. Click "Search License Records" down at the bottom of the page
# 4. You're now on the search page! From the "Jurisdiction" dropdown, select "Statewide"
# 5. In the "Trade Name" field, type "Vap%" to try to find vape shops
# 6. Click "Next" in the bottom right-hand corner to go to the next page
# 7. Click "Click for detail" to see the details for a specific business license.
# 
# That's a lot of stuff! **Let's get to work.**

# ## Import what you need

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


# ## Preparation
# 
# ### When you search for a business license, what URL should Selenium try to visit first?

# In[3]:


# https://jportal.mdcourts.gov/license/pbIndex.jsp?ac=y


# In[4]:


driver.get("https://jportal.mdcourts.gov/license/index_disclaimer.jsp")


# **It isn't going to work, though! It's going to redirect to that intro page.** You can use *Incognito mode* to go back through the "Check the box, etc" series of pages, or you can close and re-open Chrome.
# 
# - Check the checkbox, then submit the form to accept their terms of service
# 
# Selenium can submit forms by either
# 
# - Selecting the form and using `.submit()`, or
# - Selecting the button and using `.click()`
# 
# You only need to be able to get **one, not both.**
# 
# - *TIP: if something doesn't have anything special about it, xpath might be your best bet*

# In[5]:


button = driver.find_element_by_id("checkbox")
button.click()
enter = driver.find_elements_by_tag_name("tr")[6].find_elements_by_tag_name("input")[1]
enter.click()


# Now click the **Search License Records** link up top in the navigation to get to the search page.
# 
# - *TIP: Honestly you could also just visit the URL directly now since you filled out that terms of service thing*

# In[6]:


driver.get("https://jportal.mdcourts.gov/license/pbPublicSearch.jsp")


# ### Perform your search
# 
# Pick "Statewide" for the jurisdiction dropdown, and `VAP%` into the Trade Name field. The `%` is a wildcard.
# 
# *TIP: I wish I could put this on CourseWorks, but it looks too ugly: [Selenium snippets](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-snippets/) will help you with the dropdown*

# In[7]:


from selenium.webdriver.support.ui import Select
select = Select(driver.find_element_by_id('slcJurisdiction'))
select.select_by_visible_text('Statewide')

trade_name = driver.find_element_by_id("txtTradeName")
trade_name.send_keys("VAP%")


# And now, of course, **submit the form**.
# 
# - *TIP: Since scrolling to buttons can be a pain, sometimes it's easier to select the form and use `.submit()` instead of `.click()`ing the button*

# In[8]:


driver.find_element_by_name('searchForm').submit()


# ## (Try to) scrape the results
# 
# Let's start by just **printing this stuff**. We'll save it as a dataframe later on.
# 
# For now, just scrape **each store's name**, then cry a little. Fact: this is an impossible and miserable page. 

# In[9]:


stores = driver.find_elements_by_class_name("searchfieldtitle")

for store in stores: 
    name = store.find_element_by_class_name("copybold").text.strip()
    print(name)


# To avoid struggling with the search results page, we're going to use the **detail page** instead. Try to figure out how to select it and click it inside of your `for` loop.
# 
# - *TIP: Instead of just looking for an `a` or an `img`, you might want to look for one of its parents first, then click. This might affect the way you print out the shop's name, too*
# - *TIP: Not all of them have links! You can wrap in try/except to skip it, or you can check to see if the shop's status is Pending.*

# In[10]:


stores = driver.find_elements_by_class_name("searchfieldtitle")

name_url = []

for store in stores: 
    
    name = store.find_element_by_class_name("copybold").text.strip()
    
    try: 
        details = store.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute('href')
        print(details)
        
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(details)
        
#         Just to make sure this is actually doing something. 
#         random = driver.find_elements_by_tag_name('td')[3]
#         print(random)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
    except: 
        
        details = "No URL"
        print(name)
    
    name_url_dict = {
        'name': name, 
        'url': details
    }
    
    name_url.append(name_url_dict)


# Okay, now let's get to action. For each result, **click the link to the detail page** and print out the following information:
# 
# - Mailing address
# - Location address
# - License information (you can keep it as one field)
# - Total amount paid
# - Issued by
# - If you're feeling crazy, get the licenses, too.
# 
# If it doesn't have a detail page, just print out the name and that's all we need.
# 
# - *TIP: `try`/`except` is probably going to be your friend. What's it do?
# - *TIP: When you're done getting the information, you probably want to click back to the search results*
# - *TIP: You might enjoy `find_element_by_partial_link_text` to do that*
# - *TIP: Licenses can be acquired by doing some really odd list slicing - think about where it starts and where it ends, relative to the beginning and end of everything.*
# 
# > **IMPORTANT NOTE:** This is doomed!!!! It's useful to do, but your current process is doomed. Once you get a `stale element reference` error move on to the next cell.

# In[11]:


stores = driver.find_elements_by_class_name("searchfieldtitle")

truck_details = []

for store in stores: 
    
    name = store.find_element_by_class_name("copybold").text.strip()
    
    try: 
        details = store.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute('href')
        
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(details)
        
        mailing = driver.find_element_by_class_name('tablecelltext').find_element_by_tag_name("td").text.strip()

        location = driver.find_elements_by_class_name('tablecelltext')[1].find_element_by_tag_name("td").text.strip()
        
        license_info = driver.find_element_by_class_name('tablecelltext').find_elements_by_tag_name("td")[1].text.strip()
        
        paid = driver.find_elements_by_class_name('tablecelltext')[6].find_elements_by_class_name('rt')[1].text.strip()
        
        issued = driver.find_elements_by_class_name('tablecelltext')[7].find_element_by_tag_name("td").text.strip()
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
   
    except: 
        
        details = "NA"
        print(details)
        continue 
       
    truck_dict = {
        'name': name, 
        'url': details, 
        'mailing': mailing, 
        'location': location, 
        'license_info': license_info,
        'pay': paid, 
        'issued': issued
    }
    
    truck_details.append(truck_dict)
    
truck_details
    


# ### Stale message reference
# 
# Once you navigate away from a page, and you go back to it, you (sometimes, usually) can't use the variables from the first time you were on the page. So, we got a list of results when we first visited, clicked to the details page, clicked back, and now our original list is "stale."
# 
# This is sad.
# 
# Let's try this again: loop through the results and create a dataframe with `name` and `url` columns. And yes, some of them won't have URLs. No clicking links, just saving URLs.

# In[12]:


# name_url
# Made this above because it was quicker. 

df = pd.DataFrame(name_url) 
df


# ### Getting all of the results
# 
# After you've looped through the results on one page, we're going to want to go to the next page! Add a line to make it click the 'Next' button down at the bottom
# 
# - *TIP: `find_element_by_partial_link_text` will be your friend*
# - *TIP: You might need to do the scrolling thing to get it onto the screen (and by that I mean, you WILL need to, so you should)*
# 
# Confirm that it moves to the next page (it doesn't need to scrape anything yet)

# In[13]:


stores = driver.find_elements_by_class_name("searchfieldtitle")

truck_details = []

for store in stores: 
    
    name = store.find_element_by_class_name("copybold").text.strip()
    
    try: 
        details = store.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute('href')
        
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(details)
        
        mailing = driver.find_element_by_class_name('tablecelltext').find_element_by_tag_name("td").text.strip()

        location = driver.find_elements_by_class_name('tablecelltext')[1].find_element_by_tag_name("td").text.strip()
        
        license_info = driver.find_element_by_class_name('tablecelltext').find_elements_by_tag_name("td")[1].text.strip()
        
        paid = driver.find_elements_by_class_name('tablecelltext')[6].find_elements_by_class_name('rt')[1].text.strip()
        
        issued = driver.find_elements_by_class_name('tablecelltext')[7].find_element_by_tag_name("td").text.strip()
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
           
    except: 
        
        details = "NA"
        print(details)
        continue 
       
    truck_dict = {
        'name': name, 
        'url': details, 
        'mailing': mailing, 
        'location': location, 
        'license_info': license_info,
        'pay': paid, 
        'issued': issued
    }
    
    truck_details.append(truck_dict)
    
next_button = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[4]/td[2]/table[2]/tbody/tr/td[3]/a')
next_button.click()
    
truck_details


    


# ### Wrapping with `while`
# 
# > Go back to the first page of results before you try to run this
# 
# You have a bunch of scraping code. It clicks the next button, then it stops. But you'd like it to go back up to the top! You can make that happen with a special `while` loop.
# 
# ```python
# while True:
#     # Scrape your stuff
#     # Click next button
# ```
# 
# This will go on FOREVER AND EVER until there is an error (when it can't find the Next button on the last page of results, you'll get a `NoSuchElement` error when it tries to find the next button).
# 
# - *Tip: Print out "Scraping a new page" every time you visit a new page, just to check that it's working*

# In[14]:


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[15]:


# next_button = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[4]/td[2]/table[2]/tbody/tr/td[3]/a')

# while next_button not None:
#     next_button.click()
    
#     next_button = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[4]/td[2]/table[2]/tbody/tr/td[3]/a')


#     # 1. Scrape all the stuff. 
#     # 2. Hit next -- find next, click on it 
#     # If the next button exists, then click on it. 


# In[28]:


truck_details = []
i = 1
# next_button = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[4]/td[2]/table[2]/tbody/tr/td[3]/a')
# while next_button is not None:
while True: 
    stores = driver.find_elements_by_class_name("searchfieldtitle")
    for store in stores: 
        name = store.find_element_by_class_name("copybold").text.strip()
        print('---------------------------')
        print(i, name)
        i+=1
        try: 
            details = store.find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute('href')
            #print(details)
        except: 
            continue 
        try: 
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(details)
            mailing = driver.find_element_by_class_name('tablecelltext').find_element_by_tag_name("td").text.strip()
            #print(mailing)
            location = driver.find_elements_by_class_name('tablecelltext')[1].find_element_by_tag_name("td").text.strip()
            #print(location)
            license_info = driver.find_element_by_class_name('tablecelltext').find_elements_by_tag_name("td")[1].text.strip()
            #print(license_info)
            paid = driver.find_elements_by_class_name('tablecelltext')[6].find_elements_by_class_name('rt')[1].text.strip()
            #print('hi')
            issued = driver.find_elements_by_class_name('tablecelltext')[7].find_element_by_tag_name("td").text.strip()
            #print(issued)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except: 
            details = "NA"
            #print(details)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue 
        truck_dict = {
            'name': name, 
            'url': details, 
            'mailing': mailing, 
            'location': location, 
            'license_info': license_info,
            'pay': paid, 
            'issued': issued
        }
        truck_details.append(truck_dict)
    next_button = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr[4]/td[2]/table[2]/tbody/tr/td[3]/a')
    driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
    next_button.click()
truck_details


# In[29]:


truck_details


# ### Making it perfect
# 
# > Go back to the first page of results before you try to run this
# 
# Wrap all of your code in a `try`/`except` so that it doesn't finish with an error and you'll be good to go.
# 
# **Confirm your list has all of the vape shops in it.** If not, check where you are creating your empty list (`[]`) - if you do it in the wrong spot, it will overwrite your list every time you visit a page.

# In[ ]:


# did this before with 2 try and excepts. 


# ### Save this data as a csv
# 
# The filename should be `vape-shops-basic.csv`. You should have 24 rows.

# In[30]:


df = pd.DataFrame(truck_details) 


# In[27]:


df


# In[31]:


df.to_csv('vape-shops-basic.csv')  


# # Okay, let's scrape!
# 
# All right, get the actual data!
# 
# ### Look at the URL of your first row
# 
# - *TIP: Remember `pd.set_option('display.max_colwidth', None)` will let you see alllll of your strings*

# In[ ]:


pd.set_option('display.max_colwidth', None)
vape = pd.read_csv('vape-shops-basic.csv')


# ### Okay, it doesn't have a URL!
# 
# Let's drop all of the ones without URLs. You should be down to **17 rows**

# In[ ]:


# Dropped while scraping


# Now look at the first one.

# In[ ]:


vape.head(1)


# ### Use Selenium to visit that page

# In[ ]:


# .iloc[0] means "give me the first row", kind of like .head(1), but
# it allows me to use .url to pull out the actual url. I only did this
# so that I could use a variable - you just needed to cut and paste
url = df.iloc[0].url
url


# In[ ]:





# ### Now, just like you did before, grab the additional data
# 
# You should probably save it into a dictionary! Don't try to put it into the dataframe yet, though. You want:
# 
# - Mailing address
# - Location address
# - License information (you can keep it as one field)
# - Total amount paid
# - Issued by
# - If you're feeling crazy, get the licenses, too.
# 
# .
# 
# - *TIP: Licenses can be acquired by doing some really odd list slicing - think about where it starts and where it ends, relative to the beginning and end of everything.*
# - *TIP: If you've gotten addicted to xpath, total amount paid and issued by might not work with it when doing other shops. You'll want to test it! It's because xpath relies on things like "it's the fourth row" but maybe there are more or fewer licenses sometimes, right? But you know it's always a certain number from the last row, so maybe use negative numbers with `.find_elements_by_...`? This is probably a confusing explanation.*

# In[ ]:





# ### Move all of this into one cell
# 
# It should visit the URL, then grab the data and put it into a dictionary.

# In[ ]:





# ### Change it into a function
# 
# You'll want to have this function accept a `row`, and send back a `pd.Series`. You can just use `pd.Series(your_dictionary)` (but it better have a better name than `your_dictionary`!).
# 
# - *TIP: Make sure you `return` something!*
# - *TIP: Make sure you change everything to reflect the row's url, not the URL you typed in*

# In[ ]:





# ### Use your dataframe and `.apply` to pull all of the data from the vape shops
# 
# Once you know it's working, use the whole 
# 
# - *TIP: Try using it with `.head(3)` first*
# - *TIP: You'll want to use `.apply` with your new function*
# - *TIP: Issued By and Total Paid are goign to give you problems if you tried to use xpath! Try checking the classes and think about find_elementSSSSS and working backwards instead of forwards.*
# - *TIP: You might need a `try`/`except`*
# - *TIP: Make sure you're using `axis=1`*
# - *TIP: Use `.join` the big thing with all of the `dfs` - make sure you name them right!*

# In[ ]:





# ## Save as `vape-total.csv`
# 
# Make sure you don't save the index! Open it up in a text editor or Excel to make sure it's correct.

# In[ ]:





# In[ ]:





# In[ ]:




