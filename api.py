import os
from flask import Flask, request, json,jsonify,abort
from smtplib import SMTP
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

import socket
import random


app = Flask(__name__)



if __name__=="__main__":
    app.run() 