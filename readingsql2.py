import pandas as pd
import sqlite3

conn = sqlite3.connect('CSGO.db')

cursor = conn.cursor()

df = pd.read_sql('Select * From items;', conn)

names = []

def get_Percent_change(old, new):
    return((float(new)-old)/abs(old))*100


otnvalues = []
ntsnvalues = []
def get_change(percent, min_price, contains_or_full):#false = the dataset is alowed a few values below the min price, True = the dataset is allowed no values below the minimum... contains or full applies to both volume and price
    with conn:
        cursor.execute("SELECT DISTINCT name FROM items")
        x = cursor.fetchall()
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
                print("price not sufficeint")
                result = False


            elif 0 in above_price and contains_or_full == False:
                print("a few values below minimum price : PASSING")
                result = True

            elif 0 in above_price and contains_or_full == True:
                print("a few values below minimum: FAILING")
                result = False


            else:
                print("meets criteria perfectly")

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

    print(otnvalues)
    print("\n|||\n")
    print(ntsnvalues)

get_change(10, 10000, False)
