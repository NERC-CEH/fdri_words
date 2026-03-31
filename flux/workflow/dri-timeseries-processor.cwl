#!/usr/bin/env cwl-runner
cwlVersion: v1.2
class: CommandLineTool

label: "DRI Timeseries processor"
doc: |
  
  Run the dri timeseries module with the specified network and look back period.
  https://github.com/NERC-CEH/dri-timeseries-processor
  
baseCommand: [python, -m, dritimeseriesprocessor]

inputs:
  input_trigger:
    type: string
    doc: Dependency trigger from previous step
  
  network_name:
    type: string
    doc: Name of the network to process
    inputBinding:
      prefix: --network
      position: 1

  lookback_period:
    type: string
    doc: Lookback period (e.g., number of days)
    inputBinding:
      prefix: --lookback
      position: 2

outputs:
  result:
    type: string
    outputBinding:
      valueFrom: "processing_complete"
