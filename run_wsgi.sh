#!/bin/bash

APP_SETTINGS=settings.cfg uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app

