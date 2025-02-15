import requests
import pytest
from config import *

"""positive tests"""

"""post"""
#post pet with free ID
def test_post_pet_free(new_pet_free):
    response = requests.post(f"{ENDPOINT}/pet", json=new_pet_free)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_json = response.json()
    for key, expected_value in new_pet_free.items(): 
        assert str(response_json.get(key)) == str(expected_value), f"Mismatch on {key}: expected {expected_value}, got {response_json.get(key)}"

#testing pets from excel table | Positive
@pytest.mark.parametrize("pet_id, pet_name, category_id, category_name, tag_id, tag_name, status", get_pet_data_from_excel_pos())
def test_post_pet_from_excel_pos(pet_id, pet_name, category_id, category_name, tag_id, tag_name, status):
    pet_data = new_pet(pet_id, pet_name, category_id, category_name, tag_id, tag_name, status)  
    response = requests.post(f"{ENDPOINT}/pet", json=pet_data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    response_json = response.json()
    for key, expected_value in pet_data.items(): 
        assert str(response_json.get(key)) == str(expected_value), f"Mismatch on {key}: expected {expected_value}, got {response_json.get(key)}"

# testing users from excel table
@pytest.mark.parametrize("user_id, username, firstName, lastName, email, password, phone, userStatus", get_user_data_from_excel())
def test_create_user(user_id, username, firstName, lastName, email, password, phone, userStatus, update_user_data):
    user_data = create_user(user_id, username, firstName, lastName, email, password, phone, userStatus)
    
    try:
        create_response = requests.post(f"{ENDPOINT}/user/", json=user_data)
        assert create_response.status_code == 200, f"Failed to create user: {create_response.status_code}"
        
        get_response = requests.get(f"{ENDPOINT}/user/{username}")
        assert get_response.status_code == 200, f"Unexpected status code on GET: {get_response.status_code}"
        response_json = get_response.json()
        
        for key, expected_value in user_data.items(): 
            assert str(response_json.get(key)) == str(expected_value), f"Mismatch on {key}: expected {expected_value}, got {response_json.get(key)}"
        
        login_response = requests.get(f"{ENDPOINT}/user/login", json={"username": username, "password": password})
        assert login_response.status_code == 200, f"Failed to log in user: {login_response.status_code}"
        
        update_response = requests.put(f"{ENDPOINT}/user/{username}", json=update_user_data)
        assert update_response.status_code == 200, f"Unexpected status code: {update_response.status_code}"
        
        get_updated_response = requests.get(f"{ENDPOINT}/user/{username}")
        assert get_updated_response.status_code == 200, f"Unexpected status code on GET after update: {get_updated_response.status_code}"
        updated_response_json = get_updated_response.json()
        
        for key, expected_value in update_user_data.items(): 
            assert str(updated_response_json.get(key)) == str(expected_value), f"Mismatch on {key}: expected {expected_value}, got {updated_response_json.get(key)}"
    
    finally:
        delete_response = requests.delete(f"{ENDPOINT}/user/{username}") #deleting to avoid filling up the database
        assert delete_response.status_code == 200, f"Failed to delete user: {delete_response.status_code}"

    
"""delete"""
#delete with busy ID
def test_delete_busy_pet_pos():
    response = requests.delete(f"{ENDPOINT}/pet/{find_busy_pet_id()}")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

"""negative tests"""

"""post"""
#post pet with busy ID
def test_post_pet_busy(new_pet_busy):
    response = requests.post(f"{ENDPOINT}/pet", json=new_pet_busy)
    assert response.status_code != 200, f"Why 200. ID is busy." 

#testing pets from excel table | Negative

@pytest.mark.parametrize("pet_id, pet_name, category_id, category_name, tag_id, tag_name, status", get_pet_data_from_excel_neg())
def test_post_pet_from_excel_neg(pet_id, pet_name, category_id, category_name, tag_id, tag_name, status):
    pet_data = new_pet(pet_id, pet_name, category_id, category_name, tag_id, tag_name, status)  
    response = requests.post(f"{ENDPOINT}/pet", json=pet_data)
    assert response.status_code != 200, f"Why 200: ID {category_id} != {category_name} and/or ID {tag_id} != {tag_name}"

"""get pet/{id}"""
#get with free ID
def test_get_pet_free():
    response = requests.get(f"{ENDPOINT}/pet/{find_free_pet_id()}")
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"

"""delete pet/{id}"""
def test_delete_free_pet_neg():
    response = requests.delete(f"{ENDPOINT}/pet/{find_free_pet_id()}")
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
