from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sqlite3

from flask_sqlalchemy import SQLAlchemy#

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CSGO.db'
# db = SQLAlchemy(app)
#
# db.Model.metadata.reflect(db.engine)
#
# class Items(db.Model):
#     __tablename__ = 'items'
#     __table_args__ = { 'extend_existing': True }
#     _rowid_ = db.Column(db.Integer, primary_key=True)

conn = sqlite3.connect('CSGO.db',check_same_thread=False)

c = conn.cursor()

class csgo_item:
    def __init__(self, name, date, lowestsell, sellamount, icon):
        self.name = name
        self.date = date
        self.lowestsell = lowestsell
        self.sellamount = sellamount
        self.icon =icon

def get_items_by_name(name):
    c.execute("SELECT * FROM items WHERE name=:name", {'name': name})
    return c.fetchall()

def get_Percent_change(old, new):
    number = ((float(new)-old)/abs(old))*100
    return round(number, 3)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        thing = request.form['Search']
        print(thing)
        return redirect('/item/:thing',{'thing':thing})
    else:
        return render_template('index.html')

@app.route('/Table', methods=['GET', 'POST'])
def Table():

    return render_template('Table.html')

@app.route('/item/<x>')
def detail(x):
    try:
        c.execute("SELECT * FROM items WHERE name=:name", {'name': x})
        h = c.fetchall()

        dates = []
        price = []
        amount = []
        oldest_change = get_Percent_change(h[0][2],h[-1][2])
        newest_change = get_Percent_change(h[-2][2],h[-1][2])
        for x in h:
            dates.append(datetime.fromtimestamp(x[1]))
            price.append(x[2]/100)
            amount.append(x[3])
    except:
        return "404"

    return render_template('thing.html', date_data=dates, price_data=price, amount_data=amount, alldata=h, oldest_change=oldest_change, newest_change=newest_change)





# db.create_all()
if __name__ == "__main__":
    app.run(debug=True)
