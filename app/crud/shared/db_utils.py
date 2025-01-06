from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException


def fetch_by_id(db_session: Session, model, item_id, not_found_message):
    item = db_session.execute(
        select(model).where(model.id == item_id)
    ).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail=not_found_message)
    return item


def ensure_unique(db_session: Session, model, field, value, error_message):
    if db_session.execute(
        select(model).where(getattr(model, field) == value)
    ).scalar_one_or_none():
        raise HTTPException(status_code=400, detail=error_message)


def ensure_association_does_not_exist(db_session: Session, model, **kwargs):
    if db_session.execute(select(model).filter_by(**kwargs)).scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Association already exists")


def fetch_association(db_session: Session, model, not_found_message, **kwargs):
    association = db_session.execute(
        select(model).filter_by(**kwargs)
    ).scalar_one_or_none()
    if not association:
        raise HTTPException(status_code=404, detail=not_found_message)
    return association
