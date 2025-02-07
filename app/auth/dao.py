from dao.base import BaseDAO
from auth.models import User, Role


class UsersDAO(BaseDAO):
    model = User


class RoleDAO(BaseDAO):
    model = Role
