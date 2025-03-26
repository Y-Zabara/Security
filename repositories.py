class RegularFileRepo:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def get_text(self) -> str:
        with open(self.filename, "r") as content_file:
            return content_file.read()

    def save_bytes(self, bytes: bytes) -> None:
        with open(self.filename, "wb") as content_file:
            return content_file.write(bytes)

    def get_n_chars(self, n) -> str:
        text = self.get_text()
        return text[:n]
