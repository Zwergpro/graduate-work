from flask import Blueprint, render_template

bp = Blueprint('train', __name__, url_prefix='/train')


@bp.route('/', methods=('GET',))
def main():
    return render_template('train/main_train.html')
