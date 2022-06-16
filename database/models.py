from datetime import datetime
from typing import Dict, Tuple

from mongoengine import Document, StringField, DateTimeField

import database
from global_common import timed

database.connect_to_database()


class DatabaseDocument(Document):
    modified_time: datetime = DateTimeField(default=datetime.utcnow)
    modified_user_name: str = StringField()

    meta = {"abstract": True,
            "indexes": ["modified_time"]}

    def __repr__(self) -> str:
        return self.to_json()

    @timed
    def save(self, *args: Tuple, **kwargs: Dict) -> None:
        self.modified_time = datetime.utcnow()
        super().save()


class Person(DatabaseDocument):
    first_name: str = StringField()
    last_name: str = StringField()
