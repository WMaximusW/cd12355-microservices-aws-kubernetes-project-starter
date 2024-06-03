import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_username = os.environ.get("DB_USERNAME", "trungnq72-user")
db_password = os.environ.get("DB_PASSWORD", "trungnq72-password")
db_host = os.environ.get("DB_HOST", "host.docker.internal")
db_port = os.environ.get("DB_PORT", "5433")
db_name = os.environ.get("DB_NAME", "trungnq72-database")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

db = SQLAlchemy(app)

app.logger.setLevel(logging.DEBUG)