from app.routers.shared.response_templates import (
    not_found_response,
    bad_request_response,
    combine_responses,
    invalid_authentication_responses,
    invalid_password_response,
    filtering_validation_error_response,
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


def test_invalid_authentication_responses():
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
                        "non_existent_user": {
                            "summary": "Token pointing to non-existent user",
                            "value": {"detail": "Token pointing to non-existent user"},
                        },
                    }
                }
            },
        },
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "examples": {
                        "not_authenticated": {
                            "summary": "Not authenticated",
                            "value": {"detail": "Not authenticated"},
                        },
                        "insufficient_rights": {
                            "summary": "Insufficient rights",
                            "value": {"detail": "Insufficient rights"},
                        },
                    }
                }
            },
        },
    }
    assert invalid_authentication_responses() == expected


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


def test_filtering_validation_error_response():
    expected = {
        "422": {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "examples": {
                        "unsupported_operator": {
                            "summary": "Unsupported filter operator",
                            "value": {
                                "detail": "Unsupported filter operator: '<operator>'"
                            },
                        },
                        "disallowed_field": {
                            "summary": "Filtering by field not allowed",
                            "value": {
                                "detail": "Filtering by '<field>' is not allowed."
                            },
                        },
                    }
                }
            },
        }
    }
    assert filtering_validation_error_response() == expected


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
