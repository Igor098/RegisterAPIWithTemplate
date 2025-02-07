from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dao.database import Base, str_uniq


class Source(Base):

    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

    news = relationship("News", back_populates="source")

    __exclude__ = ['created_at', 'updated_at']


class News(Base):
    __tablename__ = "news"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    content: Mapped[str]
    url: Mapped[str]
    image: Mapped[str]
    publishedAt: Mapped[str]
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("sources.id"))
    source = relationship("Source", back_populates="news")

    __exclude__ = ['created_at', 'updated_at']


class NewsUsers(Base):
    __tablename__ = "news_users"

    id = None
    news_id: Mapped[str] = mapped_column(String, ForeignKey("news.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True, autoincrement=False)