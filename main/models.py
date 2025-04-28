# prices/models.py
from datetime import datetime
from mongoengine import Document, StringField, DecimalField, DateTimeField

class CurrencyHistory(Document):
    name = StringField(required=True)
    price = DecimalField(required=True, precision=2)
    timestamp = DateTimeField(required=True)
    last_updated = DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': [
            {'fields': ['name', 'timestamp'], 'unique': True}
        ]
    }

