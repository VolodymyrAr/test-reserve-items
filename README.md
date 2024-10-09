

## Launching

#### before launch

install [docker](https://docs.docker.com/desktop/install/linux/)

`pipx install poetry`

Note! all docker-compose command using v2 with space instead of hyphen

### Local

`docker compose up -d postgres`  - run local database

put in .env (root folder) DB_HOST=localhost

`poetry run python run.py` - run app, then go to http://localhost:8000/docs to see api


### Docker

put in .env (root folder) DB_HOST=postgres

`make run` - run app in docker'

## Development

`pipx install pre-commit`
`pre-commit install`

## Commands

`make lint` - run linters and formatters

`make stop` - shutdown containers

`make logs` - see logs of web container

`poetry run alembic revision --autogenerate -m "<message>"` - create migration

`poetry run alembic upgrade head` - apply migration
