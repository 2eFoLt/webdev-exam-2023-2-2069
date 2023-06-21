from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Book, Review, User, Genre, Author
from app import db
# from tools import ImageSaver
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


#
# @bp.route('/new')
# def new():
#     categories = db.session.execute(db.select(Category)).scalars()
#     users = db.session.execute(db.select(User)).scalars()
#     return render_template('courses/new.html', categories=categories, users=users)
#
#
# @bp.route('/create', methods=['POST'])
# def create():
#     data_set = form_to_dict()
#     file_obj = request.files['background_img']
#     image = None
#     if file_obj.filename != '':
#         image = ImageSaver(file_obj).save()
#     course = Course(**data_set)
#     if image:
#         course.background_image_id = image.id
#     try:
#         db.session.add(course)
#         db.session.commit()
#     except SQLAlchemyError as er:
#         db.session.rollback()
#         flash(f'File upload error!')
#     return redirect(url_for('courses.index'))
#
#
@bp.route('/<int:book_id>', methods=['GET', 'POST'])
def book_show(book_id):
    book_obj = get_first(db.session.query(Book).filter_by(id=book_id))
    genre = get_first(db.session.query(Genre).filter_by(id=book_obj.id))
    author = get_first(db.session.query(Author).filter_by(id=book_obj.author_id))
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
            flash(er.__repr__())
        return redirect(url_for('book.book_show', book_id=book_id))
    if not current_user.is_anonymous:
        user = get_first(db.session.query(User).filter_by(id=current_user.id))
        current_user_review = get_first(db.session.query(Review).filter_by(user_id=current_user.id, book_id=book_id))
    else:
        user = None
        current_user_review = None
    return render_template('book/show.html', book=book_obj, genre=genre, user=user, author=author,
                           user_review=current_user_review, reviews=reviews, users=users)
