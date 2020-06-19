import pandas as pd
import sqlite3
import colorama
from colorama import Fore, Back, Style
import requests
import re
import time
from datetime import datetime
from datetime import date
import json
import termplotlib as tpl
import numpy

colorama.init()
print('\033[2J')
print(Fore.MAGENTA+ 'Welcome To CSGO Steam Market Tools'+ Style.RESET_ALL)

conn = sqlite3.connect('CSGO.db')

c = conn.cursor()

df = pd.read_sql('Select * From items;', conn)

names = []

currency = "USD"
currency_json = []
currency_list = ['CAD','HKD','ISK','PHP','DKK','HUF','CZK','GBP','RON','SEK','IDR','INR','BRL','RUB','HRK','JPY','THB','CHF','EUR','MYR','BGN','TRY','CNY','NOK','NZD','ZAR','USD','MXN','SGD','AUD','ILS','KRW','PLN']
def get_currency():
    global currency_json
    currency_json = requests.get("https://api.exchangeratesapi.io/latest?base=USD").json()

get_currency()

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
                    i = []
                    i.append(x+": ")
                    i.append(otn)
                    otnvalues.append(i)
                    print(x+": "+str(otn))

                if ntsn > percent or ntsn < -percent:
                    i = []
                    i.append(x+': ')
                    i.append(ntsn)
                    ntsnvalues.append(i)
                    print(x+": "+str(ntsn))
            else:
                pass
        except IndexError:
            print('INDEX ERROR (the item probably does not have enough data (3 peices minimum)in the db, try adding more )')
            pass

class csgo_item:
    def __init__(self, name, date, lowestsell, sellamount, icon):
        self.name = name
        self.date = date
        self.lowestsell = lowestsell
        self.sellamount = sellamount
        self.icon =icon

    def sif(e):
        return[e[1]]#1,2 or 3?

    def info():
            print(Fore.GREEN + "currency is: "+ currency)
            print('Commands:')
            print("1 Make a new database if one does not exist")
            print('2 Populate the database (this can take up to several hours)(requires internet)')
            print("3 Get percent changes of items in the db")
            print("4 do a custom item search")
            print("5 Change the currency (requires internet)")
            print("6 exit"+ Style.RESET_ALL)

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
                        print(Fore.YELLOW+"name: "+str(data["results"][i]["name"])+ Style.RESET_ALL)
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

def insert_item(item):
    with conn:
        c.execute("INSERT INTO items VALUES (:name, :date, :lowestsell, :sellamount, :icon)", (item.name, item.date, item.lowestsell, item.sellamount, item.icon))

def boolinput(txt):
    x = input(txt)
    if x == 'n' or 'N' or 'No' or 'No':
        return False
    if x == 'y' or 'yes' or 'Yes' or 'Yes' :
        return True

def start():
    global currency
    global currency_json
    global currency_list
    csgo_item.info()
    while True:
        x = input("$:")
        if x == '1':
            csgo_item.makedb()
            csgo_item.info()
        elif x == '2':
            x = input(Fore.RED +"WARNING Are you sure you want to continue?\nThis oeration can take up to several hours and aborting partway through\n will result in an incomplete dataset\ny/n?"+ Style.RESET_ALL)
            while True:
                if x == "y":
                    csgo_item.populatedb()
                    csgo_item.info()
                    break
                elif x == "n":
                    csgo_item.info()
                    break
                else:
                    print("Error could not interpret user input")
                    x = input(Fore.RED +"WARNING Are you sure you want to continue?\nThis oeration can take up to several hours and aborting partway through\n will result in an incomplete dataset\ny/n?"+ Style.RESET_ALL)

        elif x == '3':
            min_percent_ = input(Fore.BLUE + "Enter the minimum change in percent: ")
            min_price_ = input("Enter the minimum acceptable price in US cents: ")
            accept_ = boolinput('Enter wheather you want each item to allow a few items under the price limit (0=y, 1=n): '+ Style.RESET_ALL)
            get_change(int(min_percent_), int(min_price_), accept_)
            print(Fore.RED +'Change From Oldest Values To newest Values\n'+ Style.RESET_ALL)
            otnvalues.sort(key=csgo_item.sif)
            ntsnvalues.sort(key=csgo_item.sif)
            print(Fore.YELLOW)
            for x in otnvalues:
                print(x)
            print(Style.RESET_ALL)
            print(Fore.RED +'Change from newest to second newest values\n'+ Style.RESET_ALL)
            print(Fore.YELLOW)
            for x in ntsnvalues:
                print(x)
            print(Style.RESET_ALL)
            csgo_item.info()

        elif x =='4':
            x2 = []
            y2 = []

            name = input("Please Enter an items name:\n")
            name = name.replace("|",'')
            with conn:
                c.execute("SELECT * FROM items WHERE name=:name",{'name':name})
                data = c.fetchall()
            if len(data) == 0:
                print(Fore.RED +"Sorry could no find that item in the database\nPLEASE INCLUDE THE CONDITION IN BRACKETS\nAK-47 | Uncharted becomes\nAK-47  Uncharted (Field-Tested)"+ Style.RESET_ALL)
                continue
            hc = False
            colour = False
            nint = 0
            for x in data:
                y2.append(round((x[2]/100)*currency_json['rates'][currency],2))
                x2.append(nint)
                nint += 1
                add = 0
                if hc == False:
                    print("        Date        |"+"Price "+"| Volume")
                    hc = True
                if colour == False:
                    print(Fore.CYAN,end='')
                    colour = True
                elif colour == True:
                    print(Fore.BLUE,end='')
                    colour = False
                print(str(datetime.fromtimestamp(x[1]))+" | "+str(round((x[2]/100)*currency_json['rates'][currency],2))+" | "+str(x[3]))
                print(Style.RESET_ALL,end='')
            fig = tpl.figure()
            fig.plot(x2, y2, label="price", width=120, height=30)
            fig.show()
            csgo_item.info()

        elif x == '5':
            print("Please Select a currency (Enter 3-Letter Tag)")
            print("1  CAD\n2  HKD\n3  ISK\n4  PHP\n5  DKK\n6  HUF\n7  CZK\n8  GBP\n9  RON\n10 SEK\n11 IDR\n12 INR\n13 BRL\n14 RUB\n15 HRK\n16 JPY\n17 THB\n18 CHF\n19 EUR\n20 MYR\n21 BGN\n22 TRY\n23 CNY\n24 NOK\n25 NZD\n26 ZAR\n27 USD\n28 MXN\n29 SGD\n30 AUD\n31 ILS\n32 KRW\n33 PLN")
            i = input("?: ")
            if i in currency_list:
                currency = i
            get_currency()
            csgo_item.info()

        elif x == '6':
            print("exiting...")
            conn.close()
            exit()

if __name__ == '__main__':
    start()
