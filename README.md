<h1 align="center">Homie</h1>

<p align="center">

  <img src="https://github.com/mt40/homie/actions/workflows/deploy_test.yml/badge.svg?branch=master">
  <img src="https://github.com/mt40/homie/actions/workflows/deploy_live.yml/badge.svg?branch=release">
  <img src="https://github.com/mt40/homie/actions/workflows/health_check.yml/badge.svg?branch=master">
  <br>
  <a href="https://github.com/mt40/homie/compare/release...master">Request Live Deployment</a>

</p>

<p align="center">Homie is my personal smart assistant that helps me manage my life.</p>

<p align="center">
  <img src="https://media1.tenor.com/images/43c559bf7c92523dbf946b885be75156/tenor.gif?itemid=17464584">
  <br>
</p>

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

### iOS PWA

Homie can be used as a PWA in iOS. This means that you can add it to your home screen
as an app. I implemented this following these tutorials:

- https://superpwa.com/doc/test-pwa-ios-devices/
- https://firt.dev/ios-14.5/#progressive-web-apps-on-ios-14.5



