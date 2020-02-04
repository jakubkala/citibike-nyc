#!/usr/bin/env python
# coding: utf-8

# In[15]:


import requests
import urllib.request

def downloadzip(file,url):
    r = requests.get(url)
    with open(file, "wb") as code:
        code.write(r.content)
    urllib.request.urlretrieve(url, file)
    print(file + "DONE")


# ## 2013

# In[24]:


import tqdm

for i in tqdm.tqdm(range(8,13)):
    base = 'https://s3.amazonaws.com/tripdata/'
    if  i < 10:
        file = '20130' + str(i) + '-citibike-tripdata.zip'
    else:
        file = '2013' + str(i) + '-citibike-tripdata.zip'
    url = base + file
    
    downloadzip(url,file)


# # 2014 - 2016

# In[27]:


for rok in range(2014,2019):
    for i in tqdm.tqdm(range(1,13)):
        base = 'https://s3.amazonaws.com/tripdata/'
        if  i < 10:
            file =  str(rok) + '0' + str(i) + '-citibike-tripdata.zip'
        else:
            file = str(rok) + str(i) + '-citibike-tripdata.zip'
        url = base + file
    
        downloadzip(url,file)


# ## 2017 - 2019

# In[29]:


for rok in range(2017,2019):
    for i in tqdm.tqdm(range(1,13)):
        base = 'https://s3.amazonaws.com/tripdata/'
        if  i < 10:
            file =  str(rok) + '0' + str(i) + '-citibike-tripdata.csv.zip'
        else:
            file = str(rok) + str(i) + '-citibike-tripdata.csv.zip'
        url = base + file
    
        downloadzip(url,file)


# ## 2019

# In[30]:


for rok in range(2019,2020):
    for i in tqdm.tqdm(range(1,12)):
        base = 'https://s3.amazonaws.com/tripdata/'
        if  i < 10:
            file =  str(rok) + '0' + str(i) + '-citibike-tripdata.csv.zip'
        else:
            file = str(rok) + str(i) + '-citibike-tripdata.csv.zip'
        url = base + file
    
        downloadzip(url,file)


# In[ ]:




