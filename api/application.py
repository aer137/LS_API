"""
    LoanStreet
    Loan server deliverable
    by Anna Rekow

"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json

from flask_cors import CORS

app = Flask(__name__)  # set up flask

CORS(app)

# configure database - create db data.db in same directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

# define the things we want to store in db as models
class Loan(db.Model):  # Model has built in functionalities
    # properties of a loan
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    length_in_months = db.Column(db.Integer, nullable=False)
    monthly_payment = db.Column(db.Float, nullable=False)
    def __repr__(self):
        # overwrite repr[esent] method, for when we want to print the loan data
        return f"${self.amount} - {self.length_in_months} months"

# set up endpoint
@app.route('/')

# define method we want hit when someone visits route
def index():
    return 'Hello!'


@app.route('/loans')
# get - plural
def get_loans():
    loans = Loan.query.all()
    output = []
    for loan in loans:
        loan_data = {
            'amount' : loan.amount, 
            'interest_rate' : loan.interest_rate,
            'length_in_months' : loan.length_in_months,
            'monthly_payment' : loan.monthly_payment
        }
        output.append(loan_data)
    return {"loans": output}


@app.route('/loans/<id>')
# get - singular
def get_loan(id):
    loan = Loan.query.get_or_404(id)
    return {
            'amount' : loan.amount, 
            'interest_rate' : loan.interest_rate,
            'length_in_months' : loan.length_in_months,
            'monthly_payment' : loan.monthly_payment
        }


@app.route('/loans', methods=['POST'])
# post
def add_loan():
    loan = Loan(
        amount=request.json['amount'], 
        interest_rate=request.json['interest_rate'],
        length_in_months=request.json['length_in_months'],
        monthly_payment=request.json['monthly_payment']
    )
    db.session.add(loan)
    db.session.commit()
    return {'id' : loan.id}


@app.route('/loans/<id>', methods=['PUT'])
# put
def modify_loan(id):
    loan = Loan.query.get_or_404(id)
    req = request.json
    keys = ["amount", "interest_rate", "length_in_months", "monthly_payment"]
    for key in keys:
        if key in req:
            setattr(loan, key, req[key])

    db.session.commit()
    return {'id' : loan.id}

@app.route('/loans/<id>', methods=['DELETE'])
# delete
def delete_loan(id):
    loan = Loan.query.get(id)
    if loan is None:
        return {"error" : "not found"}
    db.session.delete(loan)
    db.session.commit()
    return {"message" : "yeet deleted"}


app.run(host='0.0.0.0', port=80)
