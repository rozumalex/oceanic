from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

__all__ = ["PlaceModel"]


class PlaceModel(Model):
    id = fields.UUIDField(pk=True)
    name = fields.TextField()

    class Meta:
        ordering: list = ["name"]
        table: str = "users"

    def __str__(self):
        return self.name


PydanticPlace = pydantic_model_creator(PlaceModel)
