

## Launching

#### before launch

install [docker](https://docs.docker.com/desktop/install/linux/)

`pipx install poetry`

Note! all docker-compose command using v2 with space instead of hyphen

### Local

`make db`  - run database in docker for local development

put in .env (root folder) DB_HOST=localhost

`poetry run python run.py` - run app, then go to http://localhost:8000/docs to see api


### Docker

put in .env (root folder) DB_HOST=postgres

`make start` - run app in docker'

## Development

#### Install pre-commit
`pipx install pre-commit`

`pre-commit install`

### Commands

#### make commands
`make lint` - run linters and formatters

`make stop` - shutdown containers

`make logs` - see logs of web container

`make migration m=<message>` - create migration

`make migrate` - apply migration

`pytest` - run test

see all actual short commands in Makefile

#### other commands

`poetry run alembic downgrade -1` - downgrade last migration
