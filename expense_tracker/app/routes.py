from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Expense, db, User, Category
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to the main page
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@bp.route('/expenses', methods=['GET', 'POST'])
def expenses():
    user_id = session.get('user_id')

    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        category_id = request.form.get('category_id')

        expense = Expense(description=description, amount=amount, date=date, user_id=user_id, category_id=category_id)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')

    user_expenses = Expense.query.filter_by(user_id=user_id).all()
    categories = Category.query.all()
    return render_template('expenses.html', expenses=user_expenses, categories=categories)

