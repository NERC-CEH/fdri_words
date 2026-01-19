# [Architecture Decision Record (ADR) Identifier]. [short title of solved problem and solution] 

- Status: Draft v.1

## Context and Problem Statement 

Displaying raster layers served from TiTiler using leaflet has proven to be slow. Particularly when scrolling in and out, where parts of the raster can disappear entirely, taking a long time to re-appear, if at all. 

## Decision Drivers 
- Performance
- Ease of implementation
- Ability to support future feature requests, not just the existing basic rendering scenario in the FDRI geospatial UI.

## Considered Options 
- Leaflet
- Deck.gl

## Decision Outcome 

Yet to be determined. Currently testing the geospatial UI using deck.gl to see if it provides enough of a performance improvement to be worth the change. 

### Positive Consequences 
- Better performance
- ... 

### Negative Consequences 
- New library to learn
- ... 

### Pros and Cons of the Options 

#### [Deck.gl] 

Good

- Significant improvement in performance, particularly when loading multiple small (but higher resolution) raster layers
- Designed for handling large raster and vector datasets, and contains in built customisations such as detecting when a layer is outside the current viewing scope and not requesting tiles for it.
- Has capability to customise loading and rendering logic more than leaflet, which enables more opportunities for performance improvements.
- Designed for more advanced vector rendering, which could be very useful for any more complex UI functionality requests.
- Seems relatively simple to switch over from leaflet

Bad

- A new library to learn. Not many people are familiar with it.
- Adds more npm dependencies to the UI, which increases the built docker image size and may make managing dependencies harder.


#### [Leaflet] 

Good

- Used extensively throughout CEH meaning lots of people are familiar with it.
- Simple to learn and implement

Bad

- Designed to be used for simple raster rendering. Not optimised for loading a lot of layers at once
- Has minimal vector data support, so may not be able to be used for any more complex UI functionality requests. 


## Links 

 [Link to support documents] 
