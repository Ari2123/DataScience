from flask import Blueprint, render_template, request, redirect, url_for, flash, session, Response
from .models import Expense, db, User, Category
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import csv
from functools import wraps

bp = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
def home():
    expenses = Expense.query.all()
    return render_template('home.html', expenses=expenses)

@bp.route('/add_expense', methods=['POST'])
@login_required
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
            return redirect(url_for('main.home'))  # Redirect to the main page
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@bp.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    category_id = request.args.get('category_id')
    user_id = session.get('user_id')

    if category_id:
        user_expenses = Expense.query.filter_by(user_id=user_id, category_id=category_id).all()
    else:
        user_expenses = Expense.query.filter_by(user_id=user_id).all()

    categories = Category.query.all()

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

@bp.route('/expenses/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    categories = Category.query.all()

    if request.method == 'POST':
        expense.description = request.form['description']
        expense.amount = float(request.form['amount'])
        expense.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        expense.category_id = request.form.get('category_id')
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('expenses'))

    return render_template('edit_expense.html', expense=expense, categories=categories)

@bp.route('/expenses/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('expenses'))

@bp.route('/expenses/export/csv', methods=['GET'])
@login_required
def export_expenses_csv():
    user_id = session.get('user_id')
    user_expenses = Expense.query.filter_by(user_id=user_id).all()

    def generate():
        data = [["Description", "Amount", "Date", "Category"]]
        for expense in user_expenses:
            category_name = expense.category.name if expense.category else "No Category"
            data.append([expense.description, expense.amount, expense.date.strftime('%Y-%m-%d'), category_name])

        writer = csv.writer(Response(mimetype='text/csv'))
        for row in data:
            yield ','.join(row) + '\n'

    return Response(generate(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=expenses.csv'})

