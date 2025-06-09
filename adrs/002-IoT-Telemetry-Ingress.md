# 002. Choice of mechanism for IoT telemetry ingress.

Status: Proposal

Deciders: Lewis Chambers, Matthew Fry, Faiza Samreen, Mike Brown,
Dominic Ginger.

Consulted: Richard Smith, Oliver Swain, Simon Stanley.

Date: 2024-06-24

## Context and Problem Statement

We need a mechanism through which IoT telemetry data can ingress into
the cloud system i.e. data from FDRI sensor sites.

The adopted mechanism should be low cost to run, have minimal
maintenance, and be simple to migrate onto another cloud provider or
on-premises solution.

## Decision Drivers

- Low running cost

- Simple post-implementation maintenance

- Easily migratable to another cloud provider

## Considered Options

- AWS IoT Core

- Mosquito + Kubernetes

- AWS MSK (Managed Kafka)

- AWS MQ (Managed message queuing. RabbitMQ, Apache ActiveMQ)

## Decision Outcome

Chosen option: \"AWS IoT Core" because it is independent of machine
instances, is effectively maintenance free, and significantly lower cost
compared to other options. It best meets our current expected workflow
of semi-batched processing.

### Positive Consequences

- Low to zero maintenance

- Handles device security / authentication

- Gives remote control over devices (but unlikely to be used for
  dataloggers)

- Can handle millions of devices, billions of messages

- Allows logical device types and grouping for easier organization

- No machine costs. It is effectively a free message broker and rules
  engine (pay-as-you-go message costs). [Cost
  Comparison.](https://cehacuk.sharepoint.com/:x:/r/sites/FDRI-WP2Digital/_layouts/15/Doc.aspx?sourcedoc=%7B97CAFE1F-632B-4C9C-8021-2A64F93D12CF%7D&file=20230829_AWS_cost_estimates_v1%20(2).xlsx&action=default&mobileredirect=true)

- Messaging costs can be reduced to zero by skipping direct to the rules
  engine. (The message broker is only useful for cross-device messaging,
  which we don't need)

- Can write messages directly to S3, SQS, SNS, Lambda, databases, etc.

### Negative Consequences

- Vendor locked to AWS

- Google Cloud have discontinued their IoT services \[1\] (AWS has no
  plans right now). Azure warned customers that IoT Central will be
  closed but claimed it was an accident \[2\]. The risk of future
  migration is more challenging than moving standard infrastructure.

## Pros and Cons of the Options

### Mosquito + Kubernetes

[Eclipse Mosquito](https://mosquitto.org/) running on [Kubernetes
(k8s)](https://kubernetes.io/)

- Good, Mosquito & k8s are open source with healthy communities

- Good, deployment on k8s is platform agnostic. It can run on-premises
  or any cloud provider with minimal effort in migration.

- Bad, self-management of servers = needing people to maintain them /
  take actions during downtime.

- Bad, self-management of servers = data is lost during downtime with no
  recovery options.

### AWS MSK

[Amazon Managed Streaming for Apache Kafka](https://aws.amazon.com/msk/)

- Good, because Kafka is a common open-source tool and is easily
  migratable

- Good, because it can connect to existing data sources

- Good, because it can stream messages with multiple sources and
  subscribers

- Bad, because we only need one listener, the backend.

- Bad, because we only need to ingress messages, not stream them in real
  time

- Bad, because of the costs of machine instances to run it

- Bad, because it can't send data to storage directly. Requires Lambda
  or Kinesis Firehose

- Bad, doesn't support MQTT out of the box. Requires a custom MSK
  connector or IoT Core.

### AWS MQ

[AWS Managed Message Broker](https://aws.amazon.com/amazon-mq/)

- Good, because it is a simple message broker for consuming messages
  into the cloud,

- Good, because it is maintenance free

- Good, because it is easily migratable

- Bad, because it has instance costs. IoT core has the same capabilites
  at significantly lower cost

- Bad, because it can't send data to storage directly. Requires Lambda
  or Event Bridge + Kinesis Firehose

## Links

- \[1\] [Google Cloud close down IoT Core service in
  2023](https://techcrunch.com/2022/08/17/google-cloud-will-shutter-its-iot-core-service-next-year/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAGy1h7OrwjhN96XwzMosq1pYcnyt4zT9XxiJeO6Ebb1svh0ge_PKMfpZ3dZb5XP5dlJs9P_ZS1JPPlubSd1V1qOvOPsgte5baiul9ZPz8kPdOO1mfQm7NWZn-eCZr2yg90PbzIL7S51dEfGWiSRfm_W3_2ztcGLOW00SQFVkb4qm)

- \[2\] [Microsoft accidentally warn about IoT Central
  closing](https://www.techzine.eu/news/infrastructure/116658/is-microsoft-killing-off-azure-iot-central/)
