from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from app.models import db, User, Investment
from datetime import datetime
from werkzeug.security import generate_password_hash
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username already exists')
            return redirect(url_for('main.register'))
        user = User(username=request.form['username'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/')
@login_required
def index():
    investments = Investment.query.filter_by(user_id=current_user.id).all()
    
    # Calculate statistics
    stats = {
        'total_investments': len(investments),
        'total_value': sum(inv.current_value or 0 for inv in investments),
        'total_initial': sum(inv.amount or 0 for inv in investments),
    }
    
    # Calculate average ROI
    if stats['total_investments'] > 0:
        total_roi = sum(inv.calculate_roi() for inv in investments)
        stats['average_roi'] = total_roi / stats['total_investments']
    else:
        stats['average_roi'] = 0
    
    return render_template('dashboard.html', investments=investments, stats=stats)

@main.route('/add_investment', methods=['GET', 'POST'])
@login_required
def add_investment():
    if request.method == 'POST':
        try:
            investment = Investment(
                name=request.form['name'],
                amount=float(request.form['amount']),
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
                current_value=float(request.form['amount']),
                notes=request.form.get('notes', ''),
                user_id=current_user.id
            )
            db.session.add(investment)
            db.session.commit()
            flash('Investment added successfully!')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'Error adding investment: {str(e)}')
            return redirect(url_for('main.add_investment'))
    return render_template('add_investment.html')

@main.route('/update_investment/<int:id>', methods=['POST'])
@login_required
def update_investment(id):
    investment = Investment.query.get_or_404(id)
    if investment.user_id != current_user.id:
        flash('Unauthorized access')
        return redirect(url_for('main.index'))
    
    try:
        investment.current_value = float(request.form['current_value'])
        if request.form.get('end_date'):
            investment.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        
        db.session.commit()
        flash('Investment updated successfully!')
    except Exception as e:
        flash(f'Error updating investment: {str(e)}')
    
    return redirect(url_for('main.index'))