# 005. Raw IoT Message Directory Structure

Status: proposed

Authors: Lewis Chambers

Deciders: Lewis Chambers

Consulted: FDRI Dev Team

Date: 2024-07-04

## Context and Problem Statement

Currently the first step of the time series telemetry pipeline is to
dump raw telemetry messages into an S3 bucket on AWS with no validation
processing. The question then is: how should the messages be named and
structured to maintain efficient indexing, searchability?

## Decision Drivers

- It must be searchable / human readable

- Must maintain fast read times

## Considered Options

- Site ID first
  "fdri/cosmos_swarm/\<site_id\>/\<data_source\>/\<filename\>"

- Data table first
  "fdri/cosmos_swarm/\<data_source\>/\<site_id\>/\<filename\>"

## Decision Outcome

Chosen option: "Site ID first\", because it most closely reflects [best
practices](https://docs.aws.amazon.com/whitepapers/latest/designing-mqtt-topics-aws-iot-core/mqtt-design-best-practices.html)
for the design of MQTT topics where the path flows from left to right
and progresses from general to specific. Also, it is possible that in
future developments of the FDRI project, the sites will split data into
smaller topics for each type of sensor rather than sending 100+
variables as a single chunk. It is common for MQTT topics to be broken
down to the sensor level at the cost of more messages sent, but greatly
simplifying data validation; for example:

- fdri/cosmos_swarm/\<site\>/precipitation/tipping001/\<filename\>

- fdri/cosmos_swarm/\<site\>/precipitation/tipping002/\<filename\>

- fdri/cosmos_swarm/\<site\>/precipitation/raine/\<filename\>

- fdri/cosmos_swarm/\<site\>/temperature/sensor001/\<filename\>

If this change was required, the existing message structure would not
need to be changed as it would simply make subdirectories inside the
existing structure. This example increases the number of messages by 4x,
but IoT Core is sufficiently cost effective that the impact is not
significant.

### Positive Consequences

- Reflects common practices for MQTT topics

- Matching the MQTT topic that created the file makes it simple to
  locate the message.

- Enables future splitting up of sensors at sites

### Negative Consequences

- Slightly more complicated to collate all messages from a given data
  source (although, if we were to split messages down to the sensor
  level, it would require hundreds of directories at the base level for
  each type of sensor and configuration, which doesn't make much sense)

## Pros and Cons of the Options

### Data Table First

- Good, because it structures data according to data source (single
  sensor or a group). Simpler indexing

- Bad, because there may be hundreds of sensor types and configuration
  in the future

- Bad, because it's more difficult to match the MQTT topic with where
  the data is stored

## Links

[MQTT topic best practices white paper
(AWS)](https://docs.aws.amazon.com/whitepapers/latest/designing-mqtt-topics-aws-iot-core/mqtt-design-best-practices.html)
