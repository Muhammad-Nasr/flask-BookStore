from flask_login import UserMixin
from main import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


@login_manager.user_loader
def load_user(id):
    return Reader.query.get(int(id))


class Reader(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    books = db.relationship('Book', backref='reader', lazy='dynamic')

    def add_password(self, user_password):
        self.password_hash = generate_password_hash(password=user_password)

    def check_password(self, attempted_password):
        return check_password_hash(self.password_hash, password=attempted_password)

    def avatar(self):
        def avatar(self, size):
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                digest, size)




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
    user_id = db.Column(db.Integer, db.ForeignKey('reader.id'))


