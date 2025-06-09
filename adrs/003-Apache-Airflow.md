# 003 Using Apache Airflow for workflow orchestration.

Status: draft

Deciders: Lewis Chambers, Rod Scott, Nathan Shaw, Matthew Fry, Faiza
Samreen, Mike Brown, Dominic Ginger. 

Consulted: Richard Smith, Oliver Swain, Simon Stanley.

Date: 6/26/2024

## Context and Problem Statement

We would like a tool to build workflows using data collected from the
FDRI sensor sites. This could be in the form of ETL pipelines for moving
between data 'levels' or more bespoke analytical pipelines.

The tool should be able to be orchestrated through Terraform. Workflows
should be schedulable or triggered, and product owners (or any other
required users) should be able to add and edit workflows on their own
accord.

Apache Airflow is one (of many) tools that can do this. This was tested
using the managed service provided by AWS
([MWAA](https://aws.amazon.com/managed-workflows-for-apache-airflow/)).

## Decision Drivers

- Build complex workflows that are either scheduled or triggered.

- Orchestrated through Terraform.

- Easy to add/edit workflows.

- As low cost as possible.

## Other considered Options

- Argo Workflow (discussed in ADR 004)

## Decision Outcome

TBD

### Positive Consequences

- AWS provide a managed service
  ([MWAA](https://aws.amazon.com/managed-workflows-for-apache-airflow/))
  and associated [terraform
  module](https://registry.terraform.io/modules/aws-ia/mwaa/aws/latest).
  Infrastructure managed for us (backups, little to no down time) and
  easy to setup environments.

- Workflows defined using python code which most users should be
  familiar with.

- A wide range of
  [operators](https://airflow.apache.org/docs/apache-airflow-providers/operators-and-hooks-ref/index.html)
  to workflows that interact with pretty much anything

- Rich UI for tracking and managing workflows.

- Simple scheduling through python code or the UI.

### Negative Consequences

- Tied into AWS.

<!-- -->

- Harder to integrate with Kubernetes if not using MWAA.

- Looks quite expensive. Currently the largest cost of the month even
  though we only have a small environment and a couple of DAGs. Costs
  [here](https://aws.amazon.com/managed-workflows-for-apache-airflow/pricing/).

![](media/image1.png){width="2.515277777777778in"
height="1.9993055555555554in"}

- There is only one scheduler (regardless of amount of machines and
  nodes) so a potential single point of failure.

Other considerations that have not been fully explored yet:

- [Scaling
  up](https://docs.aws.amazon.com/mwaa/latest/userguide/mwaa-autoscaling.html)
  looks relatively simple but untested.

<!-- -->

- There would be [added
  complexity](https://docs.aws.amazon.com/mwaa/latest/userguide/configuring-networking.html)
  around the Webserver and VPC when setting up a production environment.
  Currently use public access mode but would need to use private access
  mode.
