# 006. Applying Hash of Raw MQTT Messages

Status: proposed

Authors: Lewis Chambers

Deciders: Lewis Chambers, Dominic Ginger

Consulted: FDRI Dev Team

Date: 2024-07-04

## Context and Problem Statement

IoT Core supports two MQTT QoS (Quality of Service) flags:

- At least once: Delivers 1+ of each message

- At most once: Delivers 0 -- 1 of each message

Because we don't want any data loss, we will use the "At least once"
option, meaning that duplicate messages are expected. A convenient
method to check for duplicates is to add a hash of the message, this
gives a unique (and short) representation of the message which can be
used for finding duplicate messages. The question then is:

How should the hash be made accessible to the process that deduplicates
messages without compromising searchability of messages?

## Decision Drivers

- Maintain searchability of messages

- Ease of access to hashes -\> machine and human readable

## Considered Options

- Combined filename: "\<timestamp\>-\<hash\>"

- Hashing folder mirroring message file path, but stores hash instead.

- Lambda function to add metadata to message S3 object.

## Decision Outcome

Chosen option: \"Combined Filename\", because it provides the simplest
solution to the problem with no additional compute, and no extra files
created. Because each file starts with a timestamp, it is also
convenient to sort the files by date-time and the duplicates are
logically close to each other, giving better visibility of duplicates
when visually inspected.

### Positive Consequences

- IoT Core can generate a hash of the message at no extra cost

- Better visibility of hashes -\> hashes are relatively close to each
  other

- Files remain searchable and sortable

- No I/O processes to check hashes (faster than reading files)

### Negative Consequences

- Deduplication needs to split the filename to check the hash,

- It would be cleaner to have hashes in the metadata.

## Pros and Cons of the Options

### Hashes stored in mirrored directory tree

This option creates a sibling directory tree that matches the iot
message tree exactly:

![](/media/image.png){width="2.0421773840769903in"
height="2.0941601049868765in"}

- Good, because no filename splitting is needed

- Good, because finding the hash is simple, just replace the parent path

- Bad, because the number of files is doubled

- Bad, because directory trees may drift over time and the hashes get
  lost or expire

- Bad, because it reduces human readability of hashes

- Bad, because it requires I/O operations to read hashes

### Add Metadata with Lambda

[AWS Lambda Serverless Compute](https://aws.amazon.com/lambda/)

- Good, because adding hash to metadata is clean and doesn't impact the
  filename

- Good, because machine access to hash is simple

- Bad, because more services used, and costs are increased

- Bad, because it reduces human visibility of duplicate hashes

## Links

- [AWS Lambda Serverless Compute](https://aws.amazon.com/lambda/)
