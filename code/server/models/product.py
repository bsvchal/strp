from dataclasses import dataclass
from models.price import Price


@dataclass
class Product:
    id: str
    name: str
    price: Price
