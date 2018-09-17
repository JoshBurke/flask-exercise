
# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected
def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["result"]["content"] == "hello world!"


def test_mirror(client):
    res = client.get("/mirror/Tim")
    assert res.status_code == 200
    assert res.json["result"]["name"] == "Tim"


def test_get_users(client):
    res = client.get("/users")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 4
    assert res_users[0]["name"] == "Aria"


def tests_get_users_with_team(client):
    res = client.get("/users?team=LWB")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 2
    assert res_users[1]["name"] == "Tim"


def test_get_user_id(client):
    res = client.get("/users/1")
    assert res.status_code == 200

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 19

def test_create_user(client):
    res = client.post("/users", data={"name": "test", "age": 69, "team": "gold"})
    assert res.status_code == 201

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "test"
    assert res_user["age"] == 69
    assert res_user["team"] == "gold"

def test_create_bad_user(client):
    res = client.post("/users", data={"name": "aha"})
    assert res.status_code == 422

def test_update_user(client):
    res = client.put("/users/2", data={"name": "test", "age": 12})
    assert res.status_code == 201

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "test"
    assert res_user["age"] == '12'
    assert res_user["team"] == "LWB"

def test_update_bad_user(client):
    res = client.put("/users/100", data={"name": "foo", "age": 12})
    assert res.status_code == 404

def test_delete_user(client):
    res = client.delete("/users/3")
    assert res.status_code == 201

def test_delete_bad_user(client):
    res = client.delete("/users/300")
    assert res.status_code == 404
