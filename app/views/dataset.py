from flask import Blueprint, render_template

bp = Blueprint('dataset', __name__, url_prefix='/dataset')


@bp.route('/', methods=('GET',))
def main():
    return render_template('dataset/main_dataset.html')
