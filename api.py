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


if __name__=="__main__":
    app.run() 