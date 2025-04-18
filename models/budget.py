from mongoengine import Document, StringField, IntField, DateTimeField
from datetime import datetime

class Budget(Document):
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

    category = StringField(required=True, choices=CATEGORY_CHOICES)
    amount = IntField(required=True)
    month = IntField(required=True)
    year = IntField(required=True)

    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    meta = {
        'collection': 'budgets',
        'indexes': [
            {
                'fields': ['category', 'month', 'year'],
                'unique': True
            }
        ],
        'ordering': ['-updated_at'],
        'auto_create_index': True
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(Budget, self).save(*args, **kwargs)
