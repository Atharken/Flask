from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/transaction")
def transaction():
    transactions = [
    {"name": "Part-time job", "amount": 0000,
 "category": "Salary", "type": "income"},
    {"name": "job", "amount": 50000,
 "category": "Salary", "type": "income"},
    {"name": "gig", "amount": -700,
  "category": "Salary", "type": "income"}
                    ]        

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
        amount = request.form.get("amount")
        category = request.form.get("category")
        transaction_type = request.form.get("type")

        return f"""
                name : {name} <br>
                amount : {amount} <br>
                categoy : {category} <br>
                type : {transaction_type} 
                """
    return render_template("add_transaction.html")

if __name__ == "__main__":
    app.run(debug=True)