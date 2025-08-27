from app.domain.ports import Logger
class StdoutLogger(Logger):
    """Simple stdout logger used by default (can be swapped via DI)."""
    def info(self, msg: str) -> None:
        print(f"[INFO] {msg}")

    def error(self, msg: str) -> None:
        print(f"[ERROR] {msg}")
    
    def debug(self, msg: str) -> None:
        print(f"[DEBUG] {msg}")
    
    def warning(self, msg: str) -> None:
        print(f"[WARNING] {msg}")

