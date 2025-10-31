from pydantic import Field

from api_models.id_model import IDModel


class Meta(IDModel):
    publisher: str
    license: str
    license_name: str = Field(..., alias="licenseName")
    comment: str
    version: str
    has_format: list[str] = Field(..., alias="hasFormat")