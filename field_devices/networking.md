# Networks and services

## Low-bandwidth data via MQTT

Datalogger sends observations to an "MQTT broker". Data is _published_ to a topic (which is structured like a web URL) and other services can _subscribe_ to that topic and read the messages.

In FDRI the MQTT broker is provided by Amazon Web Services IoT Core. When the data is received, the raw messages are stored in s3 storage in AWS.

We use authentication certificates (preferred) for devices which support them, this includes Campbell dataloggers.

There's also a route for devices which can't or won't do certificate-based authentication to use a username and password to connect to an MQTT broker.

### Implications for FDRI Infrastructure

Each field device needs the address of the MQTT broker in an AWS account. Please see the [campbell-mqtt-control](https://github.com/NERC-CEH/campbell-mqtt-control/) project for detail of remotely configuring settings on a Campbell datalogger via MQTT.

![diagram of data flowing from logger to s3](assets/mqtt.png)

## High-bandwidth data via direct download

MQTT is designed for "Internet of Things" services and not for high-bandwidth data at large volumes. 

In FDRI we have set up a VPN to provide direct access to automate downloading data from field devices and storing it directly in s3. The [Architectural Decision Record](https://github.com/NERC-CEH/fdri_words/blob/b7b511a210a5eac5a112d2f157767ad9b4456828/017-Flux-Raw-Data-Transfer-Method.md) provides some background to why it's done this way, and what else was tried.
 
### Implications for FDRI Infrastructure

The server which runs the scheduled pipeline to collect data from field devices needs credentials to write to s3 in the correct AWS account (access keys, role to assume, and bucket name). Please see the [fdri_field_access](https://github.com/NERC-CEH/fdri_field_access) project for detail of how this is set up.

![diagram of data collected from logger sent to s3](assets/openvpn.png)
 
