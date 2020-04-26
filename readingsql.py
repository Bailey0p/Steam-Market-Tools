import pandas as pd
import sqlite3

conn = sqlite3.connect('CSGO.db')

cursor = conn.cursor()

df = pd.read_sql('Select * From items;', conn)

names = []

def get_Percent_change(old, new):
    return((float(new)-old)/abs(old))*100

with conn:
    cursor.execute("SELECT DISTINCT name FROM items")
    x = cursor.fetchall()
    for i in x:

        names.append(i[0])

#df = df.sort_values(by=['name'])



# for x in names:
#     print(df[df['name'] == x])
#     print("\n|||\n")

for x in names:
    try:
        data = df[df['name'] == x]

        otn = get_Percent_change(data.iloc[0][2], data.iloc[-1][2])
        ntsn = get_Percent_change(data.iloc[-2][2],data.iloc[-1][2])

        print(otn)
        print(ntsn)
    except IndexError:
        print('INDEX ERROR (the item probably does not have enough data (3 peices minimum)in the db, try adding more )')
