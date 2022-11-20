#!/bin/bash

python3 init.py && gunicorn app:app --bind 0.0.0.0:3210 --workers 4