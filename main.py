from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class PersonModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Person(name = {name}, age = {age}, phone = {phone})"


person_put_args = reqparse.RequestParser()
person_put_args.add_argument("name", type=str, help="Please enter your name", required=True)
person_put_args.add_argument("age", type=int, help="Please enter your age", required=True)
person_put_args.add_argument("phone", type=int, help="Please enter your phone number", required=True)

person_update_args = reqparse.RequestParser()
person_update_args.add_argument("name", type=str, help="Please enter your name")
person_update_args.add_argument("age", type=int, help="Please enter your age")
person_update_args.add_argument("phone", type=int, help="Please enter your phone number")

# resource field is a way to define how an object should be serialized
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'phone': fields.Integer,
    }



class Person(Resource):
    @marshal_with(resource_fields)
    def get(self, person_id):
       result = PersonModel.query.filter_by(id=person_id).first()
       if not result:
           abort(404, message="Could not find person with that id...")
       return result
    
    @marshal_with(resource_fields)
    def put(self, person_id):
        args = person_put_args.parse_args()
        result = PersonModel.query.filter_by(id=person_id).first()
        if result:
            abort(409, message="Person id already exist...") # 409 status code means already exist
        person = PersonModel(id=person_id, name=args['name'], age=args['age'], phone=args['phone'])
        db.session.add(person)
        db.session.commit()
        return person, 201
    
    @marshal_with(resource_fields)
    def patch(self, person_id):
        args = person_update_args.parse_args()
        result = PersonModel.query.filter_by(id=person_id).first()
        if not result:
            abort(404, message="Person doesn't exist... cannot update")
        
        if args["name"]:
            result.name = args['name']
        if args["age"]:
            result.age = args['age']
        if args["phone"]:
            result.phone = args['phone']
        
        db.session.commit

        return result

    def delete(self, person_id):
        abort_if_id_doesnt_exist(person_id)
        del persons[person_id]
        return '', 204 #deleted successfully 

api.add_resource(Person, "/person/<int:person_id>")

# class HelloWorld(Resource):
#     def get(self, name):
#         return names[name]
    
# api.add_resource(HelloWorld, "/helloworld/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)