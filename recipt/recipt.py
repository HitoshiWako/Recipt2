import datetime
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

    items = db.session.execute(db.select(Item).filter_by(recipt_id=recipt.id)).scalars()
    if recipt.date is None:
        recipt.date = datetime.date.today()

    stores = db.session.execute(db.select(Store)).scalars()
    if request.method == 'POST':
        names = request.form.getlist('item-name')
        prices = request.form.getlist('item-price') 
        discounts = request.form.getlist('item-discount') 
        items = [Item(recipt_id=recipt.id, name=name, price=price, discount=discount) for name, price,discount in zip(names,prices,discounts) if name and not name.isspace()] 
        
        recipt.date = datetime.date.fromisoformat(request.form['purchase-date'])
        recipt.store_id = request.form['store-select'] if request.form['store-select'] else None
            
        db.session.execute(db.delete(Item).where(Item.recipt_id==recipt.id))
        db.session.add_all(items)
        db.session.commit()
        if 'register' in request.form:
            return redirect(url_for('recipt.upload'))
        elif 'new-store' in request.form:
            return redirect(url_for('store.register',id=recipt.id))
    return render_template('recipt/register.html', recipt=recipt,items=items,stores=stores)
