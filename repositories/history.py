from . import get_pool

import json

from exceptions.repositories import RepositoryError


class HistoryRepository:
    __tablename__ = "sage_history"

    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    async def create(
        self,
        topic_id: str,
        history_id: str,
        time: str,
        prompt: str,
        model: str,
        file_ids: str,
        extra_data: str,
        answer: str = None,
    ) -> bool:
        """
        创建新话题详情
        """
        _uuid = self.uuid
        _sql = f"INSERT INTO {HistoryRepository.__tablename__} (history_id, uuid, topic_id, prompt, answer, time, model, file, extra_data, is_deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 0)"
        _params = (
            history_id,
            _uuid,
            topic_id,
            prompt,
            answer,
            time,
            model,
            file_ids,
            extra_data,
        )
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    async def read(self, topic_id: str) -> dict:
        """
        获取话题详情
        """
        _uuid = self.uuid
        _sql = f"SELECT history_id, prompt, answer, time, model, file, extra_data FROM {HistoryRepository.__tablename__} WHERE uuid = %s AND topic_id = %s AND is_deleted = 0 ORDER BY time ASC"
        _params = (_uuid, topic_id)
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
                    return await cur.fetchall()

        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    async def update_answer(self, topic_id: str, history_id: str, answer: str) -> bool:
        """
        更新话题answer
        """
        _uuid = self.uuid
        _sql = f"UPDATE {HistoryRepository.__tablename__} SET answer = %s WHERE uuid = %s AND topic_id = %s AND history_id = %s"
        _params = (answer, _uuid, topic_id, history_id)
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    async def update_extra_data(
        self, topic_id: str, history_id: str, extra_data: str
    ) -> bool:
        """
        更新话题extra_data
        """
        _uuid = self.uuid
        _sql = f"UPDATE {HistoryRepository.__tablename__} SET extra_data = %s WHERE uuid = %s AND topic_id = %s AND history_id = %s"
        _params = (extra_data, _uuid, topic_id, history_id)
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
        except Exception as e:
            raise RepositoryError(e, _sql, _params)

    async def delete(self, topic_id: str) -> bool:
        """
        删除话题详情
        """
        _uuid = self.uuid
        #选择所有topic_id的数据，把他们的is_deleted改为1
        _sql = f"UPDATE {HistoryRepository.__tablename__} SET is_deleted = 1 WHERE uuid = %s AND topic_id = %s"
        _params = (_uuid, topic_id)
        try:
            async with (await get_pool()).acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(_sql, _params)
        except Exception as e:
            raise RepositoryError(e, _sql, _params)