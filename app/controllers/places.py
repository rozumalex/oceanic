from blacksheep.server.controllers import ApiController, get, patch, delete, post
from ..models import PlaceModel
from typing import Optional, List
from dataclasses import dataclass
from uuid import UUID
from pydantic import BaseModel as PydanticBaseModel
from tortoise import Model
from ..models.places import PydanticPlace


__all__ = ["Places"]


class BaseModel(PydanticBaseModel):
    @classmethod
    def from_orms(cls, instances: List[Model]) -> list:
        return [cls.from_orm(instance) for instance in instances]


class APIPlace(BaseModel):
    name: str

    @classmethod
    def from_orms(cls, instances: List[Model]) -> list:
        return [cls.from_orm(instance) for instance in instances]

    class Config:
        orm_mode = True


class APIPlaces(BaseModel):
    place: Optional[List[APIPlace]]

    @classmethod
    def from_qs(cls, qs):
        return cls(items=APIPlace.from_orms(qs))

    class Config:
        orm_mode = True


@dataclass
class APIPlace:
    id: UUID
    name: str


class Places(ApiController):
    # @classmethod
    # def version(cls) -> str:
    #     return "2021-08-27"

    # @classmethod
    # def route(cls) -> str:
    #     return "root_api_route"

    @get("")
    async def list(self):
        places = await PlaceModel.all()
        return self.json([await PydanticPlace.from_tortoise_orm(place) for place in places])

    @post("")
    async def create(self, name: str):
        place = await PlaceModel.create(name=name)
        return self.json(await PydanticPlace.from_tortoise_orm(place))

    @get("/{id}")
    async def retrieve(self, id: UUID):
        place = await PlaceModel.get(id=id)
        return self.json(await PydanticPlace.from_tortoise_orm(place))

    @patch("/{id}")
    async def patch(self, id: UUID, name: str):
        place = await PlaceModel.get(id=id)
        place = await place.update_from_dict({"name": name})
        await place.save()
        return self.json(await PydanticPlace.from_tortoise_orm(place))

    @delete("/{id}")
    async def delete(self, id: UUID):
        place = await PlaceModel.get(id=id)
        await place.delete()
        return self.json("", status=204)
