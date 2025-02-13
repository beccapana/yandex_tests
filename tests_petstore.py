import requests
import pytest
import pandas as pd
from config import *
import re

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
@pytest.mark.parametrize("pet_id, pet_name, category_id, category_name, tag_id, tag_name, status", get_pet_data_from_excel_pos())
def test_post_pet_from_excel_pos(pet_id, pet_name, category_id, category_name, tag_id, tag_name, status):
    pet_data = new_pet(pet_id, pet_name, category_id, category_name, tag_id, tag_name, status)  
    print(pet_data)
    response = requests.post(f"{ENDPOINT}/pet", json=pet_data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_json = response.json()
    assert response_json["name"] == pet_name, f"Expected {pet_name}, got {response_json['name']}"
    assert response_json["id"] == pet_id, f"Expected {pet_id}, got {response_json['id']}"
    assert response_json["category"]["id"] == category_id, f"Expected {category_id}, got {response_json['category']['id']}"
    assert response_json["category"]["name"] == category_name, f"Expected {category_name}, got {response_json['category']['name']}"
    assert response_json["tags"][0]["id"] == tag_id, f"Expected {tag_id}, got {response_json['tags'][0]['id']}"
    assert response_json["tags"][0]["name"] == tag_name, f"Expected {tag_name}, got {response_json['tags'][0]['name']}"
    assert response_json["status"] == status, f"Expected {status}, got {response_json['status']}"


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

@pytest.mark.parametrize("pet_id, pet_name, category_id, category_name, tag_id, tag_name, status", get_pet_data_from_excel_pos())
def test_post_pet_from_excel_neg(pet_id, pet_name, category_id, category_name, tag_id, tag_name, status):
    pet_data = new_pet(pet_id, pet_name, category_id, category_name, tag_id, tag_name, status)  
    print(pet_data)
    response = requests.post(f"{ENDPOINT}/pet", json=pet_data)
    assert response.status_code != 200, f"Why 200: ID {category_id} != {category_name} and/or ID {tag_id} != {tag_name}"

"""get pet/{id}"""
#get with free ID
def test_get_pet_free():
    response = requests.get(f"{ENDPOINT}/pet/{find_free_pet_id()}")
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"

"""delete pet/{id}"""
def test_delete_busy_pet_neg():
    response = requests.delete(f"{ENDPOINT}/pet/{find_free_pet_id()}")
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
