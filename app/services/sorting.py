from sqlalchemy import asc, desc, select


def apply_sorting(stmt: select, sorting_params, sort_fields: dict) -> select:
    field = sorting_params.sort_by
    order = sorting_params.sort_order
    column = sort_fields[field]

    return stmt.order_by(asc(column) if order == "asc" else desc(column))
