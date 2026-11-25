from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str = field(repr=False)

    @classmethod
    def unique(cls) -> "Credentials":
        return cls(username=f"qa_{uuid4().hex}", password=f"Qa!{uuid4().hex}")

    def payload(self) -> dict[str, str]:
        return {"username": self.username, "password": self.password}


@dataclass(frozen=True)
class Account:
    id: int
    credentials: Credentials
    token: str = field(repr=False)


def item_payload(seller_id: int, **overrides: Any) -> dict[str, Any]:
    return {
        "sellerID": seller_id,
        "name": f"QA sofa {uuid4().hex}",
        "price": 9900,
        "statistics": {"likes": 21, "viewCount": 11, "contacts": 43},
        **overrides,
    }
