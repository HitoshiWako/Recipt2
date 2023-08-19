import os
from flask import Blueprint,current_app,flash,render_template,redirect, request,url_for
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
            file.save(os.path.join(current_app.instance_path,current_app.config['UPLOAD_FOLDER'], filename))
            recipt.filename = filename
            db.session.commit()
            return redirect(url_for('recipt.register',id = recipt.id))
    return render_template('recipt/upload.html')

@bp.route('/recipt/<int:id>',methods=('GET','POST'))
def register(id):
    recipt = db.get_or_404(Recipt, id)
    if request.method == 'POST':
        names = request.form.getlist('item-name')
        prices = request.form.getlist('item-price') 
        discounts = request.form.getlist('item-discount') 
        items = [Item(recipt_id=recipt.id, name=name, price=price, discount=discount) for name, price,discount in zip(names,prices,discounts) if not name.isspace()] 
        db.session.add_all(items)
        db.session.commit()        
    return render_template('recipt/register.html', filename=recipt.filename)
