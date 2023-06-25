import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import current_app
from app import db
from users_policy import UsersPolicy

# TODO: 1) Роли, r/w/d rights, добавление книг, пилим с лаб4
# TODO: 2) Работа с изображениями, лаб6
# TODO: *3) История посещений по книге, сортировка по количеству просмотров, лаб5


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    description = db.Column(db.Text(), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    publishing_house = db.Column(db.String(45), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    cover_id = db.Column(db.Integer, db.ForeignKey('cover.id'), nullable=False)
    rating_sum = db.Column(db.Integer, default=0)
    rating_num = db.Column(db.Integer, default=0)

    author = db.relationship('Author')
    genre = db.relationship('Genre')
    cover = db.relationship('Cover')

    @property
    def rating(self):
        if self.rating_num <= 0:
            return 0
        return self.rating_sum / self.rating_num

    def __repr__(self):
        return f'Book {self.name} under {self.author.name}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())

    def __repr__(self):
        return f'<Role {self.name}>'


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    given_rating = db.Column(db.Integer, default=1)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=sa.sql.func.now(), nullable=False)

    book = db.relationship('Book')
    user = db.relationship('User')

    def __repr__(self):
        return f'<Review id={self.id}, user_id={self.user_id}, book_id={self.book_id}>'


class Cover(db.Model):
    __tablename__ = 'cover'
    id = db.Column(db.String(100), primary_key=True)
    file_name = db.Column(db.String(45), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    md5_hash = db.Column(db.String(100), nullable=False)

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name or ""}'

    def __repr__(self):
        return f'<User {self.login}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_admin(self):
        return self.role_id == current_app.config["ADMIN_ROLE_ID"]

    def is_moderator(self):
        return self.role_id == current_app.config["MODERATOR_ROLE_ID"]

    @staticmethod
    def can(action, record=None):
        users_policy = UsersPolicy(record)
        method = getattr(users_policy, action, None)
        if method:
            return method()
        return False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def render_fio(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)
