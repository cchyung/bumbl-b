#!/bin/bash
gunicorn -c gunicorn.config bumblebee_backend.wsgi:application
