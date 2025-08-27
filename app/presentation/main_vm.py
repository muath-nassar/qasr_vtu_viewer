from typing import List
from PySide6.QtCore import QObject, Signal, Property, Slot
from app.application.import_meshes import ImportMeshes
from PySide6.QtWidgets import QFileDialog

from app.domain.types import MeshRef


class MainViewModel(QObject):
    _changed = Signal()

    def __init__(self, import_meshes: ImportMeshes) -> None:
        super().__init__()
        self._import_meshes = import_meshes
        self._meshes: List[MeshRef] = []

    @Property('QStringList', notify=_changed)
    def files(self) -> List[str]:
        print("getting meshes > updated now len = ", len(self._meshes))
        return [m.name for m in self._meshes]

    # Call this from your dialog result 
    def get_files(self, dir_path: str) -> None:
        try:
            meshes = self._import_meshes.run(dir_path)
            self._meshes.extend(m for m in meshes if m not in self._meshes)
        except Exception as exc:
            print(f"[VM][ERROR] get_files failed: {exc}")
        finally:
            self._changed.emit()
            print(f"files = {[m.path for m in self._meshes]}")

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
