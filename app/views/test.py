from flask import Blueprint, render_template

bp = Blueprint('test', __name__, url_prefix='/test')


@bp.route('/', methods=('GET',))
def main():
    return render_template('test/main_test.html')
