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
    category_type = {}

    highest_category = ""
    highest_amount = 0

    lowest_category = ""


    for i in transactions:
        if i['category'] in category_type:
            category_type[i['category']] += i['amount']
        else:
            category_type[i['category']] = i['amount']

    if category_type:
      lowest_category = list(category_type.keys())[0]
      lowest_amount = list(category_type.values())[0]
    else:
      lowest_category = ""
      lowest_amount = 0
      
    lowest_amount = list(category_type.values())[0]

    for name,amount in category_type.items():
        if highest_amount < amount:
            highest_amount = amount
            highest_category = name
        if lowest_amount > amount:
            lowest_category = name
            lowest_amount = amount




    return render_template("home.html",
                          category_type = category_type,
                          highest_amount = highest_amount,
                           highest_category = highest_category,
                           lowest_category = lowest_category,
                           lowest_amount = lowest_amount)      #home page nothing special 

@app.route("/transaction")
def transaction():
   

    balance = 0
    for i in transactions:
        if i['type'] == "income":
          balance += i['amount'] 
        elif i['type'] == "expense":
          balance -= i['amount'] 

    return render_template("transaction.html",
                           transactions = transactions,
                           balance = balance)

@app.route("/add", methods = ["GET","POST"])
def add_transaction():
    success = False
    if request.method == "POST":
        name = request.form.get("name")
        amount_str = float(request.form.get("amount"))
        try:
            amount = float(amount_str)
        except ValueError:
            amount = 0
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

    rewrite(transactions)

    return redirect(url_for('transaction'))

@app.route("/edit/<int:index>", methods = ['POST','GET'])
def edit(index):   
    
    tx = transactions[index]
    
    if request.method == "POST":      #get the new data updated       
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
                           earn =earn,)
if __name__ == "__main__":
    app.run(debug=True)