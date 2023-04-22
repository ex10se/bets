import enum
import json
from decimal import Decimal


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, enum.Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)


def to_dec(num: float | int) -> Decimal:
    return Decimal(str(num))
