import os
from flask import Flask, request, json,jsonify,abort
from smtplib import SMTP
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

import socket
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'divineayomi@gmail.com',
    MAIL_PASSWORD = 'erioluwa',
))
api = swagger.docs(Api(app), apiVersion='0.1')
db = SQLAlchemy(app)
mail = Mail(app)
mail.init_app(app)
class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(32), primary_key=True)
    fullname = db.Column(db.String(32), index=True)
    username = db.Column(db.String(32), index=True)
    phone_no = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(64))
class History(db.model):
    amount_paid =  db.Column(db.String(32))
    person_paid =  db.Column(db.String(32))
    payment_description = db.Column(db.String(32))

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


def randpass():
    new = (random.randint (1000, 9000))
    return new


@app.route('/reset', methods=["POST"])
def reset_password_request():
    email = request.json.get("email")
    client = User.query.filter_by(email=email).first()
    if client:
        new_pass = (random.randint (1000, 9000))
        print(new_pass)
        User.query.filter_by(email=email).update({
            'email': email,
            'password': new_pass})
        db.session.commit()
        msg = Message('Reset your password',
                sender="divineayomi@gmail.com",
                recipients=[email],
                body="your new password is " + str(new_pass)
                )       
        mail.send(msg)
        return jsonify ({"message:":"mail sent"}), 200       
    return jsonify ({"message:":"something is not right please check you email or internet connectivity"}), 400     

@app.route('/pay', methods=["POST"])
def pay():
    amount_paid =  request.json.get("amount_paid")
    person_paid =  request.json.get("person_paid")
    payment_description = request.json.get("payment_description")
    submit_history = History(amount_paid=amount_paid, person_paid=person_paid,payment_description=payment_description)
    db.session.add(submit_history)
    db.session.commit()
    return jsonify({"message":
    {
        "amount_paid": amount_paid,
        "person_paid": person_paid,
        "payment_description":payment_description,
    }
          }), 201

if __name__=="__main__":
    app.run()