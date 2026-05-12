# Field Site Infrastructure Data Model

This document captures our current thinking and decisions about how we describe and name the elements of an FDRI field site.

## Questions

This piece of work aims to address the following questions:

- How can we represent the different elements of field sites as a model that is generic and flexible enough to apply across all field sites?
- What terms do we use to name the different elements of a field site?
- How are these elements related to one another?
- How do we define each term clearly and unambiguously?

## Proposed Data Model

We are converging towards a hierarchial model composed of four elements, from broadest to narrowest:

- Site
- Station
- Sensor Slot
- Sensor

### Site

A Site is a geographic concept. A Site is listed in the UKCEH Site Vocabulary.

A Site:

- is defined by a polygon,
- represents a physical area,
- has no operational or organisational ownership.

A Site may host multiple Stations operated by different Networks.

A Network cannot be attached directly to a Site, to avoid ambiguity when multiple organisations operate infrastructure at the same location.

### Network

A Network is an operational and organisational entity that operates Stations (i.e. infrastructure at a Site). A Network represents a collection of Stations managed under a common organisational structure.

### Station

A Station represents some infrastructure operated by a Network at a Site.

A Station may have its own polygon, defined by the Netowrk that operates it.

A Station carries operational metadata (management, maintenance responsability, etc.).

We could define Station Types (e.g. AWS, soil station, flux tower) for which we could develop a template listing all possible Sensor Slot types that may exist at that Station Type. This would help with consistency and validation without requiring every Station to use every Slot, and allowing them to add additional Slots where required.

### Platform (out of scope)

We initially thought that a Platform could be for things like a TDT array, but we decided that the concept of a Platform is unnecessary as such things can also be represented as a collection of Sensor Slots.

Platforms may still exist in the AMS, so we must ensure that any relevant information (e.g. platform-level faults) are propagated down to concepts that are part of this model (e.g. Sensor).

### Sensor Slot

A Sensor Slot represents a defined measurement at a Station. Each Sensor Slot corresponds to one time series dataset. Each Sensor Slot can host one Sensor at any given time. The Sensor deployed to a Sensor Slot may be replaced by another Sensor that measures the same variable, and this will not change the Sensor Slot. This allows for long-term continuity in our time series datasets.

Sensor Slot names should describe what is measured, e.g. primary rainfall measurement, secondary rainfall measurement, soil moisture at 30 cm depth.

### Sensor

A Sensor is a physical device.

A Sensor:

- has a serial number,
- has calibration, fault and maintenance history,
- has a deployment start and end date in relation to each Sensor Slot to which it is deployed,
- is replaceable by another Sensor,
- may be reused in other Sensor Slots over time.

We could define Sensor Types for which we could develop a template describing that Sensor Type, e.g. for when a Sensor is replaced by an identical one and all that needs changing is the serial number.

## Integration with the AMS

- Sensors in the AMS must be tagged as FDRI so that we only pull what we need into the metadata store
- Some concepts exist in the AMS but are intentionally not part of this data model (e.g. platform) to keep the model simple

## Dataset Identifiers

- Could we define a dataset ID as Sensor Slot ID + variable ID + frequency? Would this information suffice to unambiguously identify a time series dataset? Is information about frequency held in the AMS?
