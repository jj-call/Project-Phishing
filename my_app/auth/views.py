from flask import render_template, request, flash, redirect, url_for
from markupsafe import Markup
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from my_app.forms import LoginForm, RegistrationForm
from my_app.models import User
from my_app import db
from . import bp
import logging

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('simulation.base'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('simulation.base')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    logging.info("Register route hit")
    username = request.form.get('username')
    logging.debug(f"Attempting to register username: {username}")
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_exists = User.query.filter_by(username=username).first()

        if user_exists:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('auth.register'))

        try:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()

            flash('Your account has been created! You can now login.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()  # Rollback the transaction on error
            flash('An error occurred during registration. Please try again later.')
            return redirect(url_for('auth.register'))
        
    logging.info("Finished registration process")
    return render_template('auth/register.html', form=form)


