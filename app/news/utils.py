from news.schemas import NewsFromUserDBSchema


async def transform(item):
    news_obj = NewsFromUserDBSchema.model_validate(item)
    news_dict = news_obj.model_dump(exclude={"created_at", "updated_at", "source_id"})
    news_dict["source"] = news_obj.source.model_dump(exclude={"created_at", "updated_at", "id"})
    return news_dict


