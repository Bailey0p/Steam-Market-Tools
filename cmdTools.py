import pandas as pd
import sqlite3
import colorama
from colorama import Fore, Back, Style
import requests
import re
import time
from datetime import datetime
import json



colorama.init()

# Print the clear screen code '\033[2J'
print('\033[2J')


print(Fore.MAGENTA+ 'Welcome To CSGO Steam Market Tools'+ Style.RESET_ALL)


conn = sqlite3.connect('CSGO.db')

c = conn.cursor()

df = pd.read_sql('Select * From items;', conn)

names = []

def sif(e):
    return[e[1]]


def get_Percent_change(old, new):
    h = ((float(new)-old)/abs(old))*100
    return round(h, 3)


otnvalues = []
ntsnvalues = []
def get_change(percent, min_price, contains_or_full):#false = the dataset is alowed a few values below the min price, True = the dataset is allowed no values below the minimum... contains or full applies to both volume and price
    with conn:
        c.execute("SELECT DISTINCT name FROM items")
        x = c.fetchall()
        for i in x:

            names.append(i[0])




    for x in names:
        above_price = []
        above_volume = []
        try:
            data = df[df['name'] == x]

            for i in range(len(data)):
                if data.iloc[i][2] <= min_price:
                    above_price.append(0)


                else:
                    above_price.append(1)


            result = True

            # print(above_price.count(0))
            # print(len(above_price))
            if above_price.count(0) == len(above_price):

                result = False


            elif 0 in above_price and contains_or_full == False:

                result = True

            elif 0 in above_price and contains_or_full == True:

                result = False




            if result == True:
                otn = get_Percent_change(data.iloc[0][2], data.iloc[-1][2])
                ntsn = get_Percent_change(data.iloc[-2][2],data.iloc[-1][2])

                if otn > percent or otn < -percent:
                    otnvalues.append(x+": "+str(otn))
                    print(x+": "+str(otn))

                if ntsn > percent or ntsn < -percent:
                    ntsnvalues.append(x+": "+str(ntsn))
                    print(x+": "+str(ntsn))
            else:
                pass

        except IndexError:
            #print('INDEX ERROR (the item probably does not have enough data (3 peices minimum)in the db, try adding more )')
            pass

def makedb():
    try:
        c.execute("""CREATE TABLE items (
                            name text,
                            date integer,
                            lowestsell integer,
                            sellamount integer,
                            icon string
                            )""")

        conn.commit()
    except sqlite3.OperationalError:
        print("Error db already exists")


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

def insert_item(item):
    with conn:
        c.execute("INSERT INTO items VALUES (:name, :date, :lowestsell, :sellamount, :icon)", (item.name, item.date, item.lowestsell, item.sellamount, item.icon))


def boolinput(txt):
    x = input(txt)
    if x == '1':
        return False
    if x == '0':
        return True

def info():
        print(Fore.CYAN + 'Commands:')
        print("1 Make a new database if one does not exist")
        print('2 Populate the database (this can take up to several hours)')
        print("3 Get percent changes of items in the db")
        print("4 exit"+ Style.RESET_ALL)

def start():
    info()
    while True:
        x = input(Fore.GREEN+ "$:"+ Style.RESET_ALL)

        if x == '1':
            makedb()
            info()
        elif x == '2':
            populatedb()
            info()

        elif x == '3':
            min_percent_ = input(Fore.BLUE + "Enter the minimum change in percent: ")
            min_price_ = input("Enter the minimum acceptable price in US cents: ")
            accept_ = boolinput('Enter wheather you want each item to allow a few items under the price limit (0=y, 1=n): '+ Style.RESET_ALL)
            get_change(int(min_percent_), int(min_price_), accept_)
            print(Fore.RED +'Change From Oldest Values To newest Values\n'+ Style.RESET_ALL)
            otnvalues.sort(key=sif)
            ntsnvalues.sort(key=sif)
            print(Fore.YELLOW)
            for x in otnvalues:
                print(x)
            print(Style.RESET_ALL)
            print(Fore.RED +'Change from newest to second newest values\n'+ Style.RESET_ALL)
            print(Fore.YELLOW)
            for x in ntsnvalues:
                print(x)
            print(Style.RESET_ALL)
            info()

        elif x == '4':
            print("exiting...")
            conn.close()
            exit()#or break



#get_change(10, 10000, False)

if __name__ == '__main__':
    start()
