from flask import Flask, render_template, request, redirect, url_for
from datetime import date,timedelta
import csv
from pathlib import Path

app = Flask(__name__)

headers = ["name","amount","category","type","date"]
def rewrite(x):
    with open("data.csv", "w",newline="") as f:
        w = csv.DictWriter(f,fieldnames=headers)
        w.writeheader()
        w.writerows(x)




p = Path('data.csv')


if not p.exists():
    with open("data.csv", "w", newline="") as f:
        w = csv.DictWriter(f,fieldnames=headers)
        w.writeheader()




transactions = [      ]        

with open("data.csv", "r", newline="") as f:
    r = csv.DictReader(f)
    for i in r:
        temp = {"name" : i['name'],"amount" : float(i['amount']),"category" : i['category'],"type" : i['type'],"date" : i['date']}
        transactions.append(temp)


@app.route("/")
def home():
    return render_template("home.html")         #home page nothing special 

@app.route("/transaction")
def transaction():
   

    balance = 0
    for i in transactions:
        balance += i['amount'] 

    return render_template("transaction.html",
                           transactions = transactions,
                           balance = balance)

@app.route("/add", methods = ["GET","POST"])
def add_transaction():
    success = False
    if request.method == "POST":
        name = request.form.get("name")
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        transaction_type = request.form.get("type")

        current_date = str(date.today())

        new_transaction = {
            "name" : name,
            "amount" : amount,
            "category" : category,
            "type" : transaction_type,
            "date" : current_date
        }

        with open("data.csv","a",newline="") as f:
            w = csv.DictWriter(f,fieldnames=headers)
            w.writerow(new_transaction)

        transactions.append(new_transaction)
        success = True

    return render_template("add_transaction.html",success = success)

@app.route("/remove/<int:index>", methods =["POST"])
def remove(index):

    transactions.pop(index)

    with open("data.csv", "w",newline="") as f:
        w = csv.DictWriter(f,fieldnames=headers)
        w.writeheader()
        w.writerows(transactions)

    return redirect(url_for('transaction'))

@app.route("/edit/<int:index>", methods = ['POST','GET'])
def edit(index):   
    
    tx = transactions[index]
    
    if request.method == "POST":      #get the new data updated 
       if request.method == "POST":      
        transactions[index]['name'] = request.form.get("name")
        transactions[index]['amount'] = float(request.form.get("amount"))      
        transactions[index]['category'] = request.form.get("category")
        transactions[index]['type'] = request.form.get("type")

        rewrite(transactions)

        return redirect(url_for('transaction'))

    return render_template("edit.html", transactions = transactions, index = index) # when user click on edit button




@app.route("/summary")
def summary():
    high = 0

    highin = 0 

    earn = None

    exp = None

    for i in transactions:
        if i['type'] == "expense" and high < i["amount"]:
            high = i['amount'] 
            exp = i['name']

        if i['type'] == "income" and highin< i['amount']:
            highin = i['amount']
            earn = i['name']



    return render_template("summary.html",
                           high = high,
                           exp = exp,
                           highin = highin,
                           earn =earn)
     

if __name__ == "__main__":
    app.run(debug=True)