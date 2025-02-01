import asyncio
from functools import reduce

from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.news.models import News, Source, NewsUsers
from app.news.utils import transform


class NewsDAO(BaseDAO):
    model = News


class SourceDAO(BaseDAO):
    model = Source


class NewsUsersDAO(BaseDAO):
    model = NewsUsers

    async def get_news_by_user_id(self, user_id: int):

        try:
            query = (((select(News)
                     .join(self.model, self.model.news_id == News.id)
                     .filter(self.model.user_id == user_id))
                     .options(joinedload(News.source))))

            result = await self._session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            if records:
                news_list = await asyncio.gather(*map(transform, records))

                return news_list

            return []

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей по id {user_id}: {e}")
            raise
