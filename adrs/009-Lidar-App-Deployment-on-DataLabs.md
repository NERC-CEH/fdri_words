# 008. Lidar App Deployment on DataLabs

Status: Proposed

Authors: Lewis Chambers

Deciders: Lewis Chambers, Rafael Barbedo

Consulted:

Date: 2024-12-05

## Context and Problem Statement

The LiDAR app is currently aimed to be deployed on DataLabs using the
built-in "sites" functionality to provide a website-like interface for
users to interact with the data. There are a few methods of deployment
enabled in Datalabs, one of which must be chosen to develop in.

## Decision Drivers

- Must have interactive maps that support drawing of masks

- Must be deployable on Datalabs

- Must be scalable to multiple users

## Considered Options

- NBViewer

- Voila

- RShiny

- Panel

- Streamlit

## Decision Outcome

Chosen option: \"Shiny" because it is the only choice that supports all
of the project requirements

### Positive Consequences

- The app can be hosted on DataLab

### Negative Consequences

- R packages often have dependencies of Linux Packages that require a
  Datalabs admin to install

- The lead developer (Lewis) has no experience in writing R Shiny apps

## Pros and Cons of the Options

### NBViewer

[\[1\]](https://nbviewer.org/)

- Bad, because it's a non-interactive notebook display

### Voila

[\[2\]](https://voila.readthedocs.io/en/latest/?badge=latest)

- Bad, because it's effectively a notebook rendered for users. Not
  suitable for a webpage-like structure

- Good, because it's interactive

### Streamlit

[\[3\]](https://streamlit.io/)

- Good, because it supports widgets and complex layouts

- Good, because it has a 3^rd^ party add-on / widget store

- Bad, because data is stored in a cache and may have performance issues
  for a high-volume data application

- Bad because interactive map drawing is not supported

### Panel

<https://panel.holoviz.org/>

- Good, because it supports widgets and complex layouts

- Good, because interactive map drawing is available

- Bad, because clashes between \`ipyleaflet\` and \`DataLabs\` causes
  the draw functionality to have bugs -- only the first shape can be
  drawn, after that, the click that should should close a shape also
  starts a new shape, drawing them infinitely.

### Shiny

<https://shiny.posit.co/>

- Good, because it supports widgets and complex layouts

- Good, because interactive map drawing is available (and works)

- Good, because it's designed to support multiple users

- Good, because built in reactive components makes the code simpler (in
  theory)

- Bad for me (Lewis), because we only support Shiny for R, not my main
  language Python

## Links

- \[1\] <https://nbviewer.org/>

- \[2\] <https://voila.readthedocs.io/en/latest/?badge=latest>

- \[3\] <https://streamlit.io/>

- \[4\] <https://panel.holoviz.org/>

- \[5\] <https://shiny.posit.co/>
