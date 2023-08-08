from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Expense, db, User
from werkzeug.security import generate_password_hash

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

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


