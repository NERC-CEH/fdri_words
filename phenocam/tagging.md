# Tagging images

We need an interface to add tags to images (such as snow/standing
water present, field was harvested/ploughed).  If we view images as a
time series of observations at a site, then tags become an additional
series of observations parallel to the images.

## Requirements for tagging images

* Authenticated users can tag images for known tags and a free-form
  text field
* Tags are:
  * Land activity (harvested, mown, ploughed, sprayed)
  * Land cover change (if yes, select new from list)
  * Livestock
  * Other field obstruction or object
  * Corrupt
  * People
  * Lens obscured
  * Phenocam shifted
  * Snow
  * Standing water
  * Other data affected (e.g. rain gauge has fallen over)
* Tags are exported somewhere they can be linked to the images, and
  then shown in the UI when an image is selected, or available when
  requesting images from the API.

## Possible solutions

### Label Studio

[Label Studio](https://labelstud.io/) is an "open source data labeling
platform".  It's designed to add information to data intended for use
as machine learning training sets, but this sort of works out similar
enough to this use case that it might work.

Questions to answer:

* How does authentication/authorisation work?  Can it use an external
  user database?
* Can it pick up images from S3? Does it refresh automatically or is
  there some background task to wait for/trigger?
* What is the format of the (meta)data it exports? What formats can it
  export (SQLite/PostgreSQL/other)?
* Is it mature enough to support for the next 4+ years?
* Can it do optional fields?

### Other possibilities

* Amazon SageMaker
* UniversalDataTool
* CVAT
* Web gallery (e.g. Lychee, other Flickr-alike)
* Custom thing

## Decision

Given the fact that we would have to write some integration code for
Label Studio, and the risk of future updates causing breakage, we have
decided to proceed with building our own solution, integrated into the
Data API and DRI UI projects.

For now we will leave authentication/authorisation to one side, as the
project as a whole hasn't yet built a solution we can use, and it's
firewalled to permitted users only at the moment.

### Rough design


            ┌────────────────────────┐                  ┌──────────────────────────┐
            │                        │                  │                          │
            │     DRI Data API       +🭮─────────────────+      S3 bucket           │
            │                        +─────────────────🭬+        (Parquet files)   │
            │                        │    Tagging metadata                         │
            │                        │                  │                          │
            └────────+──+────────────┘                  └──────────────────────────┘
                     🭯  │
                     │  │
                     │  │
                     │  │
                     │  │
                     │  │     ┌─────────────────────┐
                     │  │     │                     │
                     │  🭭     │     Tagging         │
           ┌─────────+──+─────┤       interface     │
           │                  │                     │
           │                  │                     │
           │       DRI UI     └───────┬─────────────┘
           │                          │
           │                          │
           └──────────────────────────┘
