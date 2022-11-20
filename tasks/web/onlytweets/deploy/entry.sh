#!/bin/bash

python3 init_db.py && gunicorn app:app --bind 0.0.0.0:4321 --workers 3