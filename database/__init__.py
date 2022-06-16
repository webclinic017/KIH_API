import mongoengine
from pymongo import MongoClient

from database import constants
from global_common import timed

mongo_client: MongoClient = None


@timed
def connect_to_database() -> None:
    global mongo_client
    if mongo_client is None:
        mongo_client = mongoengine.connect(host=constants.DATABASE_URI, db=constants.DATABASE_NAME)
