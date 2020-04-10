import os
import requests
from flask import Flask, render_template, jsonify, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://tpopdzhrzugoid:22b262b28548fd03634e331c3772909d0724f951f6c263447a8a6f1188ebc671@ec2-3-211-48-92.compute-1.amazonaws.com:5432/dfdvqphj2hds5t"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login_page.html")

@app.route("/trylogin", methods=["POST"])
def trylogin():
    username=request.form.get("luser10")
    password=request.form.get("lpass10")

    us = User.query.filter_by(username=username).first()

    if us is None:
        return render_template("login_error.html", message="No such user is present.")

    if us.password==password:
        return render_template("homepage.html")
    else:
        return render_template("login_error.html", message="Wrong password.")

@app.route("/register")
def register():
    return render_template("registration.html")

@app.route("/registration", methods=["POST"])
def registration():

    # Get form information.
    name = request.form.get("name10")
    email=request.form.get("email10")
    username=request.form.get("user10")
    password=request.form.get("pass10")


    newUser = User(name=name, email=email, username=username, password=password)
    db.session.add(newUser)
    db.session.commit()
    return render_template("success_register.html")

@app.route("/searchIsbn", methods=["POST"])
def searchIsbn():

   
    isbn = request.form.get("isbn10")
    bb = Book.query.filter_by(isbn=isbn).first()

    if bb is None:
        return render_template("api_error.html", message="Book not available!")

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "f8p8EpsmGnEgKLRTunSLGA", "isbns": isbn })
    data=res.json()
    
    if res.status_code != 200:
        return render_template("api_error.html", message=res.status_code)
    
    
    val=data["books"][0].get("average_rating")
    val2=data["books"][0].get("work_reviews_count")
    
    return render_template("api_success.html", title=bb.title , author=bb.author , year=bb.year, rcount=val2 , arating=val)

#CASE INSENSITIVE SEARCH IS func.lower()