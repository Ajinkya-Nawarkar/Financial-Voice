#!flask/bin/python
from app import app
import logging
import sys

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

app.run(debug=True)
# run locally via gunicorn app:app
