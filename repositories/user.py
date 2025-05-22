from . import get_pool

from exceptions.repositories import RepositoryError

class UserRepository:
    __tablename__ = "sage_users"


    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    async def create(
        self, username: str, email: str, hashed_password: str, group: str
    ) -> bool:
        """
        创建新用户
        """
        _uuid = self.uuid
        _sql = f"INSERT INTO {UserRepository.__tablename__} (uuid,email,username,  hashed_password, `group`) VALUES (%s, %s, %s, %s, %s)"
        _params = (
            _uuid,
            email,
            username,
            hashed_password,
            group,
        )
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    await conn.commit()
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    @staticmethod
    async def check_email(email: str) -> bool:
        """
        检查邮箱是否已经注册
        """
        _sql = f"SELECT * FROM {UserRepository.__tablename__} WHERE email = %s"
        _params = (email,)
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    result = await cur.fetchone()
                    return True if result else False
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    @staticmethod
    async def read_by_email(email: str) -> dict:
        """
        通过邮箱获取用户信息
        """
        _sql = f"SELECT * FROM {UserRepository.__tablename__} WHERE email = %s"
        _params = (email,)
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    result = await cur.fetchone()
                    return result if result else None
        except Exception as e:
            raise RepositoryError(e, _sql, _params)
        
    async def read(self) -> dict:
        """
        通过uuid获取用户信息
        """
        _uuid = self.uuid
        _sql = f"SELECT * FROM {UserRepository.__tablename__} WHERE uuid = %s"
        _params = (_uuid,)
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    result = await cur.fetchone()
                    return result if result else None
        except Exception as e:
            raise RepositoryError(e, _sql, _params)
