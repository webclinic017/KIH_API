import mongoengine

from database import constants

mongoengine.connect(host=constants.DATABASE_URI, db=constants.DATABASE_NAME)
