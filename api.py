import os
from flask import Flask, request, json,jsonify,abort
from smtplib import SMTP
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

import socket
import random


app = Flask(__name__)
db = SQLAlchemy(app)
class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(32), primary_key=True)
    fullname = db.Column(db.String(32), index=True)
    username = db.Column(db.String(32), index=True)
    phone_no = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(64))

db.create_all()
@app.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email")
    username = request.json.get("username")
    fullname = request.json.get("fullname")
    phone_no = request.json.get("phone_no")
    password = request.json.get("password")
    if username is None or password is None or phone_no is None or email is None or fullname is None:
        return jsonify({"message":"parameters can not be empty"}),400
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"message":"username already exists"}),400
    if User.query.filter_by(phone_no=phone_no).first() is not None:
        return jsonify({"message":"phone number already exists"}),400
    if User.query.filter_by(email=email).first() is not None:
         return jsonify({"message":"email already exists"}),400
    new_user = User(username=username,email=email, password=password, fullname=fullname, phone_no=phone_no)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":
    {
        "email": email,
        "phone_no": phone_no,
        "username": username,
        "fullname": fullname,
        "password": password
    }
          }), 201

@app.route("/login", methods=["POST"])
def login ():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    existing_user = User.query.filter_by(username=username, password=password).first()
    if not existing_user:
        return (jsonify({"message":"incorect username or password"})), 404
    return (jsonify({"message":
    {
        "username": username,
        "password": password
    }
    })), 200




if __name__=="__main__":
    app.run() 