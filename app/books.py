from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user, AnonymousUserMixin
from models import Book, Review, User, Genre, Author, Cover, Book2Genre, VisitStat
from app import db
from tools import ImageSaver, drop_by_name, whiteclear, log, to_type
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('book', __name__, url_prefix='/book')


def get_first(query):
    return db.session.execute(query).scalars().first()


def get_all(query):
    return db.session.execute(query).scalars()


def add_to_viewed(book_id):
    current_id = session["current_id"]
    if len(session[f"{current_id}"]) < 5:
        session[f"{current_id}"].append(book_id)
        if not session.modified:
            session.modified = True
    else:
        if book_id not in session[f"{current_id}"]:
            session[f"{current_id}"].pop(0)
            session[f"{current_id}"].append(book_id)
        else:
            session[f"{current_id}"].remove(book_id)
            session[f"{current_id}"].append(book_id)
        if not session.modified:
            session.modified = True


def form_to_dict(fields):
    data_set = {}
    for field in fields:
        data_set[field] = request.form.get(field)
    return data_set


def register_visit(book_obj, user_id):
    visit_stat = get_first(
        db.session.query(VisitStat).filter(VisitStat.book_id == book_obj.id, VisitStat.user_id == user_id))
    if visit_stat is None:
        visit_obj = VisitStat(**{'book_id': book_obj.id, 'user_id': user_id})
        book_obj.add_visit()
        try:
            db.session.add(visit_obj)
            db.session.add(book_obj)
            db.session.commit()
        except SQLAlchemyError as er:
            db.session.rollback()
            print(f'\n\n{er}\n\n')
            flash(f'Visit update error', 'warning')
    else:
        if not visit_stat.is_visit_limit_reached():
            visit_stat.add_visit()
            book_obj.add_visit()
            try:
                db.session.add(visit_stat)
                db.session.add(book_obj)
                db.session.commit()
            except SQLAlchemyError as er:
                db.session.rollback()
                print(f'\n\n{er}\n\n')
                flash(f'Visit update error', 'warning')
    log(visit_stat)


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
    log(request.form)
    data_set = form_to_dict(['name', 'author_id', 'year', 'publishing_house', 'genre_id', 'size', 'description'])
    data_set = whiteclear(data_set)
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
        drop_by_name(book.cover.storage_filename)
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
    if not current_user.can('edit'):
        flash('Недостаточно прав', 'warning')
        return redirect(url_for('index'))
    data_set = form_to_dict(
        ['id', 'cover_id', 'name', 'author_id', 'year', 'publishing_house', 'size', 'description'])
    book = get_first(db.session.query(Book).filter_by(id=data_set['id']))
    new_genres = to_type(request.form.getlist('genre_id'), 'int')
    new_binds = [Book2Genre(**{'book_id': book.id, 'genre_id': genre_id}) for genre_id in new_genres]
    try:
        Book2Genre.query.filter_by(book_id=book.id).delete()
        db.session.commit()
        for bind in new_binds:
            db.session.add(bind)
        db.session.commit()
    except SQLAlchemyError as er:
        db.session.rollback()
        print(f'\n{er}\n')
        flash(f'File upload error!')
        return redirect(url_for('index'))
    data_set = whiteclear(data_set)
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
        data_set = whiteclear(data_set)
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
            print(f'\n\n{er}\n\n')
            flash(f'File upload error!', 'warning')
        return redirect(url_for('book.book_show', book_id=book_id))
    add_to_viewed(book_id)
    if not current_user.is_anonymous:
        user = get_first(db.session.query(User).filter_by(id=current_user.id))
        register_visit(book_obj, user.id)
        current_user_review = get_first(db.session.query(Review).filter_by(user_id=current_user.id, book_id=book_id))
    else:
        user = None
        current_user_review = None
    return render_template('book/show.html', book=book_obj, user=user,
                           user_review=current_user_review, reviews=reviews, users=users)
