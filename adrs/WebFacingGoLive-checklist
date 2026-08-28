# Web facing go-live Checklist (v0.1 provided by Stewart Kerr from IT). Link to actual document https://cehacuk.sharepoint.com/:w:/r/sites/CloudUseandGuidance/Shared%20Documents/General/WebFacingGoLiveChecklist.docx?d=waf7f565a31a74334a39653fe66023f09&csf=1&web=1&e=j5SyOD

**Status Options:** `Yes` | `No` | `N/A` | `Under Discussion` | 'Action owned by IT / Platform Team`

## Status Legend

| Status | Meaning |

|----------|----------|

| ✅ Yes | Requirement met |

| ❌ No | Requirement not met |

| ➖ N/A | Not applicable |

| 🟡 Under Discussion | Requires further review or decision |

| 🔵 IT's Responsibility | Action owned by IT / Platform Team |

-----------------------------------------------------------------------------------------------------------------------
## VPC

| Status | Check |
|----------|----------|
| ☐ | No unused Internet Gateways attached |
| ☐ | Private workloads in private subnets |
| ☐ | Route tables reviewed and documented |
| ☐ | DNS resolution and hostnames enabled appropriately |

---

## Security Groups

| Status | Check |
|----------|----------|
| ☐ | No `0.0.0.0/0` on SSH (22), RDP (3389), or database ports |
| ☐ | Remove default security group permissions |
| ☐ | Review all ingress and egress rules for business justification |

---

## NACLs

| Status | Check |
|----------|----------|
| ☐ | Explicit deny rules for known unwanted traffic |
| ☐ | Restrict subnet-to-subnet traffic where needed |

---

## Public Access Review

**Review and document all publicly accessible resources.**

| Status | Resource |
|----------|----------|
| ☐ | Load Balancers |
| ☐ | EC2 Public IPs |
| ☐ | Elastic IPs |
| ☐ | Public RDS Instances |
| ☐ | Public EKS Endpoints |
| ☐ | Public S3 Buckets |

---

## Encryption

**Verify encryption is implemented appropriately.**

| Status | Check |
|----------|----------|
| ☐ | EBS encryption enabled by default |
| ☐ | RDS encryption enabled |
| ☐ | S3 encryption enforced |
| ☐ | EFS encryption enabled |

---

# Compute Hardening

## EC2

| Status | Check |
|----------|----------|
| ☐ | Latest hardened AMI in use |
| ☐ | SSM Agent installed |
| ☐ | No SSH access from the internet |
| ☐ | Session Manager preferred for administration |
| ☐ | Patch baseline assigned |

---

## Containers (EKS / ECS)

| Status | Check |
|----------|----------|
| ☐ | Container images scanned |
| ☐ | No privileged containers |
| ☐ | Secrets not stored in environment variables where avoidable |
| ☐ | Control plane access restricted |

---

## Lambda

| Status | Check |
|----------|----------|
| ☐ | Least-privilege execution roles configured |
| ☐ | No secrets embedded in code |
| ☐ | Logging enabled |

---

# Storage Review

## S3

| Status | Check |
|----------|----------|
| ☐ | Block Public Access enabled |
| ☐ | Bucket policies reviewed |
| ☐ | Versioning enabled |
| ☐ | Lifecycle policies configured |
| ☐ | Logging enabled for sensitive buckets |

---

## Backup

| Status | Check |
|----------|----------|
| ☐ | AWS Backup policies assigned |
| ☐ | Cross-account backup copies configured |
| ☐ | Restore process tested successfully |

---

# Data Protection & Resilience Review

**Confirm best practices appropriate to the data classification and business requirements have been adopted.**

| Status | Check |
|----------|----------|
| ☐ | Data Protection controls implemented |
| ☐ | Secrets management and encryption practices adopted |
| ☐ | Multi-AZ deployment implemented where appropriate |
| ☐ | Disaster Recovery strategy defined and implemented |

---

## Status Legend

| Status | Meaning |

|----------|----------|

| ✅ Yes | Requirement met |

| ❌ No | Requirement not met |

| ➖ N/A | Not applicable |

| 🟡 Under Discussion | Requires further review or decision |

| 🔵 IT's Responsibility | Action owned by IT / Platform Team |
