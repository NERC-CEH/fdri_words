# 001. Document Architecture Decisions using ADRs

Status: proposed

Authors: Dominic Ginger

Deciders: Faiza Samreen, Dominic Ginger

Consulted: Dev Team, IT

Date: 2024-05-20

## Context and Problem Statement

We want a structured documentation approach to the decisions we make so
that we can move our projects forward with confidence and avoid
revisiting the same points.

How do we document the architectural decisions we are making for the
FDRI project and other future projects?

## Decision Drivers

- Easy to write

- No proprietary software

- Can be stored on SharePoint

- Consistent format

## Considered Options

- ADRs

- Design Docs

- RFCs

- Y Statements

- ISO 40210:2022

## Decision Outcome

Chosen option: ADRs, because industry standard and comes out top of
considered options (see below).

### Positive Consequences

- Modern standardized approach to documenting decisions

- Used by government organizations \[1\]\[2\]\[3\]

- Included in bigger architecture frameworks \[4\]

- Flexible can be written as markdown but also included in enterprise
  software (ADMaker in Sparx Enterprise Architect)

- Recommended to adopt by industry experts \[5\] and consultancies \[6\]

### Negative Consequences

- No single standardized template (This word doc is based on MADR \[7\])

- Although ADRs can be superseded the format does not lend itself to
  reflecting on decisions.

## Pros and Cons of the Options

###  Design Docs

[Design Docs at
Google](https://www.industrialempathy.com/posts/design-docs-at-google/)

- Good, used at Google, industry leader in ways of working practices

- Good, focuses on describing the architecture

- Good, includes metrics for measuring success/failure of the decision

### RFCs

<https://datatracker.ietf.org/doc/html/rfc7990>

- Good, because international standard used widely

- Bad, because makes a proposal rather than a decision

### 

### Y Statements

<https://socadk.github.io/design-practice-repository/artifact-templates/DPR-ArchitecturalDecisionRecordYForm.html>

- Good, because short, simple, and clear

- Bad, because limited by haiku size and lacks any detail.

### ISO 40210:2022

<https://ieeexplore-ieee-org.ezproxy.lancs.ac.uk/stamp/stamp.jsp?tp=&arnumber=9938446&tag=1>

- Good, because standards committee agreed way to describe software
  architecture

- Good, because in depth and full thought through

- Bad, because does not give a format to use but is a guideline on how
  to define a format

## Links

- \[1\] [Gov.uk documenting architecture
  decisions](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html#documenting-architecture-decisions)

- \[2\] [Gov.uk project listing
  ADRs](https://docs.modernising.opg.service.justice.gov.uk/adr/)

- \[3\] [US Gov why they use
  ADRs](https://18f.gsa.gov/2021/07/06/architecture_decision_records_helpful_now_invaluable_later/)

- \[4\] [Arc42 framework](https://arc42.org/overview)

- \[5\] [Martin Fowler - Scaling
  Architecture](https://martinfowler.com/articles/scaling-architecture-conversationally.html)

- \[6\] [Thoughtworks Tech Radar ADOPT
  ADrs](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)

- \[7\] [MADR ADR
  template](https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-of-the-madr-project)

- [NIST Big Data Interoperability
  Framework](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1500-6r2.pdf)

- [ISO List of architecture
  frameworks](http://www.iso-architecture.org/42010/afs/frameworks-table.html)

- [Evolving Reference Architecture Description (Expanding ISO
  40210:2022)](https://arxiv.org/pdf/2209.14714)

- [O\'reilly Head First Architecture
  Book](https://learning.oreilly.com/library/view/head-first-software/9781098134341/)

- [O\'reilly Communications Patterns
  Book](https://learning.oreilly.com/library/view/communication-patterns/9781098140533/)

- [Architectural Decision Guidance across
  Projects](https://www.ost.ch/fileadmin/dateiliste/3_forschung_dienstleistung/institute/ifs/cloud-application-lab/admentor-wicsa2015ubmissionv11nc.pdf)

- [ADR process at
  AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
