import pandas as pd
import random 
import pytest
import requests
import os

ENDPOINT = "https://petstore.swagger.io/v2"

current_dir = os.path.dirname(__file__)
DATA_DIR = os.path.join(current_dir, "test_cases")

NewPetPos = os.path.join(DATA_DIR, "NewPetPos.xlsx") #https://pairwise.teremokgames.com/5jw54/
NewPetNeg = os.path.join(DATA_DIR, "NewPetNeg.xlsx") #https://pairwise.teremokgames.com/5jw7w/

RANDOM_ID = random.randint(1000, 9999)


def get_pet_data_from_excel_pos():
    df = pd.read_excel(NewPetPos, usecols=[
        "id", "name", "category_id", "category_name", "tags_id", "tags_name", "status"
    ])
    return [tuple(row) for row in df.values]
 

def get_pet_data_from_excel_neg():
    df = pd.read_excel(NewPetNeg, usecols=[
        "id", "name", "category_id", "category_name", "tags_id", "tags_name", "status"
    ])
    return [tuple(row) for row in df.values]

@pytest.fixture
def update_user_data():
    return {
  "id": RANDOM_ID,
  "username": "beccapana",
  "firstName": "Me", #btw I really changed my name
  "lastName": "Test",
  "email": "test_email@test.com", 
  "password": "testpass",
  "phone": "+711234567890", 
  "userStatus": 0
}

@pytest.fixture
def user_login():
    return {
  "username": "beccapana",
  "password": "animetestt"
    }

@pytest.fixture
def create_user():
    return {
  "id": RANDOM_ID,
  "username": "beccapana",
  "firstName": "test", 
  "lastName": "test",
  "email": "string",
  "password": "animetestt",
  "phone": "string",
  "userStatus": 0
    }

def new_pet(pet_id, name, category_id, category_name, tag_id, tag_name, status):
    return {
        "id": pet_id,
        "category": {"id": category_id, "name": category_name},
        "name": name,
        "photoUrls": ["https://example.com/dog.jpg"],
        "tags": [{"id": tag_id, "name": tag_name}],
        "status": status
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