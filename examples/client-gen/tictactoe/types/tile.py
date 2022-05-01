from __future__ import annotations
import typing
from construct import Container
import borsh_construct as borsh


class TileFields(typing.TypedDict):
    row: int
    column: int


class TileJSON(typing.TypedDict):
    row: int
    column: int


class Tile:
    layout = borsh.CStruct("row" / borsh.U8, "column" / borsh.U8)

    def __init__(self, fields: TileFields) -> None:
        self.row = fields["row"]
        self.column = fields["column"]

    @classmethod
    def from_decoded(cls, obj: Container) -> "Tile":
        return cls(TileFields(row=obj.row, column=obj.column))

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"row": self.row, "column": self.column}

    def to_json(self) -> TileJSON:
        return {"row": self.row, "column": self.column}

    @classmethod
    def from_json(cls, obj: TileJSON) -> "Tile":
        return cls(TileFields(row=obj["row"], column=obj["column"]))
