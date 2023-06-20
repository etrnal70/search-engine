import struct

DBE_MSG_FORMAT = '@BB'


class DBE_Message:

    __slots__ = ["type"]

    def __init__(self, data: bytes) -> None:
        fields = struct.unpack(DBE_MSG_FORMAT, data)
        (self.type) = fields
