import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from app.container import AppContainer
from PySide6.QtWidgets import QApplication  # <-- use QApplication


def main() -> int:
    app = QApplication(sys.argv)  # <-- use QApplication here

    container = AppContainer()
    container.wire(packages=["app"])

    engine = QQmlApplicationEngine()
    vm = container.main_vm()
    engine.rootContext().setContextProperty("vm", vm)

    qml_path = Path(__file__).parent / "app" / "ui" / "Main.qml"
    engine.load(str(qml_path))

    if not engine.rootObjects():
        return 1
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
