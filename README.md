# DiagnosticsViewer

The DiagnosticsViewer is a Django web application for uploading, sharing, and distributing any kind of structured output.
The [output_viewer](https://github.com/ESGF/output_viewer) project provides a convenient set of scripts for interacting with the app
(it builds a JSON, uploads the relevant files, and manages account information on the client).

## Installing

1. [Install anaconda](https://www.continuum.io/downloads)
2. Clone the repo (`git clone git://github.com/ESGF/DiagnosticsViewer`)
2. Install the conda requirements for the app: `conda create -p $REPO_DIRECTORY/env --file $REPO_DIRECTORY/ea/conda_reqs.txt`
3. Activate the conda environment (`source activate $REPO_DIRECTORY/env`)
3. Install the pip requirements for the app: `pip install -r $REPO_DIRECTORY/ea/pip_reqs.txt`
3. Create the config file (`cp $REPO_DIRECTORY/ea/eaconfig.cfg.tpl $REPO_DIRECTORY/ea/eaconfig.cfg`)
3. Update the config file's settings for your environment (Set the database up appropriately, update the secret_key, change debug to False when you go to production, update the paths section)
3. Create the database: `python manage.py migrate`
3. Create a superuser: `python manage.py createsuperuser`
3. Run the server in the stack of your choice.


This project was created in a collaboration of Lawrence Livermore National Laboratory and Oakridge National Laboratory
