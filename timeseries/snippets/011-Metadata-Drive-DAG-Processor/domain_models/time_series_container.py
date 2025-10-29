from dataclasses import dataclass, field, asdict
from typing import Any
from time_stream import TimeFrame


@dataclass
class ProcessingConfig:
    id: str
    method: str
    params: dict[str, Any] = field(default_factory=dict)
    dep_ts: list[str] = field(default_factory=list)


@dataclass
class TimeSeriesContainer:
    id: str
    ref_id: str

    resolution: str | None = None
    periodicity: str | None = None
    processing_level: str | None = None

    source_bucket: str | None = None
    source_dataset: str | None = None
    source_column: str | None = None
    source_site: str | None = None

    variable: str | None = None
    unit: str | None = None

    method_type: str | None = None
    method: str | None = None

    depends_on: list[str] = field(default_factory=list)
    direct_depends_on: list[str] = field(default_factory=list)

    configs: list[ProcessingConfig] = field(default_factory=list)
    # correction_configs: list[ProcessingConfig] = field(default_factory=list)
    # qc_configs: list[ProcessingConfig] = field(default_factory=list)
    # infill_configs: list[ProcessingConfig] = field(default_factory=list)

    data: TimeFrame | None = None

    def all_dependencies(self) -> list[str]:
        deps = set(self.depends_on)
        for c in self.configs:
            deps.update(c.dep_ts)

        return sorted(deps)

    def load(self) -> bool:
        """If the time series doesn't have a method then this is a "base" level time series that we can load from the
        raw bucket
        """
        return self.method is None