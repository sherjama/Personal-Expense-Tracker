import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, redirect, url_for
from flask import request, flash
from flask import make_response



from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from reportlab.pdfgen import canvas


from config import Config
from models import db
from models import User
from models import Transaction

import matplotlib.pyplot as plt
import os
import io

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash('Registration Successful')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Invalid Credentials')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():

    transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).all()

    income = sum(
        t.amount for t in transactions if t.type == 'Income'
    )

    expense = sum(
        t.amount for t in transactions if t.type == 'Expense'
    )

    balance = income - expense

    return render_template(
        'dashboard.html',
        transactions=transactions,
        income=income,
        expense=expense,
        balance=balance
    )

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():

    if request.method == 'POST':

        transaction = Transaction(
            type=request.form['type'],
            category=request.form['category'],
            amount=float(request.form['amount']),
            description=request.form['description'],
            user_id=current_user.id
        )

        db.session.add(transaction)
        db.session.commit()

        flash('Transaction Added')

        return redirect(url_for('dashboard'))

    return render_template('add_transaction.html')


@app.route('/delete/<int:id>')
@login_required
def delete_transaction(id):

    transaction = Transaction.query.get_or_404(id)

    db.session.delete(transaction)
    db.session.commit()

    flash('Transaction Deleted')

    return redirect(url_for('dashboard'))

@app.route('/analytics')
@login_required
def analytics():

    transactions = Transaction.query.filter_by(
        user_id=current_user.id,
        type='Expense'
    ).all()

    categories = {}

    for t in transactions:
        if t.category in categories:
            categories[t.category] += t.amount
        else:
            categories[t.category] = t.amount

    # If no data
    if len(categories) == 0:
        return render_template('analytics.html', chart=None)


    plt.figure(figsize=(6,6))
    plt.pie(
        categories.values(),
        labels=categories.keys(),
        autopct='%1.1f%%'
    )
    chart_path = 'static/charts/pie_chart.png'
    plt.savefig(chart_path)
    plt.close()

    plt.figure(figsize=(7,5))

    plt.bar(categories.keys(), categories.values())
    
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.title("Expense by Category")
    
    bar_path = 'static/charts/bar_chart.png'
    plt.savefig(bar_path)
    plt.close()
    
    return render_template('analytics.html', chart=chart_path,bar=bar_path)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(id):

    transaction = Transaction.query.get_or_404(id)

    if request.method == 'POST':

        transaction.type = request.form['type']
        transaction.category = request.form['category']
        transaction.amount = float(request.form['amount'])
        transaction.description = request.form['description']

        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('edit_transaction.html', t=transaction)

@app.route('/search')
@login_required
def search():

    query = request.args.get('q')

    transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.category.like(f"%{query}%")
    ).all()

    return render_template(
        'dashboard.html',
        transactions=transactions,
        income=0,
        expense=0,
        balance=0
    )


@app.route('/download')
def download():

    transactions = Transaction.query.all()

    pdf = "Expense Report Generated"

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'

    return response

@app.route('/download_pdf')
@login_required
def download_pdf():

    transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).all()

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    y = 800

    p.setFont("Helvetica", 12)
    p.drawString(200, 820, "Expense Report")

    for t in transactions:

        text = f"{t.type} | {t.category} | {t.amount} | {t.description}"
        p.drawString(50, y, text)
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()

    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'

    return response

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    if __name__ == "__main__":
        app.run(debug=False) 