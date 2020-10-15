#!/bin/sh

echo "MIGRATING"
flask db upgrade

echo "RUNNING"
flask run --host=0.0.0.0
