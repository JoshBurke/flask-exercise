from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


# TODO: Implement the rest of the API here!

@app.route("/users", methods=['GET','POST'])
def users():
    if request.method == 'GET':
        team = request.args.get('team')
        data = db.get("users")
        if team != None:
            new_data = []
            for i in range(len(data)):
                if data[i]["team"] == team:
                    new_data.append(data[i])
            data = new_data
        dic = {"users": data}
        return create_response(dic)
    elif request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        team = request.form.get('team')
        if name == None or age == None or team == None:
            return create_response(status=422, message="One or more parameters is missing.")
        else:
            payload = {"name": name, "age": age, "team": team}
            db.create("users",payload)
            return create_response(status=201, data=payload)
    else:
        return create_response(status=400, message="Malformed request.")

@app.route("/users/<id>", methods=["GET"])
def user_id(id):
    data = db.getById("users", int(id))
    if data == None:
        return create_response(status=404, message="User not found.")
    else:
        return create_response(data)

@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    updated = db.updateById("users",int(id),request.form)
    if updated == None:
        return create_response(status=404, message="User not found.")
    else:
        return create_response(status=201, data=updated, message="User updated.")

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    if db.getById("users", int(id)) == None:
        return create_response(status=404, message="User not found.")

    db.deleteById("users", int(id))
    return create_response(status=201, message="User deleted.")

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
