from typing import Annotated, Any, Generic, Type, TypeVar

from pydantic import BaseModel, BeforeValidator, Field


class IDModel(BaseModel):
    """Base model with ID.

    Attributes:
        id: The unique identifier for the model.
    """
    id: str = Field(..., alias="@id")
