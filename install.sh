#!/bin/bash

# Clean install of app using bare minimum settings

conda=`which conda`
if [ -z conda ]; then
	echo "ERROR: No conda binary found. Exiting."
	exit 1
fi

# Clean up any existing conda environment
if [ -d "env" ]; then
	rm -r ./env
fi

# Install dependencies
conda create -q -p `pwd`/env --file ea/conda_reqs.txt -c uvcdat
source activate `pwd`/env
pip install -r ea/pip_reqs.txt

# Clear out cache folders
if [ -d uploads ]; then
	rm -r uploads
fi

if [ -d static ]; then
	rm -r static
fi

mkdir uploads
mkdir static

# Build config file
cat << >ea/eaconfig.cfg EOF
[paths]
root = `pwd`/ea
dataPath = `pwd`/uploads
static = `pwd`/static

[options]
debug = True
secret_key = secretsecret
hostname = localhost
port = 8000

[database]
ENGINE = django.db.backends.sqlite3
NAME = `pwd`/mydb.db
EOF

# Build the database, and make sure it's empty.
python ea/manage.py migrate
# NOTE: THIS WILL EMPTY YOUR DATABASE
python ea/manage.py flush --noinput