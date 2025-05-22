from exceptions.repositories import RepositoryError
from . import get_pool


class TokenRepository:

    __tablename__ = "sage_tokens"

    def __init__(self):
        pass

    @staticmethod
    async def create(uuid: str, token: str):
        """
        创建访问令牌
        """

        _sql = (
            f"INSERT INTO {TokenRepository.__tablename__} (uuid, token) VALUES (%s,%s)"
        )
        _params = (
            uuid,
            token,
        )
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    await conn.commit()
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    @staticmethod
    async def read(uuid: str) -> str:
        """
        读取访问令牌
        """
        _sql = f"SELECT token FROM {TokenRepository.__tablename__} WHERE uuid = %s"
        _params = (uuid,)
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    result = await cur.fetchone()
                    return result
                
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    @staticmethod
    async def update(uuid: str, token: str):
        """
        更新访问令牌
        """
        _sql = f"UPDATE {TokenRepository.__tablename__} SET token = %s WHERE uuid = %s"
        _params = (
            token,
            uuid,
        )
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    await conn.commit()
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    @staticmethod
    async def check(token: str):
        """
        检查访问令牌
        """

        _sql = f"SELECT * FROM {TokenRepository.__tablename__} WHERE token = %s "
        _params = (token,)
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    result = await cur.fetchone()
                    return True if result else False
        except Exception as e:
            raise RepositoryError(e, _sql, _params)
