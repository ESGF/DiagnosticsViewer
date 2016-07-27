[paths]
root = /path/to/the/ea/folder
dataPath = /place/to/upload/files
static = /place/to/serve/static/from

[options]
# Set to false for production
debug = True
# CHANGE THIS
secret_key = secretstring

hostname = localhost
port = 8000

# Any key here will be passed into the settings appropriately.
[database]
ENGINE = django.db.backends.sqlite3
NAME = /Users/fries2/Projects/DiagnosticsViewer/ea/mydb.db
