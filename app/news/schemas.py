import datetime
from typing import Optional

from pydantic import Field, BaseModel, ConfigDict
from datetime import datetime


class AnswerOk(BaseModel):
    ok: bool
    message: str


class SSourceModel(BaseModel):
    name: str = Field(min_length=3, max_length=50, description="Название ресурса, от 4 до 50 символов")
    model_config = ConfigDict(from_attributes=True)


class SourceModel(BaseModel):
    name: str = Field(min_length=3, max_length=50, description="Название ресурса, от 4 до 50 символов")
    url: str = Field(min_length=3, max_length=50, description="Ссылка на ресурс, от 4 до 50 символов")
    model_config = ConfigDict(from_attributes=True)


class SourceSchema(BaseModel):
    id: int
    name: str
    url: str

    model_config = ConfigDict(from_attributes=True)


class NewsModel(BaseModel):
    id: str = Field(min_length=3, max_length=50, description="Уникальный идентификатор UUID")
    title: str = Field(min_length=4, max_length=50, description="Заголовок для новости, от 4 до 50 символов")
    description: str = Field(min_length=4, description="Краткое описание новости, от 4 символов")
    content: str = Field(min_length=20, description="Полное описание новости, от 20 символов")
    url: str = Field(min_length=4, max_length=100, description="Ссылка на новость, от 4 до 100 символов")
    image: str = Field(min_length=4, max_length=100, description="Ссылка на изображение, от 4 до 100 символов")
    publishedAt: str
    source: SourceModel
    model_config = ConfigDict(from_attributes=True)


class SNewsAddModel(BaseModel):
    id: str = Field(min_length=3, max_length=50, description="Уникальный идентификатор UUID")
    title: str = Field(min_length=4, max_length=50, description="Заголовок для новости, от 4 до 50 символов")
    description: str = Field(min_length=4, description="Краткое описание новости, от 4 символов")
    content: str = Field(min_length=20, description="Полное описание новости, от 20 символов")
    url: str = Field(min_length=4, max_length=100, description="Ссылка на новость, от 4 до 100 символов")
    image: str = Field(min_length=4, max_length=100, description="Ссылка на изображение, от 4 до 100 символов")
    publishedAt: str
    source_id: int
    model_config = ConfigDict(from_attributes=True)


class SNewsModel(BaseModel):
    title: str = Field(min_length=4, max_length=50, description="Заголовок для новости, от 4 до 50 символов")


class NewsUsersModel(BaseModel):
    news_id: str = Field(min_length=3, max_length=50, description="Уникальный идентификатор UUID")
    user_id: int


class SNewsUsersModel(BaseModel):
    user_id: int


class SourceFromDBSchema(BaseModel):
    id: int
    url: str
    name: str
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NewsFromUserDBSchema(BaseModel):
    id: str
    content: str
    url: str
    publishedAt: str
    title: str
    description: str
    image: str
    source_id: int
    source: SourceFromDBSchema
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserSource(BaseModel):
    url: str
    name: str


class UserNews(BaseModel):
    id: str
    content: str
    url: str
    publishedAt: str
    title: str
    description: str
    image: str
    source: UserSource
