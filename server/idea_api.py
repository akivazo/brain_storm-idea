from flask import Flask, request, jsonify
from pymongo import MongoClient
from pydantic import BaseModel, Field, ValidationError
from typing import List
from uuid import uuid4
from typing import Type
from flask_cors import CORS

class Idea(BaseModel):
    id: str
    owner_name: str
    subject: str
    details: str
    tags: List[str] = Field(default_factory=list)

server = Flask(__name__)
CORS(server)
collection = None


def set_mongo_client(mongo_client: MongoClient):
    global collection
    collection = mongo_client.get_database("brain_storm").get_collection("ideas")

def validate_json_schema(json: dict, cls: Type):
    # validate that the accepted json is cintaining all the data nedded
    instance = None
    try:
        instance = cls(**json)
    except ValidationError as e:
        return None, e.json()
    return instance.__dict__, ""
    
@server.route("/idea", methods=["POST"])
def create():
    json = request.json
    id = str(uuid4())
    json["id"] = id
    result, message = validate_json_schema(json, Idea)
    if not result:
        return jsonify(message), 400 
    collection.insert_one(result)
    del result["_id"]
    return jsonify({"idea": result}), 201

@server.route("/idea/<id>", methods=["GET"])
def get_idea(id: str):
    result = collection.find_one({"id": id}, {"_id": 0})
    if result is None:
        return jsonify(f"Idea with id '{id}' was not found"), 404
    return jsonify({"idea": result})

@server.route("/ideas", methods=["GET"])
def get_all():
    tags = request.args.getlist("tag")
    if not tags:
        result = collection.find({}, {"_id": 0})
    else:
        result = collection.find({"tags": {"$in": tags}}, {"_id": 0})
    return jsonify({"ideas": list(result)})


@server.route("/idea/<id>", methods=["DELETE"])
def delete_idea(id: str):
    collection.delete_one({"id": id})
    return "", 204

if __name__ == "__main__":
    import dotenv, os
    dotenv.load_dotenv()
    mongo_client = MongoClient(os.environ["IDEA_MONGODB_URI"])
    server.run(debug=True)
    mongo_client.close()

    




