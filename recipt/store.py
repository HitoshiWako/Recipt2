import datetime
import os
from flask import Blueprint,current_app,flash,render_template,redirect, request,url_for
from .model import Store, Recipt, Item
from . import db

bp = Blueprint('store',__name__)

@bp.route('/store/<int:id>',methods=('GET','POST'))
def register(id):
    recipt = db.get_or_404(Recipt, id)
    if recipt.store_id is not None:
        store = db.session.execute(db.select(Store).filter_by(id=recipt.store_id)).scalar_one()
    else:
        store = Store()
    if request.method=='POST':
        name = request.form['store-name']
        if name and not name.isspace():
            if store.id is None:
                db.session.add(store)
                db.session.flush()
            store.name = name
            store.address = request.form['store-address']
            store.tel = request.form['store-tel']
            recipt.store_id=store.id
            db.session.commit()
            return redirect(url_for('recipt.register',id=recipt.id))
    return render_template('store.html', recipt=recipt,store=store)
