# Local use of images from the ECR registry

See [aws-vault](aws-vault.md) in this directory for setup. Run `aws-vault exec [workspace]` and then options:

Check the connection's working (should give you lots of JSON)
```
aws ecr describe-repositories
```

There is this method and a HTTP one which works more cleanly but deprecated by Docker. Edit region twice and numeric account ID, no dashes, once.

```
aws ecr get-login-password --region _region_ | docker login --username AWS --password-stdin _account_id_.dkr.ecr._region_.amazonaws.com
```

After this we can `docker pull` the full repository URLs for containers (like the metadata API) and it will Just Work

