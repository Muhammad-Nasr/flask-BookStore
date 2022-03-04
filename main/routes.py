import requests
from main import app, db
from flask import render_template, url_for, redirect, request, flash
from main.forms import SearchForm, RegisterForm, LoginForm, SaveForm
from flask_login import current_user, login_user, logout_user, login_required
from main.models import Reader, Book
from werkzeug.urls import url_parse

URL = 'https://www.googleapis.com/books/v1/volumes?q={}&maxResults=20&country=US'
NEW_URL = 'https://www.googleapis.com/books/v1/volumes?q=subject+{}:keys&maxResults=20&country=US'
URL_ID = 'https://www.googleapis.com/books/v1/volumes/{}'


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        save_form = SaveForm()
        search = form.search.data
        response = requests.get(NEW_URL.format(search))
        books = response.json()['items']

        for book in books:
            print(book['id'])
            print(book['volumeInfo'].keys())

            # print(book['volumeInfo']['imageLinks']['smallThumbnail'])
        return render_template('books.html', books=books, form=save_form)

    return render_template('index.html', title='Home', form=form)


@app.route('/books-index', methods=['GET', 'POST'])
def bookshelf():
    form = SaveForm()
    if form.validate_on_submit():
        print('save')

        if not current_user.is_authenticated:
            print(current_user)
            print('not current user')
            flash(
                'Ok, we need you to sign in till save your books,, so you need to register to save your books in a '
                'personal bookshlf')

            return redirect(url_for('register'))

        print('ok')
        book_id = request.form.get('book_id')
        print(book_id)
        print(current_user)

        book = requests.get(URL_ID.format(book_id)).json()

        new_book = Book(book_id=book['id'],
                        title=book['volumeInfo']['title'],
                        author=book['volumeInfo']['authors'],

                        year=book['volumeInfo']['publishedDate'] \
                            if book['volumeInfo']['publishedDate'] else None,
                        category = book ['volumeInfo']['categories']\
                        if 'categories' in book ['volumeInfo'] else 'general',


                        img_url=book['volumeInfo']['imageLinks']['smallThumbnail'],
                        link=book['volumeInfo']['infoLink'],
                        reader=current_user)

        db.session.add(new_book)
        db.session.commit()
        flash(message=f'congrats, the book {new_book.title} added to your table successfully!')

        return redirect(url_for('reader', username=current_user.username))

    return redirect(url_for('index'))


@app.route('/reader/<username>')
@login_required
def reader(username):
    reader = Reader.query.filter_by(username=username).first_or_404()
    books = reader.books.all()
    print(reader.books)
    return render_template('reader.html', title='My bookshelf', books=books)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_reader = Reader(username=form.username.data,
                            email=form.email.data)
        new_reader.add_password(form.password.data)
        flash(message=f'great welcome {new_reader.username}')
        db.session.add(new_reader)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        reader = Reader.query.filter_by(username=form.username.data).first()

        if reader is None or not reader.check_password(attempted_password=form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(reader)
        flash(message=f'congrats, you logged in successfully/'
                      f'welcome  {reader.username}.')

        next_page = request.args.get('next')
        username = request.args.get('username')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('reader', username=current_user.username)

        return redirect(next_page)

    return render_template('login.html', form=form, title='Sign In!')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
