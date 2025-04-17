from fastapi import HTTPException
from sqlalchemy import select

ALLOWED_OPERATORS = {"eq", "ne", "lt", "lte", "gt", "gte", "like", "ilike", "in"}


def parse_filter(raw_value: str):
    if ":" in raw_value:
        operator, value = raw_value.split(":", 1)
        if operator not in ALLOWED_OPERATORS:
            raise HTTPException(
                status_code=422, detail=f"Unsupported filter operator: '{operator}'"
            )
    else:
        operator = "eq"
        value = raw_value
    return operator, value


def apply_filters(stmt: select, filters: dict, allowed_fields: dict) -> select:
    operator_map = {
        "eq": lambda col, val: col == val,
        "ne": lambda col, val: col != val,
        "lt": lambda col, val: col < val,
        "lte": lambda col, val: col <= val,
        "gt": lambda col, val: col > val,
        "gte": lambda col, val: col >= val,
        "like": lambda col, val: col.like(val),
        "ilike": lambda col, val: col.ilike(val),
        "in": lambda col, val: col.in_(val.split(",")),
    }

    for field, raw_value in filters.items():
        if field not in allowed_fields:
            raise HTTPException(
                status_code=422, detail=f"Filtering by '{field}' is not allowed."
            )

        operator, value = parse_filter(raw_value)
        column = allowed_fields[field]

        stmt = stmt.where(operator_map[operator](column, value))

    return stmt
