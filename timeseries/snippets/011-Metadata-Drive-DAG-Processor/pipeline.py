from dag import DagBuilder
from domain_models.time_series_container import TimeSeriesContainer


class PipelineExecutor:
    def __init__(self, dag: dict[str, list[str]], containers: dict[str, TimeSeriesContainer]):
        self.dag = dag
        self.containers = containers
        self.completed: set[str] = set()

    def run(self):
        ordered = DagBuilder.topo_sort(self.dag)
        for dataset_id in ordered:
            try:
                container = self.containers[dataset_id]
            except:
                container = TimeSeriesContainer(id="error handling", ref_id="error!")
                self.containers[dataset_id] = container
                # TODO THIS try except block is just a work around as problem with dataset ID http://fdri.ceh.ac.uk/id/dataset/cosmos-bunnyprecip_diag_30min_raw (note lack of hyphen)

            print(f"\n Processing {dataset_id}")

            if container.load():
                container.data = self._load_raw(container)
            else:
                deps = [self.containers[d].data for d in container.all_dependencies()]
                container.data = self._process(container, deps)

            self.completed.add(dataset_id)
        print("\n DAG complete")

    def _load_raw(self, container: TimeSeriesContainer):
        # pseudo: load from S3/parquet
        print(f"  Loading raw data for {container.source_column}")
        #return load_from_s3(container.source_bucket, container.source_dataset)

    def _process(self, container: TimeSeriesContainer, deps):
        # apply corrections, QC, infill, etc
        print(f"  Running {container.method_type.upper()} ({container.method})")
        # df = combine_inputs(deps)
        # for cfg in container.configs:
        #     df = apply_processing_step(df, cfg)
        # return df