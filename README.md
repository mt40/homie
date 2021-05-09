<h1 align="center">Homie</h1>

<p align="center">
  <img src="https://github.com/mt40/homie/actions/workflows/deploy_test.yml/badge.svg?branch=master">
  <img src="https://github.com/mt40/homie/actions/workflows/deploy_live.yml/badge.svg?branch=release">
  <br>
  <a href="https://github.com/mt40/homie/compare/release...master">Request Live Deployment</a>
  <br><br>
  <img src="https://lparchive.org/Grand-Theft-Auto-San-Andreas-(Screenshot)/Update%2021/6-gtasa06.gif">
</p>

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
