# 013. AWS Account Structure

- Status: proposed

## Context and Problem Statement

We currently have a single AWS account where staging and production are mixed together, we are going to shut this account down. We need an AWS account structure for the current FDRI workload and future DRI (Digital Research Infrastructure) initiatives, with consistent naming (e.g., `dri-staging`, `dri-production`).

We also want to replicate a subset of production data into the staging environment so staging tests can run on realistic, current data.

## Decision Drivers

- Environment isolation and blast-radius reduction (production must not be impacted by staging changes).
- Clear access boundaries and least-privilege permissions between staging and production.
- Cost visibility and governance as DRI expands to multiple projects/workloads.
- Operational reliability: ability to test infrastructure changes before production.
- Ability to keep staging data fresh

## Considered Options

- Option 1: Two AWS accounts: `dri-staging` and `dri-production` with cross-account S3 replication of a subset of production data into staging.
- Option 2: Single AWS account with two VPCs (staging VPC + production VPC).
- Option 3: Single AWS account, single Kubernetes cluster, split environments by Kubernetes namespaces.

## Decision Outcome

Chosen option: Option 1: Two AWS accounts, because AWS recommends separating production workloads from non-production workloads using separate accounts, this is the standard used by most organisations.

<img width="869" height="843" alt="image" src="https://github.com/user-attachments/assets/068e295c-5c21-40d0-8c1b-43bc5a137cf8" />


### Positive Consequences

- Strong default isolation: accounts are an AWS-native security/access boundary and are isolated unless explicitly opened up which reduces risk of staging impacting production.
- Cleaner IAM and safer operations: production permissions can be much tighter than staging, and access sharing becomes explicit.
- Better reliability and operability: rolling out infra changes can be tested in staging before production
- Straightforward staging freshness: use S3 cross-account replication rules/roles/policies to replicate only a subset of production objects into staging.

### Negative Consequences

- More operational overhead than a single account (duplicated baseline infrastructure).
- Cross-account replication introduces additional configuration, monitoring, and failure modes (replication lag, permission drift, encryption/KMS considerations).

### Pros and Cons of the other Options

#### Option 2: Single AWS account with two VPCs

One account containing both environments, separated by network boundaries (distinct VPCs), but still sharing the same account-level IAM/billing/quotas.

- Good, because it can reduce administrative overhead compared to multiple accounts.
- Good, because it may lower some costs for shared tooling/components.
- Bad, because it does not provide the same natural security/access/billing boundary as separate accounts, and requires more careful controls to avoid accidental cross-environment impact.

#### Option 3: Single AWS account + single Kubernetes cluster + namespaces

<img width="904" height="615" alt="image" src="https://github.com/user-attachments/assets/2547ce10-8cda-4bbc-9875-1626349d613b" />

One account and one cluster; staging and production are separated primarily by Kubernetes namespaces and Kubernetes RBAC, with shared underlying AWS resources.

- Good, because it can be significantly cheaper.
- Good, because it can be simpler, one place to look for things.
- Bad, because the blast radius is shared at the cluster and account level (cluster-level failures/misconfigurations can impact both environments).
- Bad, because it weakens the isolation boundary that separate accounts provide for access, governance, and operational safety.

## Links

- AWS Organizations best practices (multi-account environment): https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices.html
- AWS whitepaper: Organizing Your AWS Environment Using Multiple Accounts: https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html

