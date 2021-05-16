import os
from contextlib import suppress

from flask import Blueprint, render_template, redirect, url_for, request
from sqlalchemy import desc

from models import db
from models.test import Test, TestStatus

bp = Blueprint('test', __name__, url_prefix='/test')


@bp.route('/', methods=('GET',))
def main():
    active_test = (
        Test.query
        .filter(Test.status == TestStatus.start)
        .order_by(desc(Test.dt_start))
        .first()
    )

    if active_test is not None:
        tests = Test.query.filter(Test.id != active_test.id).order_by(desc(Test.dt_start)).all()
    else:
        tests = Test.query.order_by(desc(Test.dt_start)).all()

    return render_template('test/main_test.html', tests=tests)


@bp.route('/delete/', methods=('POST',))
def delete():
    test_model = Test.query.get_or_404(ident=request.form.get('test_id', default=0))
    with suppress(FileNotFoundError, PermissionError):
        os.remove(test_model.path, dir_fd=True)

    local_session = db.session.object_session(test_model)
    local_session.delete(test_model)
    local_session.commit()
    return redirect(url_for('test.main'))
