#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool

label: DRI ingestion module
doc: |
  Pseudo module as actual ingestion service runs as a service listening out for
  SQS messages and moving and converting data as it comes in.
  Code is here: https://github.com/NERC-CEH/dri-ingestion

baseCommand: [python, -m, ingestion]

inputs:
  ingestion_name:
    type: string
    inputBinding:
      position: 1
    doc: Name of the ingestion type to run such as cosmos or flux

outputs:
  result:
    type: string
    outputBinding:
      valueFrom: "ingestion_complete"
