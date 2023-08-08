pip install pytest

def test_calculate_total_expenses():
    expenses = [100, 200, 300]
    assert calculate_total_expenses(expenses) == 600

def test_add_and_retrieve_expense():
    expense = Expense(description="Lunch", amount=15.50)
    add_expense(expense)
    retrieved_expense = get_expense(expense.id)
    assert retrieved_expense.description == "Lunch"
    assert retrieved_expense.amount == 15.50

def test_login():
    browser.get('http://localhost:5000/login')
    username_field = browser.find_element_by_name('username')
    password_field = browser.find_element_by_name('password')
    submit_button = browser.find_element_by_name('submit')
    
    username_field.send_keys('testuser')
    password_field.send_keys('testpassword')
    submit_button.click()
    
    assert "Welcome to the Expense Tracker!" in browser.page_source

def test_negative_expense_amount():
    with pytest.raises(ValueError):
        add_expense(description="Dinner", amount=-10)

def test_validate_date():
    assert validate_date("2023-08-07") == True
    assert validate_date("invalid-date") == False

def test_get_category_by_id():
    category = get_category_by_id(1)
    assert category.name == "Food"

def test_update_expense():
    expense = Expense(description="Dinner", amount=10)
    add_expense(expense)
    expense.amount = 15
    update_expense(expense)
    retrieved_expense = get_expense(expense.id)
    assert retrieved_expense.amount == 15

def test_user_registration_and_login():
    user = User(username="testuser", password="testpass")
    register_user(user)
    assert login_user("testuser", "testpass") == True

def test_delete_expense():
    browser.get('http://localhost:5000/expenses')
    delete_button = browser.find_element_by_id('delete-button-1')
    delete_button.click()
    assert "Expense deleted successfully" in browser.page_source

def test_logout():
    browser.get('http://localhost:5000/logout')
    assert "You have been logged out" in browser.page_source

def test_invalid_login():
    with pytest.raises(AuthenticationError):
        login_user("nonexistentuser", "wrongpass")

def test_get_nonexistent_expense():
    with pytest.raises(ExpenseNotFoundError):
        get_expense(9999)




