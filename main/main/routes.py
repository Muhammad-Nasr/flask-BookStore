from main.main import bp
from flask_login import current_user, login_required
from main.models import Reader, Book
from datetime import datetime
import requests
from main import db
from flask import render_template, url_for, redirect, request, flash
from main.main.forms import SearchForm, SaveForm, EditForm


URL = 'https://www.googleapis.com/books/v1/volumes?q={}&maxResults=30&country=US'
URL_ID = 'https://www.googleapis.com/books/v1/volumes/{}'


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
@login_required
def index():

    form = SearchForm()
    if form.validate_on_submit():
        save_form = SaveForm()
        search = form.search.data
        try:
            response = requests.get(URL.format(search))

        except requests.exceptions.ConnectionError as r:
            r.status_code = "Connection refused, Please try again later."
        else:
            books = response.json()['items']
            return render_template('main/books.html', books=books, form=save_form)

    return render_template('main/index.html', title='Home', form=form)


@bp.route('/books-index', methods=['GET', 'POST'])
@login_required
def bookshelf():
    form = SaveForm()
    if form.validate_on_submit():
        book_id = request.form.get('book_id')
        book = Book.query.filter_by(book_id=book_id).first()
        if book:
            current_user.save(book)
            db.session.commit()

        else:
            book = requests.get(URL_ID.format(book_id)).json()

            new_book = Book(book_id=book['id'],
                            title=book['volumeInfo']['title'],
                            author=book['volumeInfo']['authors'],

                            year=book['volumeInfo']['publishedDate'] \
                                if book['volumeInfo']['publishedDate'] else None,
                            category = book ['volumeInfo']['categories']\
                            if 'categories' in book ['volumeInfo'] else 'general',


                            img_url=book['volumeInfo']['imageLinks']['smallThumbnail'],
                            link=book['volumeInfo']['infoLink']
                            )

            db.session.add(new_book)
            current_user.save(new_book)
            db.session.commit()

            flash(message=f'congrats, the book {new_book.title} added to your table successfully!')

    return redirect(url_for('main.reader', username=current_user.username))


@bp.route('/reader/<username>')
@login_required
def reader(username):
    reader = Reader.query.filter_by(username=username).first_or_404()
    books = reader.books.all()

    return render_template('main/reader.html', title='My bookshelf', books=books,
                           reader=reader)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditForm(original_name=current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        flash('Your changes have been saved.')
        db.session.commit()
    if request.method == 'GET':
        form.username.data = current_user.username

    return render_template('main/edit_profile.html', title='Edit Profile', form=form)


@bp.route('/delete')
@login_required
def delete():
    book_id = request.args.get('book_id')
    book = Book.query.get(book_id)
    current_user.remove(book)
    flash('you removed the book successfully')
    db.session.commit()
    return redirect(url_for('main.reader', username=current_user.username))







