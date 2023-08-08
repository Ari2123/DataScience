from flask import Blueprint, render_template, request, redirect, url_for
from .models import Expense, db

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    expenses = Expense.query.all()
    return render_template('home.html', expenses=expenses)

@bp.route('/add_expense', methods=['POST'])
def add_expense():
    description = request.form['description']
    amount = request.form['amount']
    expense = Expense(description=description, amount=amount)
    db.session.add(expense)
    db.session.commit()
    return redirect(url_for('main.home'))

