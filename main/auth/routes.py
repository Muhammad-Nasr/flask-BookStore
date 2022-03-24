from main.auth import bp
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from main import db
from main.auth.forms import RegisterForm, LoginForm
from main.models import Reader
from flask_login import login_user, login_required, logout_user, current_user


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_reader = Reader(username=form.username.data,
                            email=form.email.data)
        new_reader.add_password(form.password.data)
        flash(message=f'Congrats, you have registered successfully,'
                      f' welcome {new_reader.username}!')
        db.session.add(new_reader)
        db.session.commit()
        login_user(new_reader)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        reader = Reader.query.filter_by(username=form.username.data).first()

        if reader is None or not reader.check_password(attempted_password=form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(reader)
        flash(message=f'congrats, you logged in successfully/'
                      f'welcome  {reader.username}.')

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
