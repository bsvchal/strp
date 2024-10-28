from dataclasses import dataclass


@dataclass
class Price:
    id: str
    nickname: str
    currency: str
    unit_amount: str
    lookup_key: str
