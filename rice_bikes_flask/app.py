from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import flask_restless
import datetime
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://caderitter@localhost/rice-bikes-dev'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User id: {} username: {}>'.format(self.id, self.username)


class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	email = db.Column(db.String(120))

	transactions = db.relationship('Transaction', 
		backref='customer', lazy='dynamic')
	bikes = db.relationship('Bike', 
		backref='customer', lazy='dynamic')

	def __init__(self, first_name, last_name, email):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email

	def __repr__(self):
		return '<Customer id: {} first name: {} last name: {}>'.format(self.id, self.first_name, self.last_name)


TransactionRepair = db.Table('TransactionRepair',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
    db.Column('repair_id', db.Integer, db.ForeignKey('repair.id'))
)

TransactionItem = db.Table('TransactionItem',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
)

TransactionBike = db.Table('TransactionBike',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id')),
    db.Column('bike_id', db.Integer, db.ForeignKey('bike.id'))
)


class TransactionType(enum.Enum):
	INPATIENT = 'inpatient'
	OUTPATIENT = 'outpatient'
	MERCH = 'merch'


class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(300))
	date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	transaction_type = db.Column(db.Enum(TransactionType))

	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

	repairs = db.relationship('Repair', secondary=TransactionRepair, 
		backref=db.backref('repairs', lazy='dynamic'))
	items = db.relationship('Item', secondary=TransactionItem, 
		backref=db.backref('items', lazy='dynamic'))
	bikes = db.relationship('Bike', secondary=TransactionBike, 
		backref=db.backref('bikes', lazy='dynamic'))


class Bike(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	make = db.Column(db.String(80))
	bike_model = db.Column(db.String(80))
	description = db.Column(db.String(300))

	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))


class Repair(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Integer)
	name = db.Column(db.String(80))
	description = db.Column(db.String(300))


class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Integer)
	name = db.Column(db.String(80))
	description = db.Column(db.String(300))


manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Transaction, methods=['GET', 'POST', 'PUT', 'DELETE'])







