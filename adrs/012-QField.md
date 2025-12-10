# [Architecture Decision Record (ADR) Identifier]. [short title of solved problem and solution] 

- Status: Draft v.1

## Context and Problem Statement 

Field staff undertaking surveys for FDRI require an app to record in situ measurements/metadata and upload to one place. Currently, Survery123 is being used but has limitations such as licence agreements, user restrictions and survey files are uploaded to sharepoint but metadata is kept in the ESRI environment, so QField is being investigated as an open source alternative. 

## Decision Drivers 
- Open Source 
- Post GIS compatability
- self-hosted QCloud ability
- have metadata and survey files together 

## Considered Options 
- Qfield
- Remain using Survey123

## Decision Outcome 
Chose Qfield over Survey123, because its the option that meets the criterion decision drivers. Resolves the issue of linking to a PostGIS that can be automated.

### Positive Consequences 
Can have multiple users with their own accounts instead of several users using the same account due to restrictions from ESRI. 
Can automate the transition of data stored on the QGIS project to PostGIS database and then an API can be used to retrieve the data for the FDRI catchments.
Qfield is free to use.

### Negative Consequences 
A self-hosted QCloud alternative will need to be set up for security measures, which will take time and resources.
The QField may be less streamlined than Survery123 

### Pros and Cons of the Options 

#### [QField] 

•	Good, because it is open source so data can be exported from the QField/QGIS environment. 
•   Good, because it allows multi-user access with individual accounts.
•   Good, because users in the field can add new locations, upload videos and photos, and make edits to a QGIS project.
•   Good, because there are the same QGIS functionalities available to users e.g. users can run expressions in the field calculator 
•   Good, because in-built GPS geotagging of attachments and possible to set up a GSS bluetooth connection with Android. 

- Bad, because it will need a QFieldCloud equivalent set up to host the data synced from the field or a manual transfer of files. 
- Bad, because it will require the field team to learn a new app and set up new forms, having already done so for Survey123, taking up time and resources. 

#### [Keep using Survey123] 

- Good, because it is already being used and currently works for the field team.
- Good, because it has XLS form support and the app is more user-friendly.
- Good, because a self-hosted cloud system is not required. 

- Bad, because metadata is currently uploaded separatley to the survey files.
- Bad, because is it an ESRI licenesed product and locks data into the ESRI ecosystem by storing it in ArcGIS Online.
- Bad, because it is more difficult to get data into a PostGIS database.

## Links 

- Method for linking a PostGIS database to QField and QGIS for better centralisation of data and automation of the pipeline.

(Access AWS RDS) PostgreSQL database in AWS then enable PostGIS - already set up
•	Make this database reachable over the internet and secue it (VPC rules, SSL, firewall, passwords and users)
•	Make a QGIS project with layers and add the connection to PostGIS.
•	Load tables and prepare forms in the QGIS project to use postGIS layers
•   Use QfieldSync to package project. Manual transfer to phone via USB, shared drive.
•   Make edits in the field
•   Manual transfer to phone via USB, shared drive and use QFieldSync to sync from device.

•	Migrating to AWS EC2 + RDS
•	Exposing it to field users

-	Provides real-time syncing 
-	No QFieldCloud subscription 
-	Fully self-hosted and private
-   Offline capablibility 

-   Requires manual transfer.

