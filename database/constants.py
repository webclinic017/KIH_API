import os

import global_common.constants

DATABASE_URI: str = os.getenv("MONGO_DB_URI")
DATABASE_NAME: str = global_common.constants.ENVIRONMENT
