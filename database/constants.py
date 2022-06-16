import os

import global_common.constants

DATABASE_URI: str = os.environ["MONGO_DB_URI"]
DATABASE_NAME: str = global_common.constants.ENVIRONMENT
