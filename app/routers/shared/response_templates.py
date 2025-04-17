def not_found_response(entity: str):
    return {
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        f"{entity}_not_found": {
                            "summary": f"{entity.capitalize()} not found",
                            "value": {"detail": f"{entity.capitalize()} not found"},
                        }
                    }
                }
            },
        }
    }


def bad_request_response(detail: str):
    return {
        "400": {
            "description": "Bad Request",
            "content": {"application/json": {"example": {"detail": detail}}},
        }
    }


def invalid_authentication_responses():
    return {
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


def invalid_password_response():
    return {
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {"example": {"detail": "Invalid password"}}
            },
        }
    }


def filtering_validation_error_response():
    return {
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


def combine_responses(*responses):
    combined = {}
    for response in responses:
        for status_code, content in response.items():
            if status_code not in combined:
                combined[status_code] = content
            else:
                combined[status_code]["content"]["application/json"]["examples"].update(
                    content["content"]["application/json"]["examples"]
                )
    return combined
