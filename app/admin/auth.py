from sqlalchemy.future import select
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed
from app.models import User
from app.config import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EmailAndPasswordProvider(AuthProvider):
    async def login(
        self,
        email: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        db = next(get_db())
        stmt = select(User).where(User.email == email)
        result = db.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise LoginFailed("Invalid email or password")
        if not pwd_context.verify(password, user.hashed_password):
            raise LoginFailed("Invalid email or password")
        if not user.is_admin():
            raise LoginFailed("Access denied. User is not admin")

        request.session["user_id"] = user.id
        return response

    async def is_authenticated(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        if user_id is None:
            return False

        db = next(get_db())
        stmt = select(User).where(User.id == user_id)
        result = db.execute(stmt)
        user = result.scalar_one_or_none()

        if user and user.is_admin():
            request.state.user = user
            return True
        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user: User = request.state.user
        custom_app_title = f"Hello, {user.name}!"
        return AdminConfig(app_title=custom_app_title)

    def get_admin_user(self, request: Request) -> AdminUser:
        user: User = request.state.user
        return AdminUser(username=user.name)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
