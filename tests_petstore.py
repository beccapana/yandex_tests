import requests
import pytest
import pandas as pd
import config
import re
import random

ENDPOINT = config.ENDPOINT
NewPetPos = config.NEW_PET_POS_FILE
NewPetNeg = config.NEW_PET_NEG_FILE

random_id = random.randint(1000, 9999)


def get_pet_data_from_excel_pos():
    df = pd.read_excel(NewPetPos, usecols=["id", "name"])  
    return df.values.tolist() 

def get_pet_data_from_excel_neg():
    df = pd.read_excel(NewPetNeg, usecols=["id", "name"]) 
    return df.values.tolist() 

@pytest.fixture
def update_user_data():
    return {
  "id": random_id,
  "username": "beccapana",
  "firstName": "Yan",
  "lastName": "Akulov",
  "email": "ian.sharkov@gmail.com", #don't care
  "password": "qwerty666",
  "phone": "+7977101", #private data lol
  "userStatus": 0
}

@pytest.fixture
def user_login():
    return {
  "username": "beccapana",
  "password": "anime"
    }

@pytest.fixture
def create_user():
    return {
  "id": random_id,
  "username": "beccapana", #hardcode
  "firstName": "Agei", #btw I rly changed my name 
  "lastName": "Kulesh",
  "email": "string",
  "password": "anime",
  "phone": "string",
  "userStatus": 0
    }

def new_pet(pet_id, name):
    return {
        "id": pet_id,
        "category": {"id": 1, "name": "Dogs"},
        "name": name,
        "photoUrls": ["https://example.com/dog.jpg"],
        "tags": [{"id": 1, "name": "cute"}],
        "status": "available"
    }

@pytest.fixture
def new_pet_free():
    return {
        "id": find_free_pet_id(),
        "category": {"id": 1, "name": "Dogs"},
        "name": "Buddy",
        "photoUrls": ["https://example.com/dog.jpg"],
        "tags": [{"id": 1, "name": "cute"}],
        "status": "available"
    }

@pytest.fixture
def new_pet_busy():
    return {
        "id": find_busy_pet_id(),
        "category": {"id": 1, "name": "Dogs"},
        "name": "Buddy",
        "photoUrls": ["https://example.com/dog.jpg"],
        "tags": [{"id": 1, "name": "cute"}],
        "status": "available"
    }


#search for free pet
def find_free_pet_id():
    free_pet_id = 1
    while True:
        response = requests.get(f"{ENDPOINT}/pet/{free_pet_id}")
        if response.status_code == 404:
            return free_pet_id
        free_pet_id += 1

#search for busy pet
def find_busy_pet_id():
    busy_pet_id = 1
    while True:
        response = requests.get(f"{ENDPOINT}/pet/{busy_pet_id}")
        if response.status_code == 200:
            return busy_pet_id
        busy_pet_id += 1

"""positive tests"""

"""post"""
#post pet with free ID
def test_post_pet_free(new_pet_free):
    response = requests.post(f"{ENDPOINT}/pet", json=new_pet_free)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_json = response.json()
    assert response_json["id"] == new_pet_free["id"], "Pet ID mismatch"
    assert response_json["name"] == new_pet_free ["name"], "Pet name mismatch"

#testing pets from excel table | Positive
@pytest.mark.parametrize("pet_id, pet_name", get_pet_data_from_excel_pos())
def test_post_pet_from_excel_pos(pet_id, pet_name):
    pet_data = new_pet(pet_id, pet_name)  
    response = requests.post(f"{ENDPOINT}/pet", json=pet_data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_json = response.json()
    assert response_json["name"] == pet_name, f"Expected {pet_name}, got {response_json['name']}"
    assert response_json["id"] == pet_id, f"Expected {pet_id}, got {response_json['id']}"

def test_create_user(create_user):
    response = requests.post(f"{ENDPOINT}/user/", json=create_user)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

"""put"""
def test_update_user_data(update_user_data, user_login):
    requests.get(f"{ENDPOINT}/user/login", params=user_login) 

    response = requests.put(f"{ENDPOINT}/user/beccapana", json=update_user_data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    response = requests.get(f"{ENDPOINT}/user/beccapana")
    assert response.status_code == 200, f"Unexpected status code on GET: {response.status_code}"
    response = response.json()
    for key, expected_value in update_user_data.items(): #we also can check so
        assert response.get(key) == expected_value, f"Mismatch on {key}: expected {expected_value}, got {response.get(key)}"


"""delete"""
#delete with busy ID
def test_delete_busy_pet_pos():
    response = requests.delete(f"{ENDPOINT}/pet/{find_busy_pet_id()}")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

def test_delete_user():
        response = requests.delete(f"{ENDPOINT}/user/beccapana")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"



"""negative tests"""

"""post"""
#post pet with busy ID
def test_post_pet_busy(new_pet_busy):
    response = requests.post(f"{ENDPOINT}/pet", json=new_pet_busy)
    assert response.status_code != 200, f"Why 200. ID is busy." #Must be Failed

#testing pets from excel table | Negative
@pytest.mark.parametrize("pet_id, pet_name", get_pet_data_from_excel_neg())
def test_post_pet_from_excel_neg(pet_id, pet_name):
    pet_data = new_pet(pet_id, pet_name)  
    response = requests.post(f"{ENDPOINT}/pet", json=pet_data)

    if re.search(r"[^a-zA-Z]", pet_name):  
        assert response.status_code != 200, f"{response.status_code}. Why I can use spec symbools and numbers: {pet_name}"

"""get pet/{id}"""
#get with free ID
def test_get_pet_free():
    response = requests.get(f"{ENDPOINT}/pet/{find_free_pet_id()}")
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"

"""delete pet/{id}"""
def test_delete_busy_pet_neg():
    response = requests.delete(f"{ENDPOINT}/pet/{find_free_pet_id()}")
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
