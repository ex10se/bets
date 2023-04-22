from abc import ABC, abstractmethod
from typing import TypeVar, Type

from sqlalchemy import Result, update, select
from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar("Model")
Schema = TypeVar("Schema")


class BaseService(ABC):
    """Базовый класс для сервисов."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @property
    @abstractmethod
    def model(self) -> Type[Model]:
        ...

    @property
    @abstractmethod
    def schema(self) -> Type[Schema]:
        ...

    async def retrieve(self, **kwargs) -> Schema | None:
        result = await self.db_session.execute(
            select(self.model).filter_by(**kwargs),
        )
        return await self.get(result, many=False)

    async def get(
            self, query_result: Result, many: bool, schema: Schema | None = None,
    ) -> Schema | list[Schema] | None:
        if not schema:
            schema = self.schema
        if many:
            return [schema.from_orm(res) for res in query_result.scalars().all()]
        result = query_result.scalars().one_or_none()
        return schema.from_orm(result) if result else None

    async def create(self, schema: Schema | None = None, **kwargs) -> Model:
        if schema is None:
            schema = self.schema
        obj = self.model(**kwargs)
        self.db_session.add(obj)
        await self.db_session.commit()
        return schema.from_orm(obj)

    async def update(self, where: dict, values: dict) -> None:
        await self.db_session.execute(
            update(self.model)
            .where(*(getattr(self.model, key) == value for key, value in where.items()))
            .values(**{key: value for key, value in values.items() if hasattr(self.model, key)}),
        )
        await self.db_session.commit()
