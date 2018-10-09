# Channel 2

## Development Environment Setup

Setup a Python virtual environment and install requirements:

    $ python3 -m venv ~/.envs/channel2
    $ source ./scripts/activate.sh
    (channel2) $ pip install -r requirements.txt

Run the application:

    (channel2) $ python manage.py runserver

Run commit checks prior to committing:

    (channel2) $ ./scripts/precommit.sh

## Deploying Channel2

Use the following scripts:

    $ ./scripts/deploy-setup.sh
    $ ./scripts/deploy-update.sh
