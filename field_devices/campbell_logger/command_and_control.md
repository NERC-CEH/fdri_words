## Campbell Command and Control via MQTT

For FDRI and other aligned fielf observation sites we needed a solution that supports as many as possible of:

* Firmware updates
* Script updates (Sensor changes at sites may require a script update)
* Configuration updates. e.g. Site ID, MQTT topic, max payload size, etc: Valid settings 
* File updates (For rotating root CA from AWS)
* Certificate rotation
* Data retrieval
* Device / script reboot

The models of Campbell loggers we are using support an MQTT command interface that meets almost all of these needs (apart, as far as we know, from certificate rotation)

* [campbell-mqtt-control](https://github.com/NERC-CEH/campbell-mqtt-control/) - open source library for controlling Campbell dataloggers via MQTT

* [API documentation and HOWTOs](https://nerc-ceh.github.io/campbell-mqtt-control/) for the Campbell C&C MQTT library

* [Internal documentation about setup to use AWS IoT core as a backend]()
