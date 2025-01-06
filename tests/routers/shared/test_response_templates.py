from app.routers.shared.response_templates import (
    not_found_response,
    bad_request_response,
    combine_responses,
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
