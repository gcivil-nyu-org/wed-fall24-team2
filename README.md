# NYC Soundscape Explorer

Main branch

[![Build Status](https://app.travis-ci.com/gcivil-nyu-org/wed-fall24-team2.svg?token=WJtjxLfBGECbRKomxGJe&branch=main)](https://app.travis-ci.com/gcivil-nyu-org/wed-fall24-team2)
[![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/wed-fall24-team2/badge.svg?branch=main)](https://coveralls.io/github/gcivil-nyu-org/wed-fall24-team2?branch=main)

Develop branch

[![Build Status](https://app.travis-ci.com/gcivil-nyu-org/wed-fall24-team2.svg?token=WJtjxLfBGECbRKomxGJe&branch=develop)](https://app.travis-ci.com/gcivil-nyu-org/wed-fall24-team2)
[![Coverage Status](https://coveralls.io/repos/github/gcivil-nyu-org/wed-fall24-team2/badge.svg?branch=develop)](https://coveralls.io/github/gcivil-nyu-org/wed-fall24-team2?branch=develop)

## Description

The NYC Soundscape Explorer is an interactive web application that allows users to explore and experience the diverse soundscape of New York City. 

## Features

- **Interactive Map**: A map of NYC with clickable neighborhoods to explore different sounds.
- **Sound Playback**: Ability to listen to ambient sounds specific to selected areas.
- **Noise Data Visualization**: Display of noise complaint data and sound levels across the city.
- **Search and Filter**: Users can filter sounds by type (e.g., traffic, music, nature) and location.
- **User Authentication**: Save settings, contribute content, and participate in discussions.
- **Chat Room**: Facilitate real-time community engagement and discussions.

## Target Users

- **Residents**: Understand neighborhood noises using heat map for better living decisions.
- **Researchers & Urban Planners**: Study noise pollution and urban planning.
- **Tourists**: Explore NYC’s soundscapes as part of their travel experience.
- **Community Activists**: Advocate for noise reduction and improved living conditions.
- **General Public**: Engage with NYC’s diverse auditory experiences.

## Project Structure

```sh
wed-fall24-team1/
├── .ebextensions
├── .elasticbeanstalk
├── .github/                    # GitHub configuration files
├── chatroom/                   # App that handles chatroom logic
├── core/                       # Main python package for the project
├── data_collection/            # Contains scripts to load NYCSoundData
├── sounddata_s3/               # Contains scripts to add NYCSoundData to AWS S3
├── soundscape/                 # Main app that handles frontend logic
│ ├── migrations/               
│ ├── static/                   # Static files (JS, images)
│ ├── templates/soundscape      # HTML templates for front-end
│ ├── tests/                    
│ ├── admin.py                  
│ ├── apps.py                   
│ ├── forms.py                  
│ ├── models.py
│ ├── urls.py          
│ └── views.py           
├── soundscape_user             # Contains user sound backend logic and script to add new sound descriptors
├── .coverage                  
├── .flake8                     # Setup for Python linting and formatting
├── .gitignore                  
├── .travis.yml                 # Setup for Travis CI / CD
├── Procfile                    
├── README.md
├── manage.py                   # Django management script
├── pytest.ini
└── requirements.txt            # Requirements to be installed with pip
```

## Installation

### Prerequisites
- Python 3.x (Recommended: 3.11.x)
- pip
- Virtual Environment (Recommended)
- AWS account

### Setup

Clone the repository:

```sh
git clone https://github.com/gcivil-nyu-org/wed-fall24-team2.git
cd wed-fall24-team2
```

Create virtual environment:

```sh
python -m venv env
```

Activate the virtual environment:

```sh
source env/bin/activate # On Windows: venv\Scripts\activate
```

Install required packages:

```sh
pip install -r requirements.txt
```

Run database migrations:

```sh
python src/manage.py makemigrations
python src/manage.py migrate
```

Configure AWS:

```sh
aws configure
```

Enter your AWS credentials when prompted:

- AWS Access Key ID
- AWS Secret Access Key
- Default region name (e.g., us-east-1)
- Default output format (json recommended)
  

**Configure environment files:**

Obtain an [API Key](https://www.mapbox.com/) from Mapbox. Then create a ".env" file in the root directory of the repo, and paste some contents in like this, but using your own api key:

```sh
# this is the ".env" file:
MAPBOX_ACCESS_TOKEN="__________"

...
```

Add database configuration to the ".env" file to access your local database:

```sh
...

DB_ENGINE='your_db_engine' # e.g., django.db.backends.postgresql_psycopg2
DB_NAME='your_db_name' # e.g., postgres
DB_USER='your_user_name' # e.g., postgres
DB_PASSWORD='your_password' # e.g. postgres (not recommended)
DB_HOST='your_rds_host_name' # e.g. nycsoundscape.c1aisqasc3u5.us-east-1.rds.amazonaws.com

...
```

Add AWS configuration to the ".env" file

```sh
...

AWS_ACCESS_KEY_ID='your_aws_access_key'
AWS_SECRET_ACCESS_KEY='your_aws_secret_access_key'
AWS_S3_REGION_NAME='your_aws_s3_region' # e.g., us-east-1
AWS_STORAGE_BUCKET_NAME='your_aws_s3_bucket_name' # e.g., nyc-sound-files
```

## Usage

Run the app

```sh
python manage.py runserver
```

The application will be available at ```http://127.0.0.1:8000/```

## Linting

This project uses ```flake8``` and ```black``` for linting and formatting Python files and djlint for HTML templates. To run linting locally:

```sh
black .
flake8
```

## Running tests and coverage

To run coverage tests locally:

```sh
coverage run --source='src' src/manage.py test
```

## Contributing

- Fork the repository
- Create a feature branch
- Commit your changes
- Push to the branch
- Create a Pull Request to the develop branch

## Collaborators

- Sonia Susanto: Product Owner
- Dipesh Parwani
- Manav Parikh
- Thejaswini D M
- Tzu-Yi(Belle) Chang
- Yashwanth Alapati
