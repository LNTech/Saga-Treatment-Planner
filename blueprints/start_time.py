# start_time.py
import json
from os.path import exists
from uuid import uuid4
from flask import Blueprint, render_template, request, jsonify
from extensions import basic_auth, db
from models import Customer, Site, Field


start_time = Blueprint('start_time', __name__)

def read_json():
    """ Read json file """
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def write_json(data):
    """ Write json file """
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

@start_time.route("/")
@basic_auth.required
def main():
    """ Main route for displaying location selector """
    customers = db.session.query(Customer).all()

    data = []
    for customer in customers:
        sites = Site.query.filter_by(customer_id=customer.id).all()
        fields = []
        for site in sites:
            fields.extend(Field.query.filter_by(site_id=site.id).all())
        data.append((customer, sites, fields))

    return render_template("treatment-start-time.html", data=data)

@start_time.route("/data")
@basic_auth.required
def get_data():
    """ Gets JSON and returns it via GET request"""
    _json = {}
    if exists("data.json"):
        _json = read_json()

    return jsonify(_json), 200

@start_time.route("/data", methods=["POST"])
@basic_auth.required
def post_data():
    """ Takes POST request and writes data to JSON file"""
    if request.is_json:
        data = request.json
        for line in data:
            customer = Customer.query.filter_by(name=line['customer']).first()
            if customer is None:
                # Skip if customer not found
                continue
            
            site = Site.query.filter_by(name=line['site'], customer_id=customer.id).first()
            if site is None:
                # Skip if site not found
                continue
            
            first_field = Field.query.filter_by(site_id=site.id).first()
            if first_field is None:
                # Skip if fields not found
                continue
            
            line['lat'] = first_field.lat
            line['lng'] = first_field.lng
        write_json(data)
        return jsonify(data), 200
    return jsonify({}), 403

@start_time.route("/add/customer", methods=["POST"])+
@basic_auth.required
def add_customer():
    """ Adds customer to database"""

    if request.is_json:
        data = request.json

        if 'customer' not in data:
            return jsonify({"message": "Missing 'Customer' in data"}), 400
        
        name = data['customer']
        exists = Customer.query.filter_by(name=name).first()

        if exists:
            return jsonify({"message": "Customer already exists"}), 200
        
        uuid = str(uuid4())
        new_customer = Customer(name=name, uuid=uuid)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"message": f"Added customer {name} with uuid {uuid}"}), 201
    
    return jsonify({"message": "Unrecognized request"}), 400

@start_time.route("/add/site", methods=["POST"])
@basic_auth.required
def add_site():
    """ Adds site to database """
    
    if request.is_json:
        data = request.json

        for key in ['site', 'customer']:
            if key not in data:
                return jsonify({"message": f"Missing {key} in data"}), 400
        
        site_name = data['site']
        customer_name = data['customer']

        customer = Customer.query.filter_by(name=customer_name).first()
        if customer is None:
            return jsonify({"message": f"Customer '{customer_name}' not recognized"}), 404
        
        exists = Site.query.filter_by(name=site_name, customer_id=customer.id).first()
        if exists:
            return jsonify({"message": "Site already exists"}), 200

        uuid = str(uuid4())
        new_site = Site(name=site_name, uuid=uuid, customer_id=customer.id)
        db.session.add(new_site)
        db.session.commit()
        return jsonify({"message": f"Added site {site_name} with uuid {uuid}"}), 201
    return jsonify({"message": "Unrecognized request"}), 400

@start_time.route("/add/field", methods=["POST"])
@basic_auth.required
def add_field():
    """ Add field to database """

    if request.is_json:
        data = request.json

        for key in ['customer', 'site', 'field', 'lat', 'lng']:
            if key not in data:
                return jsonify({"message": f"Missing {key} in data"}), 400
            
        lat = data['lat']
        lng = data['lng']
        field_name = data['field']
        site_name = data['site']
        customer_name =  data['customer']

        customer = Customer.query.filter_by(name=customer_name).first()
        if customer is None:
            return jsonify({"message": f"Customer '{customer_name}' not recognized"}), 404
        
        site = Site.query.filter_by(name=site_name, customer_id=customer.id).first()
        if site is None:
            return jsonify({"message": f"Site '{site_name}' not recognized"}), 404
        
        exists = Field.query.filter_by(name=field_name, site_id=site.id).first()
        if exists:
            return jsonify({"message": "Field already exists"}), 200
        
        uuid = str(uuid4())
        new_field = Field(name=field_name, uuid=uuid, lat=lat, lng=lng, site_id=site.id)
        db.session.add(new_field)
        db.session.commit()
        return jsonify({"message": f"Added field {field_name} with uuid {uuid}"}), 201
    return jsonify({"message": "Unrecognized request"}), 400