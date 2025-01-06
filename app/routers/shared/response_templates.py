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
