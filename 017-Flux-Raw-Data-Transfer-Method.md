# Architecture Decision Record (ADR) Identifier] 
## Raw flux data transfer mechanism

Status: **draft**

We need to get raw 20Hz flux data to the platform, initially because we thought researchers would be interested in it, but now because the processing pipeline will use it. What's the most painless way and cheap way of doing this - while still installing equipment?

## Decision Drivers
* Size of the raw data files
* Capability of the Datalogger

### Considered Options

#### Transferring data from the datalogger using MQTT
We asked Campbell to send all the data via MQTT, but they did not and argued against it. I don't believe there's a protocol-based reason why it shouldn't work (I've worked with MQTT sending sub-second data in the past with a larger number of variables). However, there is an issue with their implementation of MQTT where it's not able to send datatables above a certain size. I could imagine, depending on how they've engineered their firmware, they may have an issue with caching when offline with MQTT and the 20Hz data. 

#### Transferring data from the datalogger using SFTP
We tried a few different options to send data using SFTP. Neither option appeared to be reliable. The way Campbell scripts operate doesn't allow asynchronous transfers while the datalogger is busy collecting data. So you have to make a choice between collecting data from sensors and transferring data to the platform. The other option streaming the FTP data, didn't allow historic data to be resent - so comms or power issues would result in a gap. Neither options appeared to reliably upload files - regardless of the size of them.

Performing the transfer from the script wasn't particularly fast - transferring a few MB also took a few minutes. However, the datalogger is able to run a webserver and FTP, and transferring data appears to have faster throughput - and transfer operations don't stop the script from running. Unfortunately, there's no automated send file option in the configuration.  

Tom mentioned these issues to Campbell, who provided a provided a script that also sent data via FTP - and it also had the same issues. It doesn't appear possible to do it reliably, using 20 Hz data recorded over 30 minutes.

#### Transferring data from the datalogger using other equipment in the compound (Cameras / Gateway)
Some gateways (such as the LoRaWAN enabled Robustel LG5100 gateway) support running scripts on them - which could facilitate the transfer of files from the datalogger to the platform. However, the power consumption is larger for this gateway compared with the gateway we intend to use at Tring grange farm.

We intend our cameras to be switched off some of the time, to conserve power, potentially preventing them from being used for this service - they also may not be reliable enough.

#### Make data available via public IP
Other networks use SIM cards with publically addressible static IP addresses, there's increased SIM costs to this and puts the gateway in a position that's exposed to external traffic. Other monitoring networks have experienced gateways that have been comprised and also have significantly higher traffic.

#### Make data available via VPN
The remaining option from the datalogger perspective is to make it available to data requests from another machine. The datalogger provides multiple interfaces to pull data from it. The VPN can be switched on and off, which could save power and data bandwidth (openVPN has data overheads). VPN stops systems from being exposed to external threats.

1. Loggernet - but I've heard of issues (such as the software crashing if indexes wrap and crashing in other scenarios) and this ties us into proprietary software.
1. FTP - It's there and tested. Server doesn't provide resume functionality however.
1. HTTP - It's there and tested, but might be more work to automate file retrieval.

## Decision Outcome
Chosen option: "Make data available via VPN", because it's the only option that WP1 hasn't tried, but requires some additional work from WP2.

### Positive Consequences
* Reduces in-field equipment complexity
* Provides the most flexibility with direct connection to equipment
* Doesn't require WP1 and WP2 to work lock-step on the equipment

#### Negative Consequences
* Requires work from WP2 to enable - and a machine connected to the VPN to operate the mechanism
* VPN requires more datausage; using more bandwidth and power
