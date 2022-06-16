from datetime import datetime

from mongoengine import Document, StringField, DateTimeField


class DatabaseDocument(Document):
    modified_time: datetime = DateTimeField(default=datetime.utcnow)
    modified_user_name: str = StringField()

    meta = {"abstract": True,
            "indexes": ["modified_time"]}

    def save(self, **kwargs) -> None:
        self.modified_time = datetime.utcnow()
        super().save()
