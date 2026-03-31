#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool

label: DRI ingestion module
doc: |
  Pseudo module as actual ingestion service runs as a service listening out for
  SQS messages and moving and converting data as it comes in.
  Code is here: https://github.com/NERC-CEH/dri-ingestion

baseCommand: [python, -m, post_processor_module] # Add your actual module name here

# We use the input_trigger to force execution order as CWL looks out for files
# being created and passed between workflow steps.

inputs:
  input_trigger:
    type: string

outputs:
  result:
    type: string
    outputBinding:
      valueFrom: "post_processing_complete"
