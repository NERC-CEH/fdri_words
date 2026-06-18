# ADR-017. Adopt Conditional Use of Amazon Detective within AWS Security Architecture

**Status:** Agreed - revisit in 4-6 months time.  Approved by Mike Brown

## Context and Problem Statement

AWS staging and production accounts currently have the following security services enabled:

* Amazon CloudWatch
* Amazon GuardDuty
* AWS Security Hub
* Amazon Detective

While these services provide strong security monitoring and visibility, Amazon Detective is generating significant ongoing costs of approximately $600 per month. We need to determine whether its additional investigation capabilities justify the expense.
This decision will sit under **infrastructure monitoring cost ownership and optimisation**, where IT is responsible for both current and long-term monitoring cost while ensuring effective security coverage. We therefore need to jointly evaluate the optimal use of these services to achieve full value, which may lead to further investigation work with IT in the background.

Amazon Detective applies machine learning and statistical analysis mainly to:

* Build behavioural baselines for users, roles, and resources
* Detect anomalous activity patterns (indirectly, by analysing relationships and events)
* Correlate findings from services like GuardDuty into investigation graphs
* Identify relationships between entities (who accessed what, when, from where)

## Decision Drivers

* Reduce AWS operating costs
* Maintain effective threat detection
* Maintain centralised security visibility
* Minimise operational complexity - fewer services to manage and less duplication of workflow
* Align with AWS security best practices

## Considered Options

1. Retain all four services
2. Temporarily disable AWS Detective pending further investigation and optimal configuration review and retain CloudWatch, GuardDuty, and Security Hub

## Pros and Cons of the Options

### Option 1 – Retain All Services

**Good because**

* Provides the most comprehensive AWS-native security stack
* Enables faster investigation and root-cause analysis

**Bad because**

* Highest ongoing cost
* Additional operational overhead

### Option 2 – Disable Detective (Recommended)

**Good because**

* Significantly reduces AWS cost
* Maintains core security monitoring and detection
* Aligns with cost-optimised architecture

**Bad because**

* Removes advanced investigation capabilities
* Requires more manual analysis during incidents

## Decision Outcome (after having a discussion with Stewart Kerr (IT), Dom, Nathan and Mike Brown)

**Chosen option:** Option 2 – temporarily disable AWS Detective pending further investigation and optimal configuration review and retain CloudWatch, GuardDuty, and Security Hub

GuardDuty provides threat detection, Security Hub provides centralised security findings and posture management, and CloudWatch provides monitoring and alerting.

Amazon Detective primarily provides investigation and root-cause analysis capabilities but does not add additional detection value.

For our current requirements, the cost of Detective is not justified by its usage.

## Positive Consequences

* Reduced AWS security costs
* Retains core threat detection through GuardDuty
* Retains centralised security visibility through Security Hub
* Simplifies management across multiple AWS environments

## Negative Consequences

* Loss of advanced investigation and relationship-graph capabilities
* Increased manual effort during incident investigations.  The increased  effort would involve manually correlating GuardDuty, security hub and cloudtrail data for any incidents potentially increasing incident response times.


## AWS Recommendations

AWS considers the following as foundational security services:

* **GuardDuty** – Detects threats such as compromised credentials, malware, and suspicious activity
* **Security Hub** – Aggregates security findings and provides posture management
* **CloudWatch** – Provides monitoring, logging, and alerting
* **Detective** – Optional service focused on forensic investigation and analysis

Removing Detective does not reduce detection capability; it only reduces investigation depth and automation.

## Future Considerations

Amazon Detective is not permanently excluded and may be re-enabled if future security investigations require deeper graph-based analysis or if its cost-to-value profile improves. The approach is to evaluate its usage based on operational need rather than maintaining it as a default always-on service.

## Links

* Amazon GuardDuty: https://aws.amazon.com/guardduty/
* AWS Security Hub: https://aws.amazon.com/security-hub/
* Amazon Detective: https://aws.amazon.com/detective/
* Amazon CloudWatch: https://aws.amazon.com/cloudwatch/
* AWS Detective User Guide: https://docs.aws.amazon.com/detective/latest/userguide/detective-recommendations.html
