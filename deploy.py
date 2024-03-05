import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)




def encode_data(dataframe_series):
        if dataframe_series.dtype=='object':
            dataframe_series = LabelEncoder().fit_transform(dataframe_series)
        return dataframe_series

def show_page():
    colT1,colT2 = st.columns([1,8])
    with colT2:
        st.title("Proyek Analisis Data: E-Commerce Public Datase")

    st.write(" Nama:  Sulaiman Bilal Muzakhar ")
    st.write(" Email: sulbilmuzakhar@gmail.com ")
    st.write(" ID Dicoding: sulaiman_bilal_muzakhar_QNPe ")

    #import
    dataframe_review = pd.read_csv('olist_order_reviews_dataset.csv')
    dataframe_produk = pd.read_csv('olist_products_dataset.csv')
    dataframe_order_item = pd.read_csv('olist_order_items_dataset.csv')
    dataframe_kategori = pd.read_csv('product_category_name_translation.csv')
    dataframe_orders = pd.read_csv('olist_orders_dataset.csv')
    dataframe_customer = pd.read_csv('olist_customers_dataset.csv')
    dataframe_seller = pd.read_csv('olist_sellers_dataset.csv')
    dataframe_payment = pd.read_csv('olist_order_payments_dataset.csv')

    dataframe_produk['product_weight_g'].fillna(method='ffill', inplace=True)
    dataframe_produk['product_length_cm'].fillna(method='ffill', inplace=True)
    dataframe_produk['product_height_cm'].fillna(method='ffill', inplace=True)
    dataframe_produk['product_width_cm'].fillna(method='ffill', inplace=True)
    dataframe_produk['product_name_lenght'].fillna(method='ffill', inplace=True)
    dataframe_produk['product_description_lenght'].fillna(method='ffill', inplace=True)
    dataframe_produk['product_photos_qty'].fillna(method='ffill', inplace=True) 
    mode_category = dataframe_produk['product_category_name'].mode()[0]
    dataframe_produk['product_category_name'].fillna(value=mode_category, inplace=True)
    dataframe_order_item['shipping_limit_date'] = pd.to_datetime(dataframe_order_item['shipping_limit_date'])
    dataframe_orders.dropna(axis=0, inplace=True)
    dataframe_orders['order_purchase_timestamp'] = pd.to_datetime(dataframe_orders['order_purchase_timestamp'])
    dataframe_orders['order_approved_at'] = pd.to_datetime(dataframe_orders['order_approved_at'])
    dataframe_orders['order_delivered_carrier_date'] = pd.to_datetime(dataframe_orders['order_delivered_carrier_date'])
    dataframe_orders['order_delivered_customer_date'] = pd.to_datetime(dataframe_orders['order_delivered_customer_date'])
    dataframe_orders['order_estimated_delivery_date'] = pd.to_datetime(dataframe_orders['order_estimated_delivery_date'])
    order_information = pd.merge(dataframe_produk[['product_id', 'product_category_name']], dataframe_order_item[['order_id','order_item_id','product_id','shipping_limit_date']], on='product_id', how='inner')
    order_information = pd.merge(order_information,dataframe_kategori[['product_category_name', 'product_category_name_english']], on='product_category_name', how='inner')
    order_information = order_information.drop('product_category_name',axis=1)
    order_information.loc[:, 'year'] = order_information['shipping_limit_date'].dt.to_period('Y')
    review_info = pd.merge(order_information[['order_id','product_category_name_english','year']],dataframe_review[['order_id','review_score']], on='order_id', how='inner')
    review_2017 = review_info[review_info['year'] == '2017']
    average_review_2018 = review_2017.groupby('product_category_name_english')['review_score'].mean().reset_index()
    best_review_2018 = average_review_2018.sort_values(by='review_score', ascending=False)
    top_3_products = best_review_2018.head(3).reset_index(drop=True)
    bot_3_products = best_review_2018.tail(3).reset_index(drop=False)
    df_payment=dataframe_payment['payment_type'].value_counts()

    bar1= top_3_products.plot(kind='bar', x='product_category_name_english', y='review_score', color='skyblue')
    bar1= plt.title('Top 3 Produk dengan Review Score Tertinggi di Tahun 2017')
    bar1= plt.xlabel('Product Category')
    bar1= plt.ylabel('Rata-rata Review Score')
    bar1= plt.xticks(rotation=45)
    bar1= plt.tight_layout()
    bar1= plt.show()
    st.subheader(""" Dashboard """)
    st.pyplot(bar1)
    bar2=  bot_3_products.plot(kind='bar', x='product_category_name_english', y='review_score', color='salmon')
    bar2=plt.title('Top 3 Produk dengan Review Score Terendah di Tahun 2017')
    bar2=plt.xlabel('Product Category')
    bar2=plt.ylabel('Rata-rata Review Score')
    bar2=plt.xticks(rotation=45)
    bar2=plt.tight_layout()
    bar2=plt.show()
    
    st.pyplot(bar2)

    df_payment.plot(kind='bar', color='skyblue')
    plt.title('Jumlah Pembayaran berdasarkan Jenis Pembayaran')
    plt.xlabel('Jenis Pembayaran')
    plt.ylabel('Jumlah Pembayaran')
    plt.xticks(rotation=45)
    plt.tight_layout()
    bar3= plt.show()
    st.pyplot(bar3)

        
