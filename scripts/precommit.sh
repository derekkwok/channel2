#!/bin/sh
python manage.py test
pylint channel2
mypy channel2
