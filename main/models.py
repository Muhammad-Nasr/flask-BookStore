from flask_login import UserMixin, current_user
from main import db, login_manager, admin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request, current_app
import jwt
from time import time


@login_manager.user_loader
def load_user(id):
    return Reader.query.get(int(id))


reader_book = db.Table('reader_book',
                       db.Column('reader_id', db.Integer, db.ForeignKey('reader.id')),
                       db.Column('book_id', db.Integer, db.ForeignKey('book.id')))

class Reader(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), default='example@email.com')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128), nullable=False)
    books = db.relationship('Book', secondary=reader_book,
                            backref=db.backref('readers', lazy='dynamic'), lazy='dynamic')

    def add_password(self, user_password):
        self.password_hash = generate_password_hash(password=user_password)

    def check_password(self, attempted_password):
        return check_password_hash(self.password_hash, password=attempted_password)

    def avatar(self, size):
        if not self.email:
            self.email = 'example@email.com'
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                digest, size)

    def save(self, book):
        if self.is_saving(book) == False:
            self.books.append(book)

    def remove(self, book):
        if self.is_saving(book):
            self.books.remove(book)

    def is_saving(self, book):
        print(self.books.filter(
            reader_book.c.book_id == book.id))
        return self.books.filter(
            reader_book.c.book_id == book.id).count() > 0

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Reader.query.get(id)

    def __repr__(self):
        return f"<Reader: {self.username}>"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String(100), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    author = db.Column(db.String(100), nullable=False, index=True)
    year = db.Column(db.String(50))
    category = db.Column(db.Text, default=None)
    rating = db.Column(db.Float)
    img_url = db.Column(db.String(500))
    link = db.Column(db.String(500))
    date_added = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"<Book: {self.title}>"


class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(120))
    message = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_active:
            if current_user.id == 1:
                return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index', next=request.url))


class ReaderView(ModelView):
    form_columns = ['id', 'username', 'email','password_hash' , 'last_seen']

    def on_model_change(self, form, model, is_created):
        model.password_hash = generate_password_hash(password=model.password_hash)

    def is_accessible(self):
        if current_user.is_active:
            if current_user.id == 1:
                return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for('main.index', next=request.url))


class BookView(ModelView):

    def is_accessible(self):
        if current_user.is_active:
            if current_user.id == 1:
                return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):

        return redirect(url_for('main.index', next=request.url))


admin.add_view(ReaderView(Reader, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(ModelView(ContactUs, db.session))

