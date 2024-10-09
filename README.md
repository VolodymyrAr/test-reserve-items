## Launching

### Local

`docker compose up -d postgres`  - run local database

`python run.py` - run app, then go to http://localhost:8000/docs to see api

### Docker

`make run` - run app in docker'

## Development

`pipx install pre-commit`
`pre-commit install`

## Commands

`make lint` - run linters and formatters

`make down` - shutdown containers

`make logs` - see logs of web container
