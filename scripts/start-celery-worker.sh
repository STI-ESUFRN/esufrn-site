#!/bin/bash

set -o errexit
set -o nounset

poetry run celery -A esufrn worker --loglevel=info
