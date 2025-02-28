## Setup env
python -m venv env or python3 -m venv env

## Activate env
### Linux
`source env/bin/activate`
### Windows
`env\Scripts\activate`

## Rename the env.sample to .env

## Change the .env values.

## Build
`docker compose -f compose.yaml -f compose.dev.yaml build`

## Run
`docker compose -f compose.yaml -f compose.dev.yaml up --watch`
