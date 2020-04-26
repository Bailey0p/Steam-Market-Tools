import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import json

conn = sqlite3.connect('CSGO.db')

c = conn.cursor()

with conn:
    c.execute("SELECT COUNT(*) FROM items")
    x = c.fetchall()
    h = x[0][0]
