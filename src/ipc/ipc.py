import struct

MSG_CTL = 0x00  # Message for telusurictl
MSG_IDX = 0x01  # Message for DBEngine<->Indexer

# telusurictl message
MSG_CTL_STATUS = 0x00
MSG_CTL_MODE = 0x01
MSG_CTL_LOGS = 0x10

# DBEngine message
# TODO dari DBEngine ada jenis apaan aja
MSG_IDX_HUHU = 0x11

IPC_MSG_FORMAT = '@BB'


class Message:

    __slots__ = ["type", "kind"]

    def __init__(self, data: bytes) -> None:
        fields = struct.unpack(IPC_MSG_FORMAT, data)
        (self.type, self.kind) = fields

    def fromWho(self) -> str:
        if self.kind == MSG_CTL_STATUS:
            return "status"
        elif self.kind == MSG_CTL_MODE:
            return "mode"
        elif self.kind == MSG_CTL_LOGS:
            return "logs"
        return "unknown"
