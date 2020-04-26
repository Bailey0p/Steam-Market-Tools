from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sqlite3

from flask_sqlalchemy import SQLAlchemy#

app = Flask(__name__)

conn = sqlite3.connect('CSGO.db',check_same_thread=False)

c = conn.cursor()

class csgo_item:
    def __init__(self, name, date, lowestsell, sellamount, icon):
        self.name = name
        self.date = date
        self.lowestsell = lowestsell
        self.sellamount = sellamount
        self.icon =icon


c.execute("SELECT * FROM items WHERE name=:name", {'name': 'Prisma 2 Case'})
h = c.fetchall()
print(str(h))
