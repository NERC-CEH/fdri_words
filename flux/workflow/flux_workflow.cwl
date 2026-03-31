# flux_workflow.cwl
cwlVersion: v1.2
class: Workflow

# Almost a static workflow, but lets leave it more open where we can
inputs:
  ingestion_name:
    type: string
    doc: "Name of the network for which to run the ingestion service for.  FLUX or
    FDRI for example."
    default: "flux"

  network_name:
    type: string
    doc: "Name of the network to process, such as cosmos or flux"
    default: "flux"

  lookback_period:
    type: string
    doc: Lookback period (e.g., number of days)
    default: "P2D"

    
# They must point to a specific step's output using 'outputSource'.
outputs:
  results:
    type: string
    doc: "Output as one is required"
    outputSource: post_processing/result


# Workflow steps

steps:
  data_ingestion:
    run: data_ingestion.cwl
    in:
      ingestion_name: ingestion_name
    out:
      - result

  eddy_pro_processing:
    run: dri_timeseries_processor.cwl
    in:
      input_trigger: data_ingestion/result
      network_name: network_name
      lookback_period: lookback_period
    out:
      - result

  post_processing:
    run: post_processor.cwl
    in:
      input_trigger: eddy_pro_processing/result
    out:
      - result

