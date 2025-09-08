# AWS Backup

Some notes on using [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html) for s3. We currently [backup the m1 bucket](https://github.com/NERC-CEH/dri-infrastructure/blob/main/staging/modules/backups/main.tf) hourly, but all backups (for s3 and other resources) will likely be managed from a central account in the future.

Using [periodic (snapshot)](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html#compare-s3-backup-types) backups rather than continuous because of the small rentention time for continuous backups, and the fact that the bucket contents change every minute.

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
* Terraform doesnt support indexing the backups yet (see [issue](https://github.com/hashicorp/terraform-provider-aws/issues/40672)). Currently switched on via the console.
* You cant use wildcards when specifying resources in the backup selection plan. It will only accept the base s3 bucket ARN. If you want to only backup certain keys then these need to be tagged with the tag then included in the selection plan. See [example](https://registry.terraform.io/modules/lgallard/backup/aws/latest/examples/selection_by_tags)
* You cant restore from one account into another, but you can copy the restore into the desired account
