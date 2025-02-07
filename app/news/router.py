from typing import List

from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from dependencies.auth_dep import get_current_user
from dependencies.dao_dep import get_session_with_commit, get_session_without_commit
from exceptions import ArticleAlreadyAddedFromUser, ArticleNotFoundException
from news.dao import SourceDAO, NewsDAO, NewsUsersDAO
from news.schemas import SSourceModel, NewsModel, SourceModel, SNewsAddModel, NewsUsersModel, \
    SNewsModel, UserNews, AnswerOk, DeletedNewsSchema

router = APIRouter()


@router.get("/")
async def get_news(
        user_data: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_without_commit)
) -> List[UserNews]:
    news_dao = NewsUsersDAO(session)
    return await news_dao.get_news_by_user_id(user_id=user_data.id)


@router.post("/add")
async def add_news(
        article: NewsModel,
        user_data: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_with_commit)
) -> NewsModel:

    source_dao = SourceDAO(session)
    news_dao = NewsDAO(session)
    news_users_dao = NewsUsersDAO(session)

    search_article = await news_dao.find_one_or_none(filters=SNewsModel(title=article.title))

    if not search_article:
        article_data_dict = article.model_dump()
        source = await source_dao.find_one_or_none(
            filters=SSourceModel(name=article_data_dict.get("source").get("name")))

        if not source:
            source = await source_dao.add(values=SourceModel(**article_data_dict["source"]))

        article_data_dict.pop("source")
        logger.debug(article_data_dict)
        search_article = await news_dao.add(values=SNewsAddModel(**article_data_dict, source_id=source.id))

    search_user_news = await news_users_dao.find_one_or_none(
        filters=NewsUsersModel(user_id=user_data.id, news_id=search_article.id))
    if search_user_news:
        logger.error("Такая новость уже добавлена")
        raise ArticleAlreadyAddedFromUser

    await news_users_dao.add(values=NewsUsersModel(user_id=user_data.id, news_id=search_article.id))

    return article


@router.delete("/delete")
async def delete_news(
        article_id: str,
        user_data: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_with_commit)
) -> DeletedNewsSchema:

    news_users_dao = NewsUsersDAO(session)
    search_article = await news_users_dao.find_one_or_none(filters=NewsUsersModel(user_id=user_data.id, news_id=article_id))
    if not search_article:
        raise ArticleNotFoundException

    await news_users_dao.delete(filters=NewsUsersModel(user_id=user_data.id, news_id=article_id))

    return DeletedNewsSchema(id=article_id)