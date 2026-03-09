[AWS vault](https://github.com/99designs/aws-vault) is used to securely store access your AWS creds in your dev environment. To get setup create a profile (ceh-test) and enter your AWS creds.

MacOS users might need to install brew.

> [!NOTE]  
> The original `aws-vault` is an abandoned project; an [active fork provides updates for range of platforms](https://github.com/byteness/aws-vault/releases/tag/v7.9.8)

## Guide for existing AWS account

```
# Store AWS credentials for the "ceh-test" profile
$ aws-vault add ceh-test
Enter Access Key Id: ABDCDEFDASDASF
Enter Secret Key: %%%
```

Create a profile in .aws/config. If you have MFA setup on your account this needs to be added.

```
[profile ceh-test]
region=eu-west-2
mfa_serial=arn:aws:iam::<AWS-account-id>:mfa/personal-phone
```

You can now start a subshell with temporary credentials. These will last for 1 hour by default but can be changed by overriding the AWS_SESSION_TOKEN_TTL environment variable.

```
# Start a subshell with temporary credentials
$ aws-vault exec ceh-test
Starting subshell /bin/zsh, use `exit` to exit the subshell
```

## Guide for new AWS accounts (through the landing zone)

Go the AWS access portal and select the account you want to connect to. Select `Access Keys` and then copy the `aws configure sso` command into your terminal.

Enter the requested details, `SSO start url` and `SSO Region` are taken from the page above, and then follow the instructions (just hit enter for the session scope value). If the provided URL doesn't load in the VM then load it outside and copy the code in.

Once finished, there should be a new profile in `~/.aws/config`. You can rename this profile to something more sensible.

Then `aws-vault exec <your-profile-name>` should start a session. Again, you will need to sing-in via the provided URL but this might only work outside of the VM.
