# 004. Argo Workflows \<Work in progress\>

Status: draft

Author: Dominic Ginger

Deciders: Faiza Samreen, Mike Brown, Richard Smith, Simon Stanley, Oli
Swan

Consulted: Rest of FDRI Dev team, IT, other stakeholders/users

Date: 2024-06-28

## Context and Problem Statement

We want a workflow management system to orchestrate our processing of
FDRI data. Argo workflow was investigated because of its flexible
nature, its use by Epimorphics in their work for the environmental
agency.

Argo workflows \[0\] is a Kubernetes-native workflow engine that sits as
a thin layer on top of a Kubernetes cluster implemented at Custom
Resource Definitions (CRDs). It schedules workflows that can be steps or
Directed Acyclic Graphs (DAGs) where each node in the graph is a
Kubernetes pod.

##  Decision Drivers

- Cost

- Expertise

## Considered Options

- Apache Airflow, See ADR 003

## Decision Outcome

undecided

### Positive

- Cost, running Argo Workflows on an existing Kubernetes cluster is very
  cheap, requiring only 2 pods. Including Argo Events\[1\] adds another
  default 4 pods (3 event bus, 1 Argo events controller) and one for
  each event source and even sensor.

- Expertise -- We have good Kubernetes expertise with the developer
  team, IT also have good developer expertise. We also have the option
  to hire Epimorphics as consultants who have very good expertise with
  Argo and Kubernetes.

- 

### Negative

- Cost, requires a Kubernetes cluster which can be an expensive overhead
  if we don't already have one

- \...

## Links

- \[0\] <https://argoproj.github.io/workflows/>

- \[1\] <https://argoproj.github.io/events/>

- 
