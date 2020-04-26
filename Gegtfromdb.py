import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import json


class csgo_item:
    def __init__(self, name, date, lowestsell, sellamount, classid, instanceid, currency, icon, id):
        self.name = name
        self.date = date
        self.lowestsell = lowestsell
        self.sellamount = sellamount
        self.classid = classid
        self.instanceid = instanceid
        self.currency = currency
        self.icon =icon
        self.id = id


conn = sqlite3.connect('CSGO.db')

c = conn.cursor()

def insert_item(item):
    with conn:
        c.execute("INSERT INTO items VALUES (:name, :date, :lowestsell, :sellamount, :classid, :instanceid, :currency, :icon, :id)", (item.name, item.date, item.lowestsell, item.sellamount, item.classid, item.instanceid, item.currency, item.icon, item.id))


def get_items_by_name(name):
    c.execute("SELECT * FROM items WHERE name=:name", {'name': name})
    return c.fetchall()

def get_items_by_date(date):
    c.execute("SELECT * FROM items WHERE date=:date", {'date': date})
    return c.fetchall()



def sortTuple(Tup):
    lst = len(Tup)
    for i in range(0, lst):
        for j in range(0, lst-i-1):
            if (Tup[j][1]> Tup[j+1][1]):
                temp = Tup[j]
                Tup[j] = Tup[j+1]
                Tup[j+1] = temp
    return Tup

def get_Percent_change(old, new):
    return((float(new)-old)/abs(old))*100



pricelist = []

#start_time = time.time()


def getalldata():
    listofnames = []

    with conn:
        c.execute("SELECT name FROM items GROUP BY name")
        x = c.fetchall()

        l = time.perf_counter()
        print(f'Got names from db at{l}')
        print("now appending to the list...")

        for h in x:
            listofnames.append(h[0])

        l = time.perf_counter()
        print(f'added names to the list at {l}')
        print("now getting data for each name...")



    for x in listofnames:# about 15185
        with conn:
            c.execute("SELECT DISTINCT * FROM items WHERE name = :x",{"x":x})
            allofitem = sortTuple(c.fetchall())#all data for that name


            print(f"selected name and sorted name: {x}")
            print("getting percent change...")
            lastunit = int(len(allofitem)-1)#position of the last time data was recorded

            i = []
            i.append(allofitem[0][0])#add the first peice of datas name, ie get the name
            i.append(get_Percent_change(allofitem[0][2],allofitem[lastunit][2]))#get the percentage difference between the oldest and the newest item
            print("Got percent change")
            l = time.perf_counter()
            print(f'this item completed at:{l}')



            pricelist.append(i)#add that list to a list

            #print("time: "+str(time.time() - start_time))


def sif(e):
    return[e[1]]

start = time.perf_counter()

getalldata()

pricelist.sort(reverse=True,key=sif)

finish = time.perf_counter()

print(f'finished in {round(finish-start, 2)}')

for x in pricelist:
    print(x)
