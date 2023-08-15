import os
from flask import Blueprint,current_app,flash,render_template,redirect, request
from .model import Store, Recipt, Item
from . import db

ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('recipt',__name__)

@bp.route('/upload',methods=('GET','POST'))
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルが選択されていません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            recipt = Recipt()
            db.session.add(recipt)
            db.session.flush()
            filename = 'img{:08}.png'.format(recipt.id)
            file.save(os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], filename))
            recipt.filename = filename
            db.session.commit()
    return render_template('recipt/upload.html')