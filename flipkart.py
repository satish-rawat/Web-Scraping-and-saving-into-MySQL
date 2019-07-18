#!/usr/bin/env python
# coding: utf-8

# Web Scraping Flipkart 
# 
# 1)Making list of Books.
# 2)Scraping Title,Rating and Price of Books 
# 3)Saving into MySQL Database
# 4)A beginner can understand this Code as it is not that much Pythonic




import pandas as pd
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

#declaring 3 empty list

Rating=[]
Title=[]
Price=[]

#iterating over different url of using for Loop

for i in range(1,5):
    URL='https://www.flipkart.com/books/fiction-nonfiction-books/literature-fiction-books/romance-books/pr?sid=bks%2Cfnf%2Cgld%2C83v&otracker=clp_banner_1_5.bannerX3.BANNER_theliterature-fiction-store_DUU64IPVDV&fm=neo%2Fmerchandising&iid=M_5147f290-6314-49bb-a859-e430f3fac7f7_5.DUU64IPVDV&ppt=clp&ppn=theliterature-fiction-store&page='+str(i)
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html.parser')
    
    #Parsing Text From Soup Object using HTML Tags and Attribute For Desired Data
    
    rating = soup.find_all("div", class_="hGSR34")
    price = soup.find_all("div", class_="_1vC4OE")
    title = soup.find_all("a", class_="_2cLu-l")
    
    # Iterating over above variable and parsing the text and saving into different list
    
    for a in title:
        Title.append(a.text)
    for b in price:    
        Price.append(b.text)
    for c in rating:    
        Rating.append(c.text)  
# Cleaning the special character from price list

Price=list(map(lambda x: x.replace('₹',''),Price))
Price=list(map(lambda x: x.replace(',',''),Price))

# Making List of tuple and changing to dataframe for another process

Data=list(zip(Title,Price,Rating))
df = pd.DataFrame(Data)
df.head(10)

# Connecting to MySQL Database

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="xyz",
  database="abc"
)

# Creating Cursor object

mycursor = mydb.cursor()

# Creating the Table in MySQL Database

mycursor.execute("create table Books (TS TIMESTAMP DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),Title Varchar(255),Price float(23,2),Rating float(23,1))")

# Making the SQL Insert Query

sql = "INSERT INTO Books (Title, Price, Rating) VALUES (%s, %s, %s)"

# Executing Insert Query and using List of Tuple as Values 
mycursor.executemany(sql, Data)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
mydb.close()
        