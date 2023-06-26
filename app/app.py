from flask import Flask, render_template, send_from_directory, redirect, url_for, request
from sqlalchemy import MetaData, desc
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from math import ceil


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

from models import Book, Cover, Genre, Book2Genre


@app.route('/')
def index():
    popular_books = db.session.execute(db.session.query(Book).order_by(desc(Book.visit_number)).limit(5)).scalars()
    page = request.args.get('page', 1, type=int)
    books = db.session.execute(
                db.session.query(Book).order_by(desc(Book.year)).offset(10 * (page - 1)).limit(10)).scalars()
    db_counter = db.session.query(Book).count()
    page_count = ceil(db_counter / 10)
    b2g = db.session.execute(db.select(Book2Genre)).scalars()
    genres = db.session.execute(db.select(Genre)).scalars()
    return render_template(
        'index.html',
        page=page,
        page_count=page_count,
        books=books,
        popular_books=popular_books,
        genres=genres,
        b2g=b2g
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
