# RDS Database Access

Access to our RDS database involves a number of concepts

## Concepts

### Postgres Roles
<img width="333" height="270" alt="image" src="https://github.com/user-attachments/assets/ebdeb4aa-1a07-4775-b005-6f8c33074f3f" />

Postgres users = postgres roles that are allowed to login. These can be granted permissions, e.g can perform SELECT, INSERT on table X in schema Y.

### AWS IAM Roles and Policies
<img width="330" height="330" alt="image" src="https://github.com/user-attachments/assets/d81e4ab8-f845-4f76-8e6f-4ebe3b10d316" />


These allow permission granting to resources, e.g connecting to an RDS database, access to an s3 bucket.

### Kubernetes Service Accounts
<img width="330" height="330" alt="image" src="https://github.com/user-attachments/assets/be7e647e-5a99-42aa-bdfb-33744784184f" />


Since our code is deployed to Kubernetes, we need to map the IAM roles to kubernetes service accounts.

### Full Picture
These are all connected like this
<img width="866" height="768" alt="image" src="https://github.com/user-attachments/assets/d29a96de-e640-454d-9212-8efd9910774d" />



## How to setup a new service user

The phenocam_ingestion example can likely be copied and changed for future use cases.

### 1. Create the role in postgres

```sql
CREATE ROLE new_service_role; # Create the role

GRANT CONNECT ON DATABASE postgres TO new_service_role; # Allow role to connect to database
GRANT USAGE ON SCHEMA my_schema TO new_service_role; # Allow role to use specific schema
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA my_schema TO new_service_role; # Allow actions on tables in schema

ALTER ROLE new_service_role LOGIN; # Allow role to login (make role a user)
GRANT rds_iam TO new_service_role; # Allow role to login via RDS IAM
```

#### Example
https://github.com/NERC-CEH/dri-database-models/blob/main/alembic/versions/9252cb9ae98d_add_phenocam_ingestion_role.py
https://github.com/NERC-CEH/dri-database-models/blob/main/alembic/versions/122b06ec6a9a_allow_phenocam_ingestion_to_login_via_.py

### 2. Setup the IAM role and policies
```yaml
# Setup the trust policy (Maps the IAM role the Kubernetes Service Account)
data "aws_iam_policy_document" "new_service_user_trust" {
  statement {
    effect = "Allow"
    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${module.common.aws_account.id}:oidc-provider/${var.eks_oidc_url}"]
    }
    actions = ["sts:AssumeRoleWithWebIdentity"]
    condition {
      test     = "StringEquals"
      variable = "${var.eks_oidc_url}:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "${var.eks_oidc_url}:sub"
      values   = ["system:serviceaccount:my_namespace:new_service_user"]
    }
  }
}

# Create the IAM Role
resource "aws_iam_role" "new_service_user" {
  assume_role_policy = data.aws_iam_policy_document.new_service_user_trust.json
  name               = "new_service_user_role"
}

# Create policy to allow Role to connect to RDS DB
data "aws_iam_policy_document" "new_service_user_policy_document" {
  statement {
    actions = [
      "rds-db:connect"
    ]
    resources = [
      "arn:aws:rds-db:${module.common.aws_account.region}:${module.common.aws_account.id}:dbuser:${module.dri_db_cluster.cluster_resource_id}/new_service_user"
    ]
    effect = "Allow"
  }
}

resource "aws_iam_policy" "new_service_user_policy" {
  name   = "dri-db-new-service-user-policy"
  policy = data.aws_iam_policy_document.new_service_user_policy_document.json
}

# Attach the policy to the Role
resource "aws_iam_role_policy_attachment" "new_service_user_attachment" {
  role       = aws_iam_role.new_service_role
  policy_arn = aws_iam_policy.new_service_user_policy.arn
}
```

#### Example
https://github.com/NERC-CEH/dri-infrastructure/blob/main/staging/modules/ingestion/iam.tf#L303
https://github.com/NERC-CEH/dri-infrastructure/blob/main/staging/modules/dri-db/iam.tf#L44

### 3. Setup the Kubernetes Service Account
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: new_service_user
  namespace: my_namespace
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::654654490827:role/new_service_user_role
```

#### Example
https://github.com/NERC-CEH/dri-infrastructure-k8s-staging/blob/main/workloads/dri-ingestion/service-accounts.yaml#L41
https://github.com/NERC-CEH/dri-infrastructure-k8s-staging/blob/main/workloads/dri-ingestion/deployment-phenocam.yaml#L17

### 4. Check everything works

With these 3 things in place, they should map together and allow the service to connect to the RDS database under the define postgres role. The connection can be tested with the following python code.

```python
import boto3
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

DB_USER = "postgres"
DB_HOST = 'localhost'
DB_NAME = "postgres"
DB_PORT = 5432
REGION = "eu-west-2"

client = boto3.client('rds')

token = client.generate_db_auth_token(DBHostname=DB_HOST, Port=DB_PORT, DBUsername=DB_USER, Region=REGION)

db_url_object = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=token,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(db_url_object)

with engine.connect() as connection:
    print("Connection successful!")
```

#### Example 

https://github.com/NERC-CEH/dri-ingestion/blob/main/src/ingestion/ingesters/phenocam/ingester.py#L67

