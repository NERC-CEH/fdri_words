# Campbell Cloud Id to site id/station name mapping

Each campbell logger sends us data to a prefix that includes the unique campbell cloud id. We don't use this id anywhere but it can help with debugging to know which cloud id maps to which station_name in the messages. The station_name from the raw data is what we use to write to the ingested bucket site_id (SITE=<station_name>) in the s3 prefix.
Sometimes the station_id gets changed, most likely while the device is being setup, so this isn't an absolute list of the mappings, it's just the most recent mapping taken on 02.06.2026.


```
DIRECTORY            LATEST_FILE_TIME           STATION_NAME
---------            ----------------           ------------
23B9-FKUR-TW4G       2026-06-02T15:04:45Z       70683
4DX4-45BN-U333       2026-05-08T10:30:00Z       CH_TRIGR_EC
6HUK-36Y7-A6G5       2026-06-02T15:32:03Z       -
7ERZ-EEAE-23ZK       2026-06-02T15:05:14Z       SE-FOFAD-01-PR
C2N5-N2P6-HH4Z       2025-12-03T17:47:27Z       CH-PEDMF-01
CBUW-UPZZ-FK7J       2026-06-02T15:34:00Z       CH-TRIGR-01
DV8B-ZR6T-23JB       2026-05-19T12:57:31Z       CH-LOWPA-01
HZEZ-6T2T-5G3Z       2026-06-02T15:05:03Z       CH-CHOPS-01-RG
J3EA-8YB6-QFV9       2026-06-02T15:05:03Z       -
JVVR-H4CU-RBBW       2026-05-15T14:42:03Z       23825
K3CN-QJ9X-6HQ8       2026-06-02T15:05:02Z       FDRI_Severn_Trap
NF55-NQ6X-7HLZ       2026-05-26T07:55:31Z       FDRI_Mobile_Station
NR6X-KEFT-A2D5       2026-06-02T15:05:00Z       CH_MILFA_01
QSF5-STKX-4YVB       2025-05-12T12:04:04Z       FDRI_Test_site
QU8Q-9JTY-HVP8       2026-06-02T15:05:03Z       Generic-Precipitation-1
SQQE-X6SS-WG2G       2026-06-02T15:33:03Z       -
T8NK-LP3S-9CTF       2026-06-02T15:05:30Z       CH-SCOBR-01
TX6A-Y96Q-NH63       2026-03-29T19:41:06Z       Test_1
XMUU-Y6KX-MMTF       2026-06-02T15:00:00Z       CH_MILFA_EC_01
cr1000x              2026-05-20T15:27:20Z       22505
```
