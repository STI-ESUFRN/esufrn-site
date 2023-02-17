#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'

poetry run celery -A esufrn beat -l info
