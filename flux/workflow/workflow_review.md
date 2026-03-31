# Review of the FLUX pipeline

Workflow consists of 3 main steps: Ingestion, processing (eddy pro), post processing. Converting this to a formal workflow is not possible as ingestion is ran as a service and cannot be incorporated into a workflow properly.

This workflow relies heavily on the timeseries processor, and ontop of that the metadata service.  This has 2 main results: how do you run the pipeline without the metadata service?  and can you re-use components of the workflow without creating a new network within timeseries processor and meta-data service.

## CWL files

The workflow is described in a psuedo CWL file.  This is not a true reflection of the workflow as CWL lacks the capabilities to be used in the way needed, and the ingestion tool is a service not a method. Nonetheless it serves as a description of the workflow to an extent.

## Metadata

The question around the metadata service maybe moot, but can we guarentee it will still be up and running 10 years from now? Also, if we make the data from FDRI/flux open and FAIR, how can someone else re-process the data to ensure replicability of our results?  The reliance on the metadata service appears to hamper reproducibility.

The modular nature of the pipeline is then brought into question as well.  To run an analysis you need to use the timeseries processor and the metadata service to run the required ingestion, pre-processing, transformation and processing steps.  These appear to be a little opaque. Even if someone had access to read the metadata service it seems that they would not be able to easily modify the workflow.

## Modualarity

There are methods and functions which appear to have use outside of the timeseries processor. These are ingestion functions for getting data from complex APIs (EA) or S3 buckets, transforming them and putting them in a final location.  These cannot be ran outside of the dri-ingestion module which runs a service.  Ideally, if a service is needed it should call the methods from an external package and wrap with additional code if needed for the services - this would support more reusable DRI.

A similar argument is made for the timeseries processor.  There are pre-processing, clean up and validaation methods, along side full processing methods which cannot be ran outside of the timeseries processor. If these were moved outside of the timeseries processor, and the timeseries processor remained as a workflow occastrator this would better support one DRI and FAIR far better.

## Which runner

CWL is great for a pure workflow, it can be ran on a laptop or cluster.  However we have to fudge certain bits to get it to work the way we need, such as input triggers.  However, the end results is a clear scientific workflow providing full provinance.

ARGO is kubernetes native, and has support for traditional workflow, trigger events, and timed events making it suited to the current FDRI/flux setup. The workflow can then be supplied as YAML files, but these would be separate workflows for the different styles (trigger/timed) in the file, and not a single file.  This may not be an issue.

It maybe that what we need is a combination of the two.  Workflows written in CWL so they can be re-run where ever needed, but ARGO+Calrission as the workflow executor to meet the demands of out workflow: S3 triggers and cron timer based workflows.
