from pydantic import BaseModel, Field

from api_models.id_model import IDModel
from api_models.meta import Meta


class Variable(IDModel):
    pref_label: list[str] = Field(..., alias='prefLabel')


class HasUnit(IDModel):
    pref_label: list[str] = Field(..., alias='prefLabel')


class Aggregation(IDModel):
    value_statistic: IDModel = Field(..., alias='valueStatistic')
    periodicity: str
    resolution: str


class Measure(IDModel):
    variable: Variable
    has_unit: HasUnit = Field(..., alias='hasUnit')
    aggregation: Aggregation


class HasCurrentConfigurationItem(IDModel):
    method: IDModel | None = None


class Configuration(IDModel):
    type: IDModel
    has_current_configuration: list[HasCurrentConfigurationItem] = Field(..., alias='hasCurrentConfiguration')


class Methodology(IDModel):
    uses: list[IDModel]
    configuration: Configuration


class TypeItem(IDModel):
    processing_level: IDModel = Field(..., alias='processingLevel')
    measure: Measure
    methodology: Methodology | None = None


class TimeSeriesDatasetItem(IDModel):
    field_type: list[IDModel] = Field(..., alias='@type')
    type: list[TypeItem]
    source_bucket: str | None = Field(None, alias='sourceBucket')
    source_dataset: str | None = Field(None, alias='sourceDataset')
    source_column_name: str | None = Field(None, alias='sourceColumnName')
    originating_facility: list[IDModel] | None = Field(None, alias="originatingFacility")
    originating_site: list[IDModel] | None = Field(None, alias='originatingSite')
    depends_on: list[IDModel] = Field(default_factory=list, alias="dependsOn")
    direct_depends_on: list[IDModel] = Field(default_factory=list, alias="directDependsOn")


class TimeSeriesDataset(BaseModel):
    meta: Meta
    items: list[TimeSeriesDatasetItem]
