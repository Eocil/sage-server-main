from . import get_pool

from exceptions.repositories import RepositoryError


class TopicRepository:

    __tablename__ = "sage_topics"

    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    async def create(self, topic_id: str, title: str, time: str) -> bool:
        """
        创建新话题
        """
        _uuid = self.uuid
        _sql = f"INSERT INTO {TopicRepository.__tablename__} (uuid, topic_id, title, time) VALUES (%s, %s, %s, %s)"
        _params = (
            _uuid,
            topic_id,
            title,
            time,
        )
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    await conn.commit()
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    async def update_title(self, topic_id: str, title: str) -> bool:
        """
        更新话题标题
        """
        _uuid = self.uuid
        _sql = f"UPDATE {TopicRepository.__tablename__} SET title = %s WHERE uuid = %s AND topic_id = %s"
        _params = (
            title,
            _uuid,
            topic_id,
        )
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    await conn.commit()
        except Exception as e:
            raise RepositoryError(e, _sql, _params)
        
    async def read(self, topic_id: str) -> dict:
        """
        获取话题
        """
        _uuid = self.uuid
        _sql = f"SELECT topic_id, title, time FROM {TopicRepository.__tablename__} WHERE uuid = %s AND topic_id = %s AND is_deleted = 0"
        _params = (
            _uuid,
            topic_id,
        )
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    result = await cur.fetchone()
                    return result if result else None
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    async def read_all(self, offset: int, limit: int) -> dict:
        """
        获取所有话题
        """
        _uuid = self.uuid
        _sql = f"SELECT topic_id, title, time FROM {TopicRepository.__tablename__} WHERE uuid = %s AND is_deleted = 0 ORDER BY time DESC LIMIT %s OFFSET %s"
        _params = (
            _uuid,
            limit,
            offset,
        )
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    result = await cur.fetchall()
                    return result if result else None
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    async def delete(self, topic_id: str) -> bool:
        """
        伪删除话题
        """
        _uuid = self.uuid
        _sql = f"UPDATE {TopicRepository.__tablename__} SET is_deleted = 1 WHERE uuid = %s AND topic_id = %s"
        _params = (
            _uuid,
            topic_id,
        )
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    await conn.commit()
        except Exception as e:
            raise RepositoryError(e, _sql, _params)
