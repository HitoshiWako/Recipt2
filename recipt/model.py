from recipt import db
import sqlalchemy as sa

class Store(db.Model):
    __tablename__ = 'stores'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255))
    address = sa.Column(sa.String(255))
    tel = sa.Column(sa.String(255))

class Recipt(db.Model):
    __tablename__ = 'recipts'
    id = sa.Column(sa.Integer, primary_key=True)
    filename = sa.Column(sa.String(255))
    date = sa.Column(sa.Date)
    store_id = sa.Column(sa.Integer, sa.ForeignKey('stores.id'))

class Item(db.Model):
    __tablename__ = 'items'
    id = sa.Column(sa.Integer, primary_key=True)
    recipt_id = sa.Column(sa.Integer, sa.ForeignKey('recipts.id'))
    name = sa.Column(sa.String(255))
    price = sa.Column(sa.Integer)
    discount = sa.Column(sa.Integer)