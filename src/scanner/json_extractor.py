class JsonExtractor:

    def extract(self, file_path: str) -> list[TextUnit]:
        """
        Extract all translatable texts from a JSON file.
        """
        raise NotImplementedError