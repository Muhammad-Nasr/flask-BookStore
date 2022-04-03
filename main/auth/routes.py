import os
from main.auth import bp
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from main import db
from main.auth.forms import RegisterForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from main.models import Reader
from flask_login import login_user, login_required, logout_user, current_user
from main.auth.email import send_password_reset_email


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_reader = Reader(username=form.username.data.lower(),
                            email=form.email.data)
        new_reader.add_password(form.password.data)
        flash(message=f'Congrats, you have registered successfully,'
                      f' welcome {new_reader.username}!')
        db.session.add(new_reader)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(os.environ.get('DATABASE_URL'))
    if form.validate_on_submit():
        reader = Reader.query.filter_by(username=form.username.data.lower()).first()

        if reader is None or not reader.check_password(attempted_password=form.password.data):
            flash('Invalid username or password')
            print('no')
            return redirect(url_for('auth.login'))
        print('yes')
        login_user(reader)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index', username=current_user.username)

        return redirect(next_page)

    return render_template('auth/login.html', form=form, title='Sign In!')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        reader = Reader.query.filter_by(email=form.email.data).first()
        if reader:
            print('ok')
            send_password_reset_email(reader)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)



@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    reader = Reader.verify_reset_password_token(token)
    if not reader:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        reader.password = form.password.data
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

