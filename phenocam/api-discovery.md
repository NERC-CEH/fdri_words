# phenocam notes

There will be a load[^1] of images dumped into S3.  We need a way of
indexing and filtering them by site and date, generating pre-signed
URLs and presenting them to the user.

Use [metadata api](https://github.com/NERC-CEH/dri-metadata-api)?  Not
100% clear what it can provide.

* Is it fast enough just to grab bucket contents as an API call,
  generate pre-signed URLs for each, and return them to the frontend?


[^1]: something like 5 images per site per day

## Pre-signed URLs

<https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html>

Validity up to 7 days, though depends on the credential used to create
it.

## Autogenerating thumbnails/resizing images

Dom mentioned that it might be possible to have S3 automatically
resize the images on the fly as they are requested.  I can't see
whether this is possible without using Lambda, as in [this
tutorial][resize-images-lambda].  Not sure how necessary this is
really - depends on how big the images are and how many the client
requests at once.

[resize-images-lambda]: https://aws.amazon.com/blogs/compute/resize-images-on-the-fly-with-amazon-s3-aws-lambda-and-amazon-api-gateway/

## Sketch API design

`/v1/phenocam/images?site=<site>&from=<from>&to=<to>`
returns
```js
{
    "images": [
        {
            "site": "ALIC1",
            "date": "1970-01-01T00:00:00Z", // or 1739976978
            "url": "<pre-signed url>",
            "metadata": {
                "reviewed": false,
                // ...
            }
        },
        // ...
    ],
    // ...
}
```

Eventually, perhaps also
`/v1/phenocam/masks/<site>?from=<>&to=<>`
returns
```js
{
    "masks": [
        {
            "site": "ALIC1",
            "dateFrom": "1970-01-01T00:00:00Z",
            "dateTo": "1970-01-01T00:00:00Z",
            "url": "<pre-signed url>",
            "metadata": {
                //...
            }
        },
        //...
    ],
    //...
}
```

