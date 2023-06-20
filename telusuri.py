# Here it will abstract running the crawler and indexer process
class Telusuri:

    def __init__(self, log_path: str) -> None:
        self.mode: str = "crawler"
        self.log_path = log_path

    def status(self) -> str:
        return self.mode

    # TODO Should return stream of logs (?)
    def getLogs(self, mode: str) -> str:
        return "Makan nih log gblk orang blom jadi asw"

    # TODO
    def switchMode(self, mode: str) -> None:
        pass
