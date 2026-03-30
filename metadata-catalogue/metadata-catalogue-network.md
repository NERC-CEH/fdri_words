# Metadata Catalogue Network View

High-level view of the metadata catalogue Kubernetes cluster.

![Metadata Catalogue Network View](Catalogue-network-view.drawio.svg)

## Overview

Namespaces are shown as the blue outlined boxes.

catalogue.ceh.ac.uk and vocabs.ceh.ac.uk shown in orange, are still on the old infrastructure.

Consolidating the different domain names under a single domain is a planned future improvement.
This would likely be done by replacing the ingress controller with a Gateway API implementation.

Data storage is not shown, but the underlying SAN is mounted as a persistent volume 
multiple times to give common access to storage.

## Each namespace
### eidc

sparql.ceh.ac.uk is a Fuseki instance containing triples describing the public metadata records.
Triples are generated from the catalogue and loaded into Fuseki on a schedule.

`dri-ui` displays the spatial and file preview explorers.

The `proxy` manages authentication for user access to the catalogue.
The catalogue is made up of the `catalogue` Java application and `solr` as the main
components. `datastore` provides direct access to the datasets. `mapserver` provides
access to the spatial data, i.e. web map services.

### automated-racs

Automated resource acceptance checks (RACS), used by the data centre staff to check 
that dataset files are correctly formatted.

### data-package

A Java application that packages datasets into a zip file with the metadata and licence
information.

### hubbub

Maintains the integrity of the dataset files by checking that the file hashes match.
API provides file-level information about each dataset, used, for example, by the
file preview explorer in the catalogue `dri-ui` or to generate Croissant formatted
metadata records.

### order-manager

Subset spatial datasets ordered by users. Has a Java application for the API and a
React application for the frontend. The API interacts with FME to do the spatial
transformation. FME will be replaced soon as the licence is too expensive.

### vocabs

Skosmos instance as frontend for the vocabularies. Vocabularies are loaded from the
Fuseki instance.

Proxy used to protect draft vocabularies from public access.