from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView
from app.config import engine, settings
from app.models import Book, Author, Genre, User
from app.admin.auth import EmailAndPasswordProvider, pwd_context

admin = Admin(
    engine,
    title="Library Admin Panel",
    auth_provider=EmailAndPasswordProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=settings.COOKIE_SECRET_KEY)],
)


class CustomModelView(ModelView):
    exclude_fields_from_create = ["created_at", "updated_at"]
    exclude_fields_from_edit = ["created_at", "updated_at"]


class UserAdmin(CustomModelView):
    async def before_create(self, request, data: dict, item: User) -> None:
        if item.hashed_password and not item.hashed_password.startswith("$"):
            item.hashed_password = pwd_context.hash(item.hashed_password)

    async def before_edit(self, request, data: dict, item: User) -> None:
        if item.hashed_password and not item.hashed_password.startswith("$"):
            item.hashed_password = pwd_context.hash(item.hashed_password)


admin.add_view(UserAdmin(User, name="Users"))
admin.add_view(CustomModelView(Book, name="Books"))
admin.add_view(CustomModelView(Author, name="Authors"))
admin.add_view(CustomModelView(Genre, name="Genres"))
