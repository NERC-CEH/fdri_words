# FDRI Raspberry Pi deployment - overview

## Software

### FDRI Raspberry Pi Camera repository

This repository includes a python package for capturing images at a set interval during daylight hours, a template for site-specific configuration values, and scripts to update the operating system and set up the camera package as a systemd service.

## Infrastructure

Please see the [internal documentation](https://github.com/NERC-CEH/fdri_words_private) for detail about the cloud storage for cameras.

## Authentication

Currently this is done with access keys issued to an IAM user with very restricted privileges. It's sustainable for testing and for the first trial site, but needs improvement.

There's a method for providing access to other AWS services via the certificate authentication available in AWS IoT Core.

### Drawbacks of the key-based method

* The max limit is 2 keys, with one for development, which would provide write access to an s3 bucket if the bucket name is also known
* At present all the devices share a single key, which causes a maintenance headache if it needs to be revoked after accidental leakage

### Considerations for the certificate-based method

* Complex permissions flow which needs AWS expertise and careful configuration
* New work on dri-infrastructure to manage Raspberry Pis as Things and provision them with certificates (there's a method for doing this for Campbell dataloggers with manual steps) 
* Potential advantages in being able to send and receive MQTT status messages from the Pis, which is on the Wishlist 

## Certificate auth flow

Please see [this Github issue](https://github.com/NERC-CEH/FDRI_RaspberryPi_Scripts/issues/28) on alternate authentication methods.

The [AWS Reference documentation](https://docs.aws.amazon.com/iot/latest/developerguide/authorizing-direct-aws.html) has a long description which boils down to this:

* Create an IoT core "Role alias" for pi cameras
* Create a Policy giving the alias iot:AssumeRoleWithCertificate access to the s3 uploader role
* Create a Things Group and assign it the policy
* Create a Thing and assign it to the Things Group, and issue it a certificate
* Create a Policy allowing the s3 uploader role to offer the IoT credentials provider sts:AssumeRole access

We've tried (manually) configuring this up to the last step, which threw errors - see notes in the Github issue.

There's some sample code in an auth-flow-experimental branch in the repository, in a scratch directory, for proof of concept upload to s3 via certificates issued to IoT Core Things,

The auth flow needs the IoT credential provider endpoint, which is different from the main IoT MQTT endpoint; it's discoverable via the AWS CLI / CloudShell like this:

```
aws iot describe-endpoint --endpoint-type iot:CredentialProvider
```

## Field setup

@JacHam12 maintains the code, with advice and support from RSEs. 

Please see the [internal documentation](https://github.com/NERC-CEH/fdri_words_private) for links to the setup process that the field engineers are using for this project.

## Suggestions box

The Github issue list for the FDRI Raspberry Pi Scripts includes some nice-to-have features for after the initial trial deployment. Here's an extended version. Feel invited to add to it:

* Remote access to the Pi via VPN running on the on-site modem
* MQTT client running on the Pi - send status updates and optionally receive update messages
* Ability to remotely update the application running on the Pi (either its configuration values, like the interval it takes pictures at, or any onboard analytical code)
* Central repository storing the deployed configuration values for all the Pi Cameras - [outline of that here](https://github.com/NERC-CEH/fdri_assets)  
* Face detection and blurring - this is a need from WP1 (to avoid storing or publishing images with personally identifying information). TBD create issue based on PR comments
* Option to add more sensor types (there is provision for this in the housing)