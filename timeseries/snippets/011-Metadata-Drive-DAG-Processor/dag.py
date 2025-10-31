from collections import defaultdict, deque
import requests

from api_models.data_processing_configuration import DataProcessingConfiguration
from api_models.dataset_timeseries import TimeSeriesDataset
from api_models.dataset_dependencies import DatasetDependencies
from domain_models.time_series_container import TimeSeriesContainer, ProcessingConfig
from mappers.api_to_domain import map_dataset_item, map_processing_config_item


class DagBuilder:
    """
    Build a metadata-driven DAG by starting from a single target dataset and
    recursively resolving:
      - instance-ready dependencies via /{dataset_id}/_dependencies.json
      - configuration dependencies via data-processing-configuration?appliesToTimeSeries=...
    """

    def __init__(self, session: requests.Session | None = None):
        self.http = session or requests.Session()
        self.datasets: dict[str, TimeSeriesContainer] = {}
        self._cache: dict[str, TimeSeriesContainer] = {}
        self._dependency_cache: list[str] = []

    def _get(self, url: str) -> dict:
        r = self.http.get(url, timeout=30)
        r.raise_for_status()
        return r.json()

    def fetch_processed_dataset(
        self, sites: str | list[str], resolution: str, variables: str | list[str]
    ) -> list[TimeSeriesContainer]:
        """
        Resolve the *processed* dataset for (site, resolution, variable), using the /id/dataset.json search endpoint.
        """
        if isinstance(sites, str):
            sites = [sites]

        if isinstance(variables, str):
            variables = [variables]

        sites_part = "".join(
            [
                f"&originatingSite=http://fdri.ceh.ac.uk/id/site/cosmos-{site.lower()}"
                for site in sites
            ]
        )
        variables_part = "".join(
            [f"&sourceColumnName={variable.upper()}" for variable in variables]
        )

        url = (
            "https://dri-metadata-api.staging.eds.ceh.ac.uk/id/dataset.json"
            "?_view=timeseries"
            f"{sites_part}"
            f"&type.measure.aggregation.periodicity={resolution}"
            f"{variables_part}"
            f"&type.processingLevel=http://fdri.ceh.ac.uk/ref/common/processing-level/processed"
        )
        print(url)
        js = self._get(url)

        parsed = TimeSeriesDataset.model_validate(js)

        containers = []
        for item in parsed.items:
            container = map_dataset_item(item)
            self._cache[container.id] = container
            containers.append(container)

        return containers

    def fetch_dataset_by_id(self, dataset_id: str) -> TimeSeriesContainer:
        """
        Fetch a specific dataset by instance ID.
        """
        dataset_id = dataset_id.lower()  # WORKAROUND FOR CORRECTION CONFIG DEP_ID ISSUE

        # WORKAROUND FOR PRECIP DIAG TYPO
        if "precip_diag_30min_raw" in dataset_id:
            dataset_id = dataset_id.replace("precip_diag_30min_raw", "-precip_diag_30min_raw")

        if dataset_id in self._cache:
            return self._cache[dataset_id]

        url = f"https://dri-metadata-api.staging.eds.ceh.ac.uk/id/dataset/{dataset_id.split('/')[-1]}.json?_view=timeseries"
        print(url)
        js = self._get(url)

        parsed = TimeSeriesDataset.model_validate(js)
        container = map_dataset_item(parsed.items[0])
        self._cache[container.id] = container
        return container

    def fetch_dependencies(self, dataset_id: str) -> list[TimeSeriesContainer]:
        """
        Fetch instance-ready dependencies for the dataset
        """
        url = (f"https://dri-metadata-api.staging.eds.ceh.ac.uk/id/dataset/"
               f"{dataset_id.split('/')[-1]}/_all_dependencies.json")
        print(url)
        js = self._get(url)

        parsed = DatasetDependencies.model_validate(js)

        containers = []
        for item in parsed.items:
            container = map_dataset_item(item)
            self._cache[container.id] = container
            containers.append(container)

        return containers

    def fetch_configs_for_dataset(self, dataset_id: str) -> list[ProcessingConfig]:
        types = ("infill-configuration", "qc", "correction-configuration")
        types_part = "".join([
            f"&type=http://fdri.ceh.ac.uk/ref/common/configuration-type/{t}" for t in types
        ])

        url = (f"https://dri-metadata-api.staging.eds.ceh.ac.uk/id/data-processing-configuration.json?"
               f"appliesToTimeSeries={dataset_id}{types_part}")
        js = self._get(url)
        print(url)

        parsed = DataProcessingConfiguration.model_validate(js)
        return [map_processing_config_item(item) for item in parsed.items]

    def build_from_target(
        self, sites: str | list[str], resolution: str, variables: str | list[str]
    ) -> dict[str, list[str]]:
        """
        Entry point: resolve target processed dataset, recursively walk deps, return DAG.
        """
        root_datasets = self.fetch_processed_dataset(sites, resolution, variables)
        for container in root_datasets:
            self._resolve_dataset(container)

        # clear the caches
        self._cache = {}
        self._dependency_cache = []

        return self._build_dag()

    def _resolve_dataset(self, container: TimeSeriesContainer):
        if container.id in self.datasets:
            return
        self.datasets[container.id] = container

        # 1) Instance-ready deps from _all_dependencies.json
        if container.id not in self._dependency_cache:
            all_deps = self.fetch_dependencies(container.id)
            # The _all_dependencies endpoint is recursive, so we know that for all the "depends_on" datasets of the
            # parent we will already have their direct dependencies. Keep a cache so that we can skip the API call for
            # these child datasets
            self._dependency_cache.extend(container.depends_on)

        # 2) Get processing configs for this dataset (correction, QC, infill) (only needed for RAW datasets)
        if container.processing_level == "raw":
            container.configs = self.fetch_configs_for_dataset(container.id)

        # 3) Recurse into dependencies
        for dep_id in container.all_dependencies():
            if dep_id not in self.datasets:
                dep_container = self.fetch_dataset_by_id(dep_id)
                self._resolve_dataset(dep_container)

    def _build_dag(self) -> dict[str, list[str]]:
        dag = {container_id: container.all_dependencies() for container_id, container in self.datasets.items()}
        # ensure all nodes exist as keys
        for ds_id in list(dag):
            for dep in dag[ds_id]:
                dag.setdefault(dep, [])
        return dag

    @staticmethod
    def topo_sort(dag: dict[str, list[str]]) -> list[str]:
        ordered: list[str] = []
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(_node: str):
            if _node in visited:
                return
            if _node in visiting:
                raise ValueError(f"Cycle detected at {_node}")
            visiting.add(_node)
            for d in dag.get(_node, []):
                visit(d)
            visiting.remove(_node)
            visited.add(_node)
            ordered.append(_node)

        for node in dag:
            visit(node)
        return ordered

    @staticmethod
    def topo_layers(dag: dict[str, list[str]]) -> list[list[str]]:
        """
            Return layers of a DAG where each inner list contains nodes that can be
            processed in parallel (all their dependencies are satisfied by earlier layers).
            dag: {node: [dependencies]}
            """
        # ensure every mentioned node appears in the dict
        all_nodes = set(dag.keys())
        for deps in dag.values():
            all_nodes.update(deps)
        for n in all_nodes:
            dag.setdefault(n, [])

        # indegree is the number of prerequisites (dependencies) for a node
        indegree = {n: len(dag[n]) for n in dag}

        # reverse adjacency: dep -> [nodes that depend on dep]
        succs = defaultdict(list)
        for node, deps in dag.items():
            for d in deps:
                succs[d].append(node)

        # start with nodes that have no dependencies
        q = deque(sorted([n for n, deg in indegree.items() if deg == 0]))
        layers = []

        visited_count = 0
        while q:
            # the current "wave" (parallel batch)
            this_layer = list(q)
            q.clear()
            layers.append(this_layer)

            for n in this_layer:
                visited_count += 1
                for s in succs.get(n, []):
                    indegree[s] -= 1
                    if indegree[s] == 0:
                        q.append(s)

            # keep deterministic order inside the next layer
            q = deque(sorted(q))

        if visited_count != len(all_nodes):
            # There is a cycle or dangling reference
            raise ValueError("Cycle detected or graph not fully connected")

        # Optional: stable sort inside each emitted layer
        for layer in layers:
            layer.sort()

        return layers