from extensions import db

class Customer(db.Model):
    __tablename__ = "Customers"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    sites = db.relationship('Site', backref='customer', lazy=True)


class Site(db.Model):
    __tablename__ = "Sites"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))
    fields = db.relationship('Field', backref='site', lazy=True)


class Field(db.Model):
    __tablename__ = "Fields"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('Sites.id'), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)