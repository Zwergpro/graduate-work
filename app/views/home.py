from flask import Blueprint, render_template

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=('GET',))
def main():
    return render_template('home/main_home.html')
