# NYC Soundscape Explorer

[![Build Status](https://app.travis-ci.com/gcivil-nyu-org/wed-fall24-team2.svg?token=WJtjxLfBGECbRKomxGJe&branch=develop)](https://app.travis-ci.com/gcivil-nyu-org/wed-fall24-team2)
[![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/wed-fall24-team2/badge.svg)](https://coveralls.io/github/gcivil-nyu-org/wed-fall24-team2)

## Setup

Create virtual environment:

```sh
python -m venv env
```

Activate the environment:

```sh
source env/bin/activate
```

Install packages:

```sh
pip install -r requirements.txt
```

Environment files:

Obtain an [API Key](https://www.mapbox.com/) from Mapbox. Then create a ".env" file in the root directory of the repo, and paste some contents in like this, but using your own api key:

```sh
# this is the ".env" file:
MAPBOX_ACCESS_TOKEN="__________"
```
Add database configuration to the ".env" file to access your local database:
```sh
...

DB_ENGINE='__________'
DB_NAME='__________'
DB_USER='__________'
DB_PASSWORD='__________'
```
## Usage

Run the app

```sh
python manage.py runserver
```
