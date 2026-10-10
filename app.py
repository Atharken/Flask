from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

transactions = [
    {"name": "Part-time job", "amount": 0000,
 "category": "Salary", "type": "income"},
    {"name": "job", "amount": 50000,
 "category": "Salary", "type": "income"},
    {"name": "gig", "amount": -700,
  "category": "Salary", "type": "income"}
                    ]        

@app.route("/")
def home():
    return render_template("home.html")

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

        
        #return redirect(url_for(transaction))
    return render_template("add_transaction.html")
     

if __name__ == "__main__":
    app.run(debug=True)