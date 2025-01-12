import pytest
from fastapi import status


valid_user_data = {
    "name": "John",
    "surname": "Doe",
    "email": "johndoe@example.com",
    "password": "ValidPass123",
}

update_data = {
    "name": "John Updated",
    "surname": "Doe Updated",
    "email": "johnupdated@example.com",
}


@pytest.fixture
def create_sample_user(client):
    response = client.post("sessions/sign_up", json=valid_user_data)
    assert response.status_code == status.HTTP_201_CREATED


# Test for successful sign-up
def test_sign_up_user(client):
    response = client.post("sessions/sign_up", json=valid_user_data)
    assert response.status_code == status.HTTP_201_CREATED


# Test for sign-up with existing email
def test_sign_up_user_existing_email(client, create_sample_user):
    response = client.post("sessions/sign_up", json=valid_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Email already in use"}


# Test for successful sign-in
def test_sign_in_user(client, create_sample_user):
    sign_in_data = {
        "email": valid_user_data["email"],
        "password": valid_user_data["password"],
    }
    response = client.post("sessions/sign_in", json=sign_in_data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


# Test for sign-in with incorrect password
def test_sign_in_user_invalid_password(client, create_sample_user):
    invalid_data = {"email": valid_user_data["email"], "password": "WrongPassword123"}
    response = client.post("sessions/sign_in", json=invalid_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid password"}


# Test for sign-in with non-existent email
def test_sign_in_user_non_existent_email(client):
    sign_in_data = {"email": "nonexistent@example.com", "password": "ValidPass123"}
    response = client.post("sessions/sign_in", json=sign_in_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


# Test for fetching current user details
def test_show_current_user(authorized_client):
    response = authorized_client.get("sessions/current_user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "user@example.com"
    assert response.json()["name"] == "User"
    assert response.json()["surname"] == "User"


# Test for updating the current user details
def test_update_current_user(authorized_client):
    response = authorized_client.patch("sessions/current_user", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == update_data["email"]
    assert response.json()["name"] == update_data["name"]


# Test for updating current user with email already in use
def test_update_current_user_existing_email(authorized_client):
    # Create another user to conflict
    authorized_client.post(
        "sessions/sign_up",
        json={
            "name": "Jane",
            "surname": "Doe",
            "email": "janedoe@example.com",
            "password": "ValidPass123",
        },
    )

    # Try updating to the existing email
    update_data["email"] = "janedoe@example.com"
    response = authorized_client.patch("sessions/current_user", json=update_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Email already in use"}


# Test for deleting the current user
def test_delete_current_user(authorized_client):
    response = authorized_client.delete("sessions/current_user")
    assert response.status_code == status.HTTP_204_NO_CONTENT
