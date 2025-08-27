from typing import List
from PySide6.QtCore import QObject, Signal, Property, Slot
from app.application.import_meshes import ImportMeshes
from PySide6.QtWidgets import QFileDialog


class MainViewModel(QObject):
    _changed = Signal()

    def __init__(self, import_meshes: ImportMeshes) -> None:
        super().__init__()
        self._import_meshes = import_meshes
        self._files: List[str] = []

    @Property('QStringList', notify=_changed)
    def files(self) -> List[str]:
        return self._files

    # Call this from your dialog result (temporary: pass a path manually)
    def get_files(self, dir_path: str) -> None:
        self._files = self._import_meshes.run(dir_path)
        try:
            self._files = self._import_meshes.run(dir_path)
        except Exception as exc:
            self._files = []
            print(f"[VM][ERROR] get_files failed: {exc}")
        finally:
            self._changed.emit()
            print(f"files = {self._files}")

    @Slot()
    def show_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)  # allow file selection
        file_dialog.setOptions(options)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, False)  # show files and folders

        if file_dialog.exec():
            selected = file_dialog.selectedFiles()
            if selected:
                path = selected[0]
                # Check if it's a directory or a .vtu file
                import os
                if os.path.isdir(path) or path.endswith('.vtu'):
                    self.get_files(path)
                else:
                    print("Please select a folder or a .vtu file.")
