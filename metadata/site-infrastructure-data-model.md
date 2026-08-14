# Field Site Infrastructure Data Model

This document captures our current thinking and decisions about how we describe and name the elements of an FDRI field site.

## Questions

This piece of work aims to address the following questions:

- How can we represent the different elements of field sites as a model that is generic and flexible enough to apply across all field sites?
- What terms do we use to name the different elements of a field site?
- How are these elements related to one another?
- How do we define each term clearly and unambiguously?

## Proposed Data Model

We have opted for a model in which everything is a typed ``Facility``, rather than a specialised hierarchial class model.

Possible ``Facility`` types include:

- Site
- Platform
- Sensor

This choice has been made for FDRI because:

- Existing standards indicate that this is the best solution for interoperability (see [INSPIRE Data Specification on Environmental Monitoring Facilities](https://knowledge-base.inspire.ec.europa.eu/publications/inspire-data-specification-environmental-monitoring-facilities-technical-guidelines_en))
- This solution results in a model that is more flexible and easier to adapt to the introduction of new asset types
- This solution results in a model that does not require every asset to respect a strict hierarchy, e.g. a platform does not necessarily have to be part of a site and may belong directly to a network.

### Network (class)

A ``Network`` is an operational or organisational entity. A ``Network`` consists of one or more ``Facilities``. A ``Facility`` can be part of any number of ``Networks``. A recursive hierarchical link exists between ``Networks``, meaning that any ``Network`` can be part of another ``Network``.

### Facility (class)

Every asset is a ``Facility``. A ``Facility`` can be fixed or mobile. A recursive hierarchical link exists between ``Facilities``, meaning that any ``Facility`` can be part of another ``Facility``.

#### Site (type)

A ``Site`` is a type of ``Facility``. A ``Site`` is a geographic concept. A ``Site`` is listed in the UKCEH Site Vocabulary.

A ``Site``:

- has a geographic location defined by a polygon,
- represents a physical area,
- has no operational or organisational ownership.

A ``Site`` may contain multiple ``Facilities`` operated by different ``Networks``.

#### Platform (type)

A ``Platform`` is a type of ``Facility``.

A ``Platform``:

- has a geographic location defined by a point,
- may be moved in and out of a ``Site``.

#### Sensor (type)

A ``Sensor`` is a type of ``Facility``. A ``Sensor`` is a physical device.

A ``Sensor``:

- has a serial number,
- has calibration, fault and maintenance history,
- has a deployment start and end date in relation to each ``Platform`` to which it is deployed,
- is replaceable by another ``Sensor``,
- may be reused in other ``Platforms`` over time.

### Facility Group (class)

We could create ``Facility Groups`` to bring together  ``Facilities`` that belong to a specific grouping for analytical or geographic purposes, e.g. region or catchment.
