import pytest
from sqlalchemy import Table, MetaData, Column, Integer, String, select
from sqlalchemy.dialects import postgresql
from fastapi import HTTPException

from app.services.search import parse_filter, apply_filters

@pytest.fixture
def user_table():
    metadata = MetaData()
    table = Table(
        'users', metadata,
        Column('id', Integer, primary_key=True),
        Column('age', Integer),
        Column('name', String),
    )
    return table


def compile_query(stmt):
    return str(
        stmt.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True}
        )
    )


class TestParseFilter:
    def test_default_operator_eq(self):
        op, val = parse_filter("123")
        assert op == "eq"
        assert val == "123"

    def test_valid_operator(self):
        op, val = parse_filter("lt:5")
        assert op == "lt"
        assert val == "5"

    def test_invalid_operator(self):
        with pytest.raises(HTTPException) as exc:
            parse_filter("bad:val")
        assert exc.value.status_code == 422
        assert "Unsupported filter operator" in str(exc.value.detail)


class TestApplyFilters:
    def test_eq_filter(self, user_table):
        stmt = select(user_table)
        filters = {"age": "30"}
        allowed = {"age": user_table.c.age, "name": user_table.c.name}
        result = apply_filters(stmt, filters, allowed)
        sql = compile_query(result)
        assert "users.age = '30'" in sql

    def test_ne_filter(self, user_table):
        stmt = select(user_table)
        filters = {"age": "ne:20"}
        allowed = {"age": user_table.c.age}
        result = apply_filters(stmt, filters, allowed)
        sql = compile_query(result)
        assert "users.age != '20'" in sql

    def test_lt_filter(self, user_table):
        stmt = select(user_table)
        filters = {"age": "lt:50"}
        allowed = {"age": user_table.c.age}
        result = apply_filters(stmt, filters, allowed)
        sql = compile_query(result)
        assert "users.age < '50'" in sql

    def test_lte_filter(self, user_table):
        stmt = select(user_table)
        filters = {"age": "lte:25"}
        allowed = {"age": user_table.c.age}
        sql = compile_query(apply_filters(stmt, filters, allowed))
        assert "users.age <= '25'" in sql

    def test_gt_filter(self, user_table):
        stmt = select(user_table)
        filters = {"age": "gt:18"}
        allowed = {"age": user_table.c.age}
        sql = compile_query(apply_filters(stmt, filters, allowed))
        assert "users.age > '18'" in sql

    def test_gte_filter(self, user_table):
        stmt = select(user_table)
        filters = {"age": "gte:21"}
        allowed = {"age": user_table.c.age}
        sql = compile_query(apply_filters(stmt, filters, allowed))
        assert "users.age >= '21'" in sql

    def test_like_filter(self, user_table):
        stmt = select(user_table)
        filters = {"name": "like:John%"}
        allowed = {"name": user_table.c.name}
        sql = compile_query(apply_filters(stmt, filters, allowed))
        assert "users.name LIKE 'John%%'" in sql

    def test_ilike_filter(self, user_table):
        stmt = select(user_table)
        filters = {"name": "ilike:%doe%"}
        allowed = {"name": user_table.c.name}
        sql = compile_query(apply_filters(stmt, filters, allowed))
        assert "users.name ILIKE '%%doe%%'" in sql

    def test_in_filter(self, user_table):
        stmt = select(user_table)
        filters = {"age": "in:20,30,40"}
        allowed = {"age": user_table.c.age}
        sql = compile_query(apply_filters(stmt, filters, allowed))
        assert "users.age IN ('20', '30', '40')" in sql

    def test_invalid_field(self, user_table):
        stmt = select(user_table)
        filters = {"invalid": "1"}
        allowed = {"age": user_table.c.age}
        with pytest.raises(HTTPException) as exc:
            apply_filters(stmt, filters, allowed)
        assert exc.value.status_code == 422
        assert "Filtering by 'invalid' is not allowed." in str(exc.value.detail)

    def test_multiple_filters_combined(self, user_table):
        stmt = select(user_table)
        filters = {"age": "gte:18", "name": "like:J%"}
        allowed = {"age": user_table.c.age, "name": user_table.c.name}
        result = apply_filters(stmt, filters, allowed)
        sql = compile_query(result)
        assert "users.age >= '18'" in sql
        assert "users.name LIKE 'J%%'" in sql
