[AWS vault](https://github.com/99designs/aws-vault) is used to securely store access your AWS creds in your dev environment. To get setup create a profile (ceh-test) and enter your AWS creds.

New users might need to install brew.

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