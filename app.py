from flask import Flask, jsonify, request
from models.storage import Storage

app = Flask(__name__)

storage = Storage()

@app.route("/api", methods=["POST"])
def create_user():
    """api url to create user with post request"""
    data = request.get_json()
    if not data:
        return {
            "status": "error",
            "message": "Not a JSON"
        }, 400
    if not data.get("name"):
        return {
            "status": "error",
            "message": "no name attribute"
        }, 400
    result = storage.create(data.get("name"))
    if result:
        return {
                "status": "success",
                "message": "created successfully"
            }, 201
    return jsonify({
            "status": "error",
            "message": "Database Error, Please try again"
        }), 400

@app.route("/api/<id>", methods = ["GET", "PUT", "DELETE"])
def get_user(id):
    """get a user with id"""
    print(id)
    if request.method == "GET":
        result = storage.get(id)
        if result != {}:
            return result, 200
        return {
            "status": "error",
            "message": "please put in a valid 'id'"
        }, 400
    if request.method == "PUT":
        result = storage.update(id)
        if result:
            return {
                "status": "success",
                "message": "updated successfully"
            }, 200
        return {
            "status": "error",
            "message": "error updating record"
        }, 400
    
    if request.method == "DELETE":
        result = storage.delete(id)
        if result:
            return {}, 200
        return {
            "status": "error",
            "message": "failed to delete record"
        }, 400


if __name__ == "__main__":
    app.run()