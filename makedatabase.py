import sqlite3


conn = sqlite3.connect('CSGO.db')

c = conn.cursor()

c.execute("""CREATE TABLE items (
                    name text,
                    date integer,
                    lowestsell integer,
                    sellamount integer,
                    icon string
                    )""")

conn.commit()
conn.close()
