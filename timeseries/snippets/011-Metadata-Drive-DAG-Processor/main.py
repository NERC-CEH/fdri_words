from dag import DagBuilder
from pipeline import PipelineExecutor

import time


if __name__ == "__main__":
    start = time.time()

    builder = DagBuilder()
    dag = builder.build_from_target(
        sites=["BUNNY"], resolution="PT30M", variables=["RN"]
    )

    end = time.time()
    print("DAG built took {} seconds".format(end - start))

    print("\n=== DAG ===")
    for node, deps in dag.items():
        print(f"{node} -> {[d for d in deps]}")

    print("\n=== Topological order ===")
    order = builder.topo_sort(dag)
    for n in order:
        print(" ", n)

    print("\n=== Topological layer order ===")
    layers = DagBuilder.topo_layers(dag)
    for i, level in enumerate(layers):
        print(f"\n=== Layer {i} ===")
        for node in level:
            print(f"  {node}")

    print("\n=== Example pipeline execution ===")
    executor = PipelineExecutor(dag, builder.datasets)
    executor.run()
