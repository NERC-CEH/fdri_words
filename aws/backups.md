Some notes on our experiences trying to back up data m1 data in s3. We tried a couple of different options. Worth noting that all backups (for s3 and other resources) will likely be managed from a central account in the future.

# AWS Backup

Some notes on using [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html) for s3. We created a [backup plan](https://github.com/NERC-CEH/dri-infrastructure/pull/190) for hourly backups, using [periodic (snapshot)](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html#compare-s3-backup-types) backups rather than continuous because of the small rentention time for continuous backups, and the fact that the bucket contents change every minute.

## Requirement for s3 backups
* The bucket must have versioning
* The bucket must have ACL enabled
* s3 backups must be [opted-in](https://eu-west-2.console.aws.amazon.com/backup/home?region=eu-west-2#/settings)
* Several permissions required
    - AWSBackupServiceRolePolicyForS3Backup
    - AWSBackupServiceRolePolicyForS3Restore
    - AWSBackupServiceRolePolicyForBackup

For the latter, this covers permissions for all resources so could be filtered for just those you want to backup.

## Some good to knows
* Terraform doesnt support indexing the backups yet (see [issue](https://github.com/hashicorp/terraform-provider-aws/issues/40672)).
* You cant use wildcards when specifying resources in the backup selection plan. It will only accept the base s3 bucket ARN. If you want to only backup certain keys then these need to be tagged with the tag then included in the selection plan. See [example](https://registry.terraform.io/modules/lgallard/backup/aws/latest/examples/selection_by_tags)
* You cant restore from one account into another, but you can copy the restore into the desired account

## Issues
* Backups were failing for cosmos (probably due to permissions). Because of the volume of objects (~30,000,000) and the fact it was trying to backup up all of them every hour (because they kept failing) the costs started soaring. We could have tagged the cosmos data to remove from the backup plan, but this would have cost a good chunk of money. Hence, we switched off the backup plan and looked for other options.

# s3 replication

[s3 replication](https://aws.amazon.com/s3/features/replication/) allows you to replicate objects in your bucket via a [replication config](https://github.com/NERC-CEH/dri-infrastructure/pull/203). Rules can be set to replicate only certain objects. These rules are run on all new objects in the bucket. For our purposes we only want to replicate objects under the `fdri/fdri_sensors` and `nrfa` prefixes. With this in place, costs went up by around 5% from ~ $2 to ~$2.10.

To replicate existing objects, you need to run a [batch replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-batch-replication-batch.html) job. The job requires a manifest that you can either provide or AWS can build for you. We had AWS build one for us to replicate all objects that had a replication status as `NONE` (i.e. they have never been replicated by the rules mentioned above). This cost ~ $50 for around 1.7 million objects.
