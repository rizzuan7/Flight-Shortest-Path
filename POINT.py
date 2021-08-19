#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas,os


# In[2]:


df1=pandas.read_csv("city.csv")


# In[3]:


df1


# In[4]:


import geopy


# In[5]:


dir(geopy)


# In[6]:


from geopy.geocoders import Nominatim


# In[7]:


nom = Nominatim()


# In[8]:


df1["Coordinates"]=df1["Adress"].apply(nom.geocode) 


# In[9]:


df1["Latitude"]=df1["Coordinates"].apply(lambda x: x.latitude if x !=None else None)


# In[10]:


df1["Longitude"]=df1["Coordinates"].apply(lambda x: x.longitude if x !=None else None)


# In[11]:


df1["Longitude"]=df1["Coordinates"].apply(lambda x: x.longitude if x !=None else None)


# In[12]:


from geopy.distance import great_circle


# In[13]:


df1


# In[14]:


KL=(3.1516636, 101.6943028)
HN=(21.0294498, 105.8544441)
TP=(25.0375198, 121.563680)
SL=(37.566679, 126.978291)
TK=(35.6828387, 139.7594549)
HK=(22.350627, 114.1849161)
CH=(30.662420, 104.063322)
ZH=(34.759188, 113.652408)
VN=(49.260872, -123.113953)


# In[15]:


print("KL,HANOI :",great_circle(VN, HN).kilometers)
print("KL,TAIPEI :",great_circle(VN, TP).kilometers)
print("KL,SEOUL :",great_circle(VN, SL).kilometers)
print("KL,TOKYO :",great_circle(VN, TK).kilometers)
print("KL,HONG KONG :",great_circle(VN, HK).kilometers)
print("KL,CHENGDU :",great_circle(VN, CH).kilometers)
print("KL,ZHENGZHOU :",great_circle(VN, ZH).kilometers)
print("KL,VANCOUVER :",great_circle(VN, VN).kilometers)


# In[ ]:




