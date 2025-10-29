from pydantic import BaseModel

from api_models.dataset_timeseries import TimeSeriesDatasetItem
from api_models.meta import Meta


class DatasetDependencies(BaseModel):
    meta: Meta
    items: list[TimeSeriesDatasetItem]
