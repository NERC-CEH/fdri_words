# Initial overview of the technology

A desirable capability for the Campbell loggers in the capability to remotely perform actions on them and not be dependent on proprietary software or need to send out field engineers. This includes:

* Firmware updates
* Logger program updates
* Certificate rotation

These should ideally be possible with automated deployment and the capacity to selectively roll out updates across different logger models and roll back broken updates.

Control in Campbell loggers is provided by [sending MQTT messages with a specified JSON payload](https://help.campbellsci.com/CR300/Content/shared/Communication/mqtt/mqtt-command-control.htm)

## The Campbell Side

Making changes to firmware or CRBasic programs is fairly simple with each requiring a payload containing the download URL.

## Firmware Download

```
Topic: <groupID>/cc/<deviceID>/OS 

{
“url” : “https://example.123.xyz”
}
Program Download

Topic: <groupID>/cc/<deviceID>/program

{
“url” : ”https://example.123.xyz”,
“filename”:”MyProg.crb”
}
```

## Certificate Rotation

There is no inbuilt command for rotating certificates, but there all file manipulation commands allowing you to:

* List files
* Delete a file
* Download a file from the cloud
* Upload file to cloud (via presigned S3 URL)

It isn't clear right now whether certificate rotation is possible

## The AWS Side

AWS IoTCore has many built in features for managing IoT devices remotely that might work on Campbell loggers (but needs to be tested).

## Remote Actions
### Commands

The command feature is allows you to define a MQTT payload command to a given device and topic. It is intended for single one-off commands to a single device which may or may not be registered with IoT Core. The feature is not intended for regular actions across a fleet of devices, but should be very useful for testing purposes.

#### Secure Tunnels

Tunnels can be used to securely connect to devices behind firewalls for debugging/testing/maintenance and function by creating a pair of Client Access Tokens (CAT) to facilitate security. This feature is a little expensive at $1/tunnel as each tunnel closes after 12 hours.

#### Jobs / Job Templates

The jobs feature is designed for repetitive tasks that run regularly or run on a large number of devices, usually firmware/program updates. Jobs can be converted into templates to run parametrically on a fleet of devices.

The implementation details of jobs are not currently clear. It isn't known if it can send MQTT commands to the logger, but heavily advertises itself as being useful for software/firmware updates

#### Software Package Catalog

[IoT Core recently released their package catalog](https://docs.aws.amazon.com/iot/latest/developerguide/software-package-catalog.html) which allows you to upload a collection of files that form a software package (Can also include firmware) that can then by deployed using the jobs .  This allows each "thing" to have a software package and version associated with it and changes as required. With fleet indexing enabled, this also allows IoT Core to sort devices by their software version.