from docx import Document

class DocFileRepo:
    """
    A repository class for handling .docx files.

    Attributes:
        file_path (str): The path to the .docx file.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the repository with the given file path.

        Args:
            file_path (str): The path to the .docx file.
        """
        self.file_path = file_path

    def get_text(self) -> str:
        """
        Reads the entire content of the .docx file and returns it as a string.

        Returns:
            str: The text content of the document.
        """
        doc = Document(self.file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])


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
