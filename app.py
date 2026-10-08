from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/transaction")
def transaction():
    income = 100
    expense = 100
    balance = income - expense
    return f"transactions\nincome-{income} expense-{expense} balance-{balance}"

if __name__ == "__main__":
    app.run(debug=True)