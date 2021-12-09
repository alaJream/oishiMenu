from flask import Flask, redirect, url_for, render_template, request, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os



app = Flask(__name__)

host = os.environ.get('DB_URL')
client = MongoClient(host=host)
db = client.orderapp
order = db.order

app.secret_key = "asdf4asdf"
# app.permanent_session_lifetime = timedelta(minutes=30)


@app.route("/")
def home():
    return render_template('index.html')

# ----------------------User Login----------------------------

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        # session.permanent = True
        user = request.form["nm"]
        session["user"] = user


        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("You are already logged in!")
            return redirect(url_for("user"))

        return render_template('login.html')

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You must log in to place an order!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("Thanks for visiting! You have been logged out!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

#------------------------------------------------------------

# Create and submit an order
@app.route('/order')
def order_index():
    return render_template('index.html')


# Form to add new order and fill out 
@app.route('/order/new')
def order_new():
    return render_template('order_new.html', title='New Order')


@app.route('/order', methods=['POST'])
def order_submit():
    order = {
        'note_name': request.form.get('dname'),
        'note_content': request.form.get('desc'),
        'date': request.form.get('date'),
    }
    order.insert_one(order)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)



    