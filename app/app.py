from flask import Flask, render_template, send_from_directory, redirect, url_for
from sqlalchemy import MetaData, desc
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from flask_login import current_user

# TODO: 2) class UsersPolicy, лаб5

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(app, metadata=MetaData(naming_convention=convention))
migrate = Migrate(app, db)

from auth import bp as auth_bp, init_login_manager

from books import bp as book_bp

app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)

init_login_manager(app)

from models import Book, Cover, Genre


@app.route('/')
def index():
    books = db.session.query(Book).order_by(desc(Book.year))
    genres = db.session.execute(db.select(Genre)).scalars()
    return render_template(
        'index.html',
        books=books,
        genres=genres
    )


@app.route('/<int:genre_id>')
def sortby(genre_id):
    genres = db.session.execute(db.select(Genre)).scalars()
    books = db.session.query(Book).filter_by(genre_id=genre_id)
    return render_template(
        'index.html',
        books=books,
        genres=genres,
        selected=genre_id
    )


@app.route('/gen_hash/<string:password>')
def gen(password):
    print(generate_password_hash(password), f'for {password}')
    return redirect(url_for('index'))


@app.route('/media/<cover_id>')
def image(cover_id):
    img = db.get_or_404(Cover, cover_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img.storage_filename)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))
