from app.routers.shared.response_templates import (
    not_found_response,
    bad_request_response,
    combine_responses,
    not_authenticated_response,
    invalid_token_responses,
    invalid_password_response,
)


def test_not_found_response():
    entity = "user"
    expected = {
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "user_not_found": {
                            "summary": "User not found",
                            "value": {"detail": "User not found"},
                        }
                    }
                }
            },
        }
    }
    assert not_found_response(entity) == expected


def test_bad_request_response():
    detail = "Invalid input"
    expected = {
        "400": {
            "description": "Bad Request",
            "content": {"application/json": {"example": {"detail": detail}}},
        }
    }
    assert bad_request_response(detail) == expected


def test_not_authenticated_response():
    expected = {
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {"example": {"detail": "Not authenticated"}}
            },
        }
    }
    assert not_authenticated_response() == expected


def test_invalid_token_responses():
    expected = {
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "examples": {
                        "token_expired": {
                            "summary": "Token expired",
                            "value": {"detail": "Token has expired"},
                        },
                        "invalid_token": {
                            "summary": "Invalid token",
                            "value": {"detail": "Invalid token"},
                        },
                    }
                }
            },
        }
    }
    assert invalid_token_responses() == expected


def test_invalid_password_response():
    expected = {
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {"example": {"detail": "Invalid password"}}
            },
        }
    }
    assert invalid_password_response() == expected


def test_combine_responses():
    response1 = not_found_response("user")
    response2 = not_found_response("product")
    response3 = bad_request_response("Invalid input")
    combined = combine_responses(response1, response2, response3)

    expected = {
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "user_not_found": {
                            "summary": "User not found",
                            "value": {"detail": "User not found"},
                        },
                        "product_not_found": {
                            "summary": "Product not found",
                            "value": {"detail": "Product not found"},
                        },
                    }
                }
            },
        },
        "400": {
            "description": "Bad Request",
            "content": {"application/json": {"example": {"detail": "Invalid input"}}},
        },
    }
    assert combined == expected
