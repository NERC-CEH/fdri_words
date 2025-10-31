from pydantic import BaseModel, Field

from api_models.id_model import IDModel
from api_models.meta import Meta


class AppliesToTimeSeries(IDModel):
    originating_site: IDModel = Field(..., alias="originatingSite")


class HasValue(IDModel):
    value: int | float | str | None = None
    field_type: list[IDModel] | None = Field(None, alias="@type")
    value_reference: IDModel | None = Field(None, alias="valueReference")


class ArgumentItem(IDModel):
    has_value: HasValue = Field(..., alias="hasValue")
    parameter: IDModel
    field_type: list[IDModel] = Field(..., alias="@type")


class ObservationInterval(IDModel):
    field_type: list[IDModel] = Field(..., alias="@type")
    start_date: str = Field(..., alias="startDate")


class HasCurrentConfigurationItem(IDModel):
    argument: list[ArgumentItem]
    method: IDModel
    field_type: list[IDModel] = Field(..., alias="@type")
    observation_interval: ObservationInterval | None = Field(
        None, alias="observationInterval"
    )


class HasAnnotationItem(IDModel):
    has_value: HasValue = Field(..., alias="hasValue")
    property: IDModel
    field_type: list[IDModel] = Field(..., alias="@type")


class DataProcessingConfigurationItem(IDModel):
    applies_to_time_series: list[AppliesToTimeSeries] = Field(..., alias="appliesToTimeSeries")
    has_annotation: list[HasAnnotationItem] | None = Field(None, alias="hasAnnotation")
    has_current_configuration: list[HasCurrentConfigurationItem] = Field(..., alias="hasCurrentConfiguration")
    type: IDModel
    field_type: list[IDModel] = Field(..., alias="@type")


class DataProcessingConfiguration(BaseModel):
    meta: Meta
    items: list[DataProcessingConfigurationItem]
