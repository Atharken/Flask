from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)



transactions = [
    {"name": "Part-time job", "amount": 0,
 "category": "Salary", "type": "income"},       # main data collector temp
    {"name": "job", "amount": 50000,
 "category": "Salary", "type": "income"},
    {"name": "gig", "amount": -700,
  "category": "Salary", "type": "income"},
  {"name": "test", "amount": 12000,
    "category": "testing", "type": "expense"}
                    ]        

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

    if request.method == "POST":
        name = request.form.get("name")
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        transaction_type = request.form.get("type")

        new_transaction = {
            "name" : name,
            "amount" : amount,
            "category" : category,
            "type" : transaction_type,
        }

        transactions.append(new_transaction)

    return render_template("add_transaction.html")

@app.route("/remove/<int:index>", methods =["POST"])
def remove(index):

    transactions.pop(index)

    return redirect(url_for('transaction'))

@app.route("/summary")
def summary():
    high = 0

    exp = None

    for i in transactions:
        if i['type'] == "expense" and high < i["amount"]:
                high = i['amount'] 
                exp = i['name']

    return render_template("summary.html",
                           high = high,
                           exp = exp)
     

if __name__ == "__main__":
    app.run(debug=True)