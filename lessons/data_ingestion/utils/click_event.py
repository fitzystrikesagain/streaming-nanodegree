import json
from dataclasses import dataclass, field
from random import random

from faker import Faker

faker = Faker()


@dataclass
class Purchase:
    username: str = field(default_factory=faker.user_name)
    currency: str = field(default_factory=faker.currency_code)
    amount: int = field(default_factory=lambda: random.randint(100, 200000))

    def serialize(self):
        return json.dumps(
            {
                "username": self.username,
                "currency": self.currency,
                "amount": self.amount,
            }
        )


@dataclass
class ClickEvent:
    email: str = field(default_factory=faker.email)
    timestamp: str = field(default_factory=faker.iso8601)
    uri: str = field(default_factory=faker.uri)

    num_calls = 0

    def serialize(self):
        email_key = "email" if ClickEvent.num_calls < 10 else "user_email"
        ClickEvent.num_calls += 1
        return json.dumps(
            {"uri": self.uri, "timestamp": self.timestamp, email_key: self.email}
        )

    @classmethod
    def deserialize(self, json_data):
        purchase_json = json.loads(json_data)
        return Purchase(
            username=purchase_json["username"],
            currency=purchase_json["currency"],
            amount=purchase_json["amount"],
        )
