from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, AnonymousUserMixin
from models import Book, Review, User, Genre, Author, Cover
from app import db
from tools import ImageSaver, drop_by_name
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('book', __name__, url_prefix='/book')


def get_first(query):
    return db.session.execute(query).scalars().first()


def get_all(query):
    return db.session.execute(query).scalars()


def form_to_dict(fields):
    data_set = {}
    for field in fields:
        data_set[field] = request.form.get(field)
    return data_set


@bp.route('/new')
@login_required
def book_new():
    if current_user.can('create'):
        genres = db.session.execute(db.select(Genre)).scalars()
        authors = db.session.execute(db.select(Author)).scalars()
        return render_template('book/new.html', book=None, genres=genres, authors=authors)
    else:
        flash('Недостаточно прав', 'warning')
        return redirect(url_for('index'))


@bp.route('/create', methods=['POST'])
@login_required
def book_create():
    if not current_user.can('create'):
        flash('Недостаточно прав', 'warning')
        return redirect(url_for('index'))
    print('\n', request.form, '\n')
    data_set = form_to_dict(['name', 'author_id', 'year', 'publishing_house', 'genre_id', 'size', 'description'])
    file_obj = request.files['cover_id']
    image = None
    if file_obj.filename != '':
        image = ImageSaver(file_obj).save()
    book = Book(**data_set)
    if image:
        book.cover_id = image.id
    try:
        db.session.add(image)
        db.session.commit()
    except SQLAlchemyError as er:
        db.session.rollback()
        print(f'\n{er}\n')
        flash(f'File upload error!')
        return redirect(url_for('index'))
    try:
        db.session.add(book)
        db.session.commit()
    except SQLAlchemyError as er:
        db.session.rollback()
        print(f'\n{er}\n')
        flash(f'File upload error!')
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@bp.route('/edit/<int:book_id>')
@login_required
def book_edit(book_id):
    if not current_user.can('edit'):
        flash('Недостаточно прав', 'warning')
        return redirect(url_for('index'))
    book_obj = get_first(db.session.query(Book).filter_by(id=book_id))
    genres = db.session.execute(db.select(Genre)).scalars()
    authors = db.session.execute(db.select(Author)).scalars()
    return render_template('book/edit.html', book=book_obj, genres=genres, authors=authors)


@bp.route('/update', methods=['POST'])
@login_required
def book_update():
    data_set = form_to_dict(
        ['id', 'cover_id', 'name', 'author_id', 'year', 'publishing_house', 'genre_id', 'size', 'description'])
    book = Book(**data_set)
    try:
        db.session.query(Book).filter_by(id=data_set['id']).update(data_set)
        db.session.commit()
    except SQLAlchemyError as er:
        db.session.rollback()
        print(f'\n{er}\n')
        flash(f'File upload error!')
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@bp.route('/delete/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_delete(book_id):
    if not current_user.can('delete'):
        flash('Недостаточно прав', 'warning')
        return redirect(url_for('index'))
    book_obj = get_first(db.session.query(Book).filter_by(id=book_id))
    cover = get_first(db.session.query(Cover).filter_by(id=book_obj.cover_id))
    if request.method == 'GET':
        return render_template('book/delete.html', book=book_obj)
    else:
        try:
            db.session.delete(book_obj)
            db.session.delete(cover)
            db.session.commit()
            drop_by_name(cover.storage_filename)
            flash('Книга успешно удалена', 'success')
        except SQLAlchemyError as er:
            db.session.rollback()
            print(f'\n\n{er}\n\n')
            flash(f'File upload error!', 'warning')
            return redirect(url_for('index'))
        return redirect(url_for('index'))


@bp.route('/<int:book_id>', methods=['GET', 'POST'])
def book_show(book_id):
    book_obj = get_first(db.session.query(Book).filter_by(id=book_id))
    reviews = get_all(db.session.query(Review).filter_by(book_id=book_id))
    users = db.session.execute(db.select(User)).scalars()
    if request.method == 'POST':
        data_set = form_to_dict(['text', 'given_rating'])
        data_set['book_id'] = book_id
        data_set['user_id'] = current_user.id
        review_obj = Review(**data_set)
        book_obj.rating_num += 1
        book_obj.rating_sum += int(data_set['given_rating'])
        try:
            db.session.add(review_obj)
            db.session.add(book_obj)
            db.session.commit()
        except SQLAlchemyError as er:
            db.session.rollback()
            flash(f'File upload error!', 'warning')
        return redirect(url_for('book.book_show', book_id=book_id))
    if not current_user.is_anonymous:
        user = get_first(db.session.query(User).filter_by(id=current_user.id))
        current_user_review = get_first(db.session.query(Review).filter_by(user_id=current_user.id, book_id=book_id))
    else:
        user = None
        current_user_review = None
    return render_template('book/show.html', book=book_obj, user=user,
                           user_review=current_user_review, reviews=reviews, users=users)
