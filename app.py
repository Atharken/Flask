from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/transaction")
def transaction():
    transactions = [
    {"name": "Part-time job", "amount": 5000,
 "category": "Salary", "type": "income"},
    {"name": "job", "amount": 50000,
 "category": "Salary", "type": "income"}
                    ]        

    return render_template("transaction.html",
                           transactions = transactions)

if __name__ == "__main__":
    app.run(debug=True)