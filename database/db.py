import os
from databases import Database
import sqlalchemy

from dotenv import dotenv_values
config = dotenv_values(".env")

db = Database(config["DATABASE_URL"])
metadata = sqlalchemy.MetaData()