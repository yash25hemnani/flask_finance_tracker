from mongoengine import Document, StringField, IntField, DateTimeField
from datetime import datetime

class Transaction(Document):
    CATEGORY_CHOICES = [
        ("Food", "Food"),
        ("Transport", "Transport"),
        ("Utilities", "Utilities"),
        ("Entertainment", "Entertainment"),
        ("Healthcare", "Healthcare"),
        ("Shopping", "Shopping"),
        ("Education", "Education"),
        ("Savings", "Savings"),
        ("Other", "Other")
    ]

    amount = IntField(required=True)
    date = DateTimeField(required=True)
    description = StringField(required=False)
    category = StringField(required=True, choices=CATEGORY_CHOICES)
    color = StringField(default="#000000")

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'transactions',
        'indexes': [
            'category', 'date'
        ],
        'ordering': ['-updated_at'],
        'auto_create_index': True
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(Transaction, self).save(*args, **kwargs)
