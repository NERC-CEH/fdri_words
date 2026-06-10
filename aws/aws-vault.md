[AWS vault](https://github.com/99designs/aws-vault) is used to securely store access your AWS creds in your dev environment. To get setup create a profile (ceh-test) and enter your AWS creds.

aws-vault can be installed via brew

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

### One-time: install aws-vault (if not installed already)

The original `99designs/aws-vault` is abandoned; use the `ByteNess` fork.  

Go to https://github.com/ByteNess/aws-vault/releases and find the latest version number (v7.12.1 as of writing).

```bash
# Download latest Linux amd64 binary - replace version number as appropriate
sudo curl -L -o /usr/local/bin/aws-vault \
  https://github.com/ByteNess/aws-vault/releases/download/v7.12.1/aws-vault-linux-amd64

sudo chmod 755 /usr/local/bin/aws-vault
aws-vault --version
```

### One-time: remove the old IAM user credentials 

If you had IAM user set up for the old account, might be best to remove these so things don't get confused.

1. Remove from aws-vault's store:
   
   ```bash
   aws-vault list
   aws-vault remove <user name>
   ```
   
3. Remove the long-term keys from the plain credentials file:
   
   ```bash
   gedit ~/.aws/credentials      # delete the IAM-user block
   ```
   
4. Remove the old IAM-user profile from `~/.aws/config`
   
### One-time: configure SSO

Go the AWS access portal and select the account you want to connect to (e.g. dri-staging). Select `Access Keys` - this will give you the values for the prompts that will come up below.

Configure SSO:

```bash
aws configure sso
```

Provide when prompted (from the `Access Keys` panel in the AWS access portal):

- SSO start URL
- SSO region
- Session scope - just hit enter for the default
- A sensible profile name

It will give you a URL that requires you to enter a one-time code.

This writes an `[sso-session ...]` block and an SSO `[profile ...]` block into `~/.aws/config`.  You can rename this profile to something more sensible if you didn't set it already.

### Daily usage

`aws-vault` should now detect the SSO profile and runs the SSO device-auth flow automatically (opens a browser, shows a `user_code`). Approve it in the browser; the token is cached until it expires (typically 8–12h), then re-prompts.

```bash
aws-vault exec <profile name>

# Do the authentication as prompted

# Starts a subshell - for a working session with many commands
#   ...run commands...

exit                              # leaves subshell, creds cleared from env
```
