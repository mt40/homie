# Homie

A personal assistant.

## Requirements

Install Docker on your machine.

## Usage

First, run some setups:

```shell
docker-compose run web python manage.py migrate
docker-compose run web python manage.py create_default_admin
docker-compose run web python manage.py init_db
```

Now run the server:
```shell
docker-compose up
```

## Architecture
### Components
![components diagram][components]

### Deployment flow
// todo

[components]: doc/diagrams.drawio.png