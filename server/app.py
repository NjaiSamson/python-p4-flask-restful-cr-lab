#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plants_dict = [plant.to_dict() for plant in plants]
        
        response = make_response(plants_dict, 200)
        return response

    def post(self):
        data = request.get_json()        
        new_plant = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price'),            
        )
        
        db.session.add(new_plant)
        db.session.commit()
        
        response_dict = new_plant.to_dict()
        
        return jsonify(response_dict), 201  # Returning the created plant with 201 status
    
# Adding the resource to the API
api.add_resource(Plants, '/plants')
class PlantByID(Resource):
    def get(self, id):
        plant_by_id = Plant.query.filter(Plant.id == id).first()
        plant_by_id_dict = plant_by_id.to_dict()
        
        response = make_response(plant_by_id_dict, 200,)
        return response
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
