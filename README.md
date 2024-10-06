# NYC Soundscape Explorer

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

## Usage

Run the app

```sh
python manage.py runserver
```
