from __future__ import annotations
import typing
from construct import Container
import borsh_construct as borsh


class BarStructFields(typing.TypedDict):
    some_field: bool
    other_field: int


class BarStructJSON(typing.TypedDict):
    some_field: bool
    other_field: int


class BarStruct:
    layout = borsh.CStruct("some_field" / borsh.Bool, "other_field" / borsh.U8)

    def __init__(self, fields: BarStructFields) -> None:
        self.some_field = fields["some_field"]
        self.other_field = fields["other_field"]

    @classmethod
    def from_decoded(cls, obj: Container) -> "BarStruct":
        return cls(
            BarStructFields(some_field=obj.some_field, other_field=obj.other_field)
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"some_field": self.some_field, "other_field": self.other_field}

    def to_json(self) -> BarStructJSON:
        return {"some_field": self.some_field, "other_field": self.other_field}

    @classmethod
    def from_json(cls, obj: BarStructJSON) -> "BarStruct":
        return cls(
            BarStructFields(
                some_field=obj["some_field"], other_field=obj["other_field"]
            )
        )
