# Getting Started

Walkthrough of getting started with local development and testing of the FDRI stack.

Clone the [dri-data-api](https://github.com/NERC-CEH/dri-data-api/) repository.

`uv sync` and activate the environment

Set up, according to its instructions, a copy of `localstack` with a small amount of test data in it.

`docker compose --profile localstack up`

Run the tests. Ensure we have python version 3.12 or above.

Run the application locally. This needs environment variables set in `.env`. There is a default `config.env` which does not need changed.

`DUCKDB_TIMEDELTA=10000 python -m dataapi`

This should now give us a locally running copy of the API + storage accessible at:

http://localhost:8000/v1/docs _note the *v1* everywhere_

Next the [dri-ui](https://github.com/NERC-CEH/dri-ui/) repository for the web application that sits atop.

`npm install --force`

Edit the `.env` file to point to localhost:8000 for the API_ENDPOINT
`npm run dev`

This brings up a Vite application server with the app on port 3000.



