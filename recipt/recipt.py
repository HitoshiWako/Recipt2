from flask import Blueprint, render_template
from .model import Store, Recipt, Item

bp = Blueprint('recipt',__name__)

@bp.route('/upload',methods=('GET','POST'))
def upload():
    return render_template('recipt/upload.html')