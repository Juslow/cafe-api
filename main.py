from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=['GET'])
def search_by_location():
    location = request.args.get('loc')
    cafes = Cafe.query.filter_by(location=location).all()
    if len(cafes) != 0:
        return jsonify(cafes=[{"id": cafe.id,
                               "name": cafe.name,
                               "map_url": cafe.map_url,
                               "img_url": cafe.img_url,
                               "location": cafe.location,
                               "seats": cafe.seats,
                               "has_toilet": cafe.has_toilet,
                               "has_wifi": cafe.has_wifi,
                               "has_sockets": cafe.has_sockets,
                               "can_take_calls": cafe.can_take_calls,
                               "coffee_price": cafe.coffee_price, } for cafe in cafes])
    else:
        return jsonify(error={"not_found": "Sorry, we don't have a cafe in that location."})


# HTTP GET - Read Record
@app.route("/all", methods=['GET'])
def get_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    return jsonify(cafes=[{"id": cafe.id,
                           "name": cafe.name,
                           "map_url": cafe.map_url,
                           "img_url": cafe.img_url,
                           "location": cafe.location,
                           "seats": cafe.seats,
                           "has_toilet": cafe.has_toilet,
                           "has_wifi": cafe.has_wifi,
                           "has_sockets": cafe.has_sockets,
                           "can_take_calls": cafe.can_take_calls,
                           "coffee_price": cafe.coffee_price, } for cafe in all_cafes])


@app.route("/random", methods=['GET'])
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
    })


# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add_new_cafe():
    # data for that object is given by a user in a search bar
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('loc'),
        seats=request.form.get('seats'),
        has_toilet=bool(request.form.get('toilet')),
        has_wifi=bool(request.form.get('wifi')),
        has_sockets=bool(request.form.get('sockets')),
        can_take_calls=bool(request.form.get('calls')),
        coffee_price=request.form.get('price'),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_price(cafe_id: int):
    cafe = Cafe.query.get(cafe_id)
    cafe.coffee_price = request.args.get('new_price')
    db.session.commit()
    return jsonify(response={"success": f"Successfully changed black coffee price in {cafe.name}."})


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete(cafe_id: int):
    cafe_to_delete = Cafe.query.get(cafe_id)
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"success": f"Successfully deleted {cafe_to_delete.name}."})
    else:
        return jsonify(error={"Sorry, cafe with that id was not found in database."})


if __name__ == '__main__':
    app.run(debug=True)
