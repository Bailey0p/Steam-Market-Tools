import sqlite3
import requests
import re
import time
from datetime import datetime
import json

def populatedb():
    try:
        r = requests.get("https://steamcommunity.com/market/search/render/?query=&start=0&count=10&search_descriptions=0&sort_column=popular&norender=1&sort_dir=desc%26count%3D100&appid=730")
        total = r.json()
        total = total["total_count"]
        total = int(total/100)
    except TypeError:
        print(f"TypeError most likely steam search api still on cooldown time: {datetime.now()}")
        print("waiting 5 minutes")
        time.sleep(300)
    for x in range(total+1):#duplicates?
        passed = False
        while passed == False:
            try:
                r = requests.get("https://steamcommunity.com/market/search/render/?query=&start="+str(x*100)+"&count=100&search_descriptions=0&sort_column=popular&currency=21&norender=1&country=AU&sort_dir=desc%26count%3D100&appid=730")
                data = r.json()
                for i in range(100):
                    print("name: "+str(data["results"][i]["name"]))


                    temp_item = csgo_item(data["results"][i]["name"].replace('|', ''), int(datetime.timestamp(datetime.now())), data["results"][i]["sell_price"], data["results"][i]["sell_listings"], data["results"][i]["asset_description"]["icon_url_large"])
                    insert_item(temp_item)
                    conn.commit()
                print("\n")
                passed = True
            except TypeError:
                time.sleep(0.5)
            except IndexError:
                time.sleep(0.5)
    conn.close()



class csgo_item:
    def __init__(self, name, date, lowestsell, sellamount, icon):
        self.name = name
        self.date = date
        self.lowestsell = lowestsell
        self.sellamount = sellamount
        self.icon =icon

conn = sqlite3.connect('CSGO.db')

c = conn.cursor()

def insert_item(item):
    with conn:
        c.execute("INSERT INTO items VALUES (:name, :date, :lowestsell, :sellamount, :icon)", (item.name, item.date, item.lowestsell, item.sellamount, item.icon))


populatedb()
