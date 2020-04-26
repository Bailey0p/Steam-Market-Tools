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
def get_change(percent, min_price, min_volume):
    with conn:
        cursor.execute("SELECT DISTINCT name FROM items")
        x = cursor.fetchall()
        for i in x:

            names.append(i[0])




    for x in names:
        try:
            data = df[df['name'] == x]



            otn = get_Percent_change(data.iloc[0][2], data.iloc[-1][2])
            ntsn = get_Percent_change(data.iloc[-2][2],data.iloc[-1][2])

            if otn > percent or otn < -percent:
                otnvalues.append(x+": "+str(otn))


            if ntsn > percent or ntsn < -percent:
                ntsnvalues.append(x+": "+str(ntsn))

        except IndexError:
            #print('INDEX ERROR (the item probably does not have enough data (3 peices minimum)in the db, try adding more )')
            pass

    print(otnvalues)
    print("\n|||\n")
    print(ntsnvalues)

get_change(35)
