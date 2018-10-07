#!/bin/sh
pylint channel2
mypy channel2
python manage.py test
