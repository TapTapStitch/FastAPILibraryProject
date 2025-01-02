from sqlalchemy import select, func
from sqlalchemy.orm import Session
from ..schemas.pagination import PaginationParams, PaginatedResponse


def paginate(
    db: Session, stmt: select, pagination: PaginationParams
) -> PaginatedResponse:
    offset = (pagination.page - 1) * pagination.size
    limit = pagination.size

    paginated_stmt = stmt.offset(offset).limit(limit)
    results = db.execute(paginated_stmt).scalars().all()
    subquery = stmt.subquery()
    total_count_stmt = select(func.count()).select_from(subquery)
    total_count = db.execute(total_count_stmt).scalar()
    total_pages = (total_count + pagination.size - 1) // pagination.size

    return PaginatedResponse(
        items=results,
        total=total_count,
        page=pagination.page,
        size=pagination.size,
        pages=total_pages,
    )
