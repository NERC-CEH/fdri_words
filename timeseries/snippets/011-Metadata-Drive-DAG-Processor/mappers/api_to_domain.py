from api_models.dataset_timeseries import TimeSeriesDatasetItem
from api_models.data_processing_configuration import DataProcessingConfiguration, DataProcessingConfigurationItem
from domain_models.time_series_container import ProcessingConfig, TimeSeriesContainer


def map_dataset_item(item: TimeSeriesDatasetItem) -> TimeSeriesContainer:
    t = item.type[0]
    measure = t.measure
    variable = measure.variable.pref_label[0] if measure.variable else None
    unit = measure.has_unit.pref_label[0] if measure.has_unit else None
    agg = measure.aggregation

    methodology = t.methodology
    method_type = None
    method = None
    if methodology:
        method_type = methodology.configuration.type.id.split("/")[-1]
        if methodology.configuration.has_current_configuration:
            method = methodology.configuration.has_current_configuration[0].id.split("/")[-1]

    depends_on = [dep.id for dep in item.depends_on]
    direct_depends_on = [dep.id for dep in item.direct_depends_on]

    return TimeSeriesContainer(
        id=item.id,
        ref_id=t.id,
        resolution=agg.resolution,
        periodicity=agg.periodicity,
        processing_level=t.processing_level.id.split("/")[-1],
        source_bucket=item.source_bucket,
        source_dataset=item.source_dataset,
        source_column=item.source_column_name,
        source_site=item.originating_site[0].id.split("/")[-1],
        variable=variable,
        unit=unit,
        method_type=method_type,
        method=method,
        depends_on=depends_on,
        direct_depends_on=direct_depends_on
    )


def map_processing_config_item(item: DataProcessingConfigurationItem) -> ProcessingConfig:
    """Convert one Pydantic configuration item into a domain ProcessingConfig."""
    config_id = item.id

    # usually there is one current configuration block
    cfg = item.has_current_configuration[0]
    method = cfg.method.id.split("/")[-1]  # e.g. 'battery_v'

    params: dict[str, object] = {}
    dep_ts: list[str] = []

    for arg in cfg.argument:
        param_id = arg.parameter.id.split("/")[-1]
        val = arg.has_value

        if val.value_reference:
            # reference to another time series (dependency)
            dep_ts.append(val.value_reference.id)
        elif param_id == "dep_ts":  # This is specific for correction config.  Is this the best way to do this?
            # reference to another time series (dependency)

            # hack until IDs updated in metadata
            dep_ts_id = val.value
            if dep_ts_id[:6] == "COSMOS":
                dep_ts_id = f"http://fdri.ceh.ac.uk/id/dataset/{dep_ts_id.lower()}"
            dep_ts.append(dep_ts_id)


        elif val.value is not None:
            params[param_id] = val.value

    return ProcessingConfig(
        id=config_id,
        method=method,
        params=params,
        dep_ts=dep_ts,
    )


def map_processing_config_response(resp: DataProcessingConfiguration) -> list[ProcessingConfig]:
    return [map_processing_config_item(i) for i in resp.items]