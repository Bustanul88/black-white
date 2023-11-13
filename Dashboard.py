#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


# In[11]:


all_df = pd.read_csv('all_data.csv')


# In[6]:


date_time = ['shipping_limit_date','review_answer_timestamp','order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date']
for columns in date_time:
    all_df[columns] = pd.to_datetime(all_df[columns])


# In[7]:


revenue_seller = all_df.groupby(by='seller_id', as_index=False).agg({
'price':'sum'
}, inplace=True)


# In[8]:


min_date = all_df['order_purchase_timestamp'].min()
max_date = all_df['order_purchase_timestamp'].max()

with st.sidebar:
    start_date,end_date = st.date_input(
    label="Rentang Waktu",min_value=min_date,
    max_value=max_date,
    value=[min_date,max_date]
    )


# In[9]:


st.header("Data E-commerce with Dashboard")


# In[16]:


sum_order_item_df = all_df.groupby(by='product_category_name').freight_value.sum().sort_values(ascending=False).reset_index()


# In[17]:


st.subheader("Best and Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

color = ['#F67828', '#A9A9A9', '#A9A9A9', '#A9A9A9', '#A9A9A9']

sns.barplot(x='freight_value',y='product_category_name', data = sum_order_item_df.head(5), palette=color, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title('Best Performing Product',loc='center', fontsize=50)
ax[0].tick_params(axis='y',labelsize=12)

sns.barplot(x='freight_value',y='product_category_name', data = sum_order_item_df.sort_values(by='freight_value',ascending=True).head(5), palette=color, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position('right')
ax[1].yaxis.tick_right()
ax[1].set_title('Worst Performing Product',loc='center', fontsize=50)
ax[1].tick_params(axis='y',labelsize=12)

st.pyplot(fig)


# In[18]:


product_review_score = all_df.groupby(by='product_category_name').review_score.mean().sort_values(ascending=False).reset_index()


# In[23]:


st.subheader("Best and Worst Review Score")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

color = ['#F67828', '#A9A9A9', '#A9A9A9', '#A9A9A9', '#A9A9A9']

sns.barplot(x='product_category_name',y='review_score', data=product_review_score.head(5), palette=color, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title('Best Review Score',loc='center', fontsize=50)
ax[0].tick_params(axis='x',labelsize=15, rotation=70)

sns.barplot(x='product_category_name',y='review_score', data=product_review_score.sort_values(by='review_score',ascending=True).head(5), palette=color, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position('right')
ax[1].yaxis.tick_right()
ax[1].set_title('Worst Review Score',loc='center', fontsize=50)
ax[1].tick_params(axis='x',labelsize=15, rotation=70)

st.pyplot(fig)


# In[24]:


colors = ['#FF6F5E','#6A9C89','#F0134D','#F5F0E3','#40BFC1']
explode = (0.1,0,0.05,0,0)
fig = plt.figure(figsize=(6,6))
ax = plt.axes()
ax.pie('price', labels = 'seller_id', data = revenue_seller.sort_values(by='price', ascending=False).head(5), autopct = '%1.0f%%', explode=explode,colors = colors)
ax.set_title ('Diagram Pendapatan Seller')

st.pyplot(fig)


# In[ ]:




