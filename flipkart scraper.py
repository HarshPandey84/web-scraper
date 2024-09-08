from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st


global name
st.title("E-Commerce Product")
name=st.text_input("Enter product name:")
try:
    def search():
        
        mname=name.strip().replace(" ","+")

        html_text = requests.get("https://www.flipkart.com/search?q="+mname+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off").text

        soup = BeautifulSoup(html_text, 'lxml')
        names = soup.find_all('div', class_='KzDlHZ')
        prices = soup.find_all('div', class_='Nx9bqj _4b5DiR')
        ratings = soup.find_all('div', class_='XQDdHH')
        links = soup.find_all('a', class_='CGtC98')
        if(len(links)==0):

            names = soup.find_all('a' , class_="wjcEIp")
            prices = soup.find_all('div', class_="Nx9bqj")
            ratings = soup.find_all('div', class_="XQDdHH")
            links = soup.find_all('a', class_='VJA3rP')


        if(len(links)>0):
            dict = {'Product Name':[], 'Rating':[], 'Price(₹)':[],  'Webstore':[],'Link':[]}
            for i in range(0,len(names)):
                dict['Product Name'].append(names[i].text)
                dict['Price(₹)'].append(int(prices[i].text[1:].replace(",","")))
                dict['Rating'].append(ratings[i].text+" *")
                dict['Webstore'].append("Flipkart")
                dict['Link'].append("https://www.flipkart.com"+links[i]["href"])
        else:
            dict={'Product Name':[], 'Rating':[], 'Price(₹)':[],  'Webstore':[]}
            for i in range(0,len(names)):
                dict['Product Name'].append(names[i].text)
                dict['Price(₹)'].append(int(prices[i].text[1:].replace(",","")))
                dict['Rating'].append(ratings[i].text+" *")
                dict['Webstore'].append("Flipkart")
        df = pd.DataFrame(data=dict)
        df = df.sort_values(by=['Rating'], ascending=False)
        df.to_excel('ecommerce_products.xlsx',index=False)
        st.write(df)

    if(st.button("Search")):
        df=search()
except IndexError as e:
    st.error("Sorry! No results found")
