from flask import Blueprint, render_template  # , request
from flask_login import login_required
from sqlalchemy import desc
from app import db
from auth import check_rights
from models import Book  # VisitStat

bp = Blueprint('visits', __name__, url_prefix='/visits')


@bp.route('/logs')
@login_required
@check_rights("show_stat")
def logs():
    books = db.session.execute(
        db.session.query(Book).order_by(desc(Book.visit_number))).scalars()
    # visit_stat = db.session.execute(db.select(VisitStat)).scalars()
    return render_template('visits/logs.html', books=books)
