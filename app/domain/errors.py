
class PathNotFound(Exception):
    """The provided path does not exist (file or directory)."""
    def __init__(self, path: str):
        super().__init__(f"Path not found: {path}")
        self.path = path

class NotVTUFile(Exception):
    """A file path was provided but it is not a .vtu file."""
    def __init__(self, path: str):
        super().__init__(f"Not a .vtu file: {path}")
        self.path = path
