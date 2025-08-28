import os
from typing import List
from PySide6.QtCore import QObject, Signal, Property, Slot, QTimer
from app.application.import_meshes import ImportMeshes
from PySide6.QtWidgets import QFileDialog, QMessageBox

from app.domain.types import MeshRef


class MainViewModel(QObject):
    changed = Signal()
    statusMessageChanged = Signal()
    errorOccurred = Signal(str)

    def __init__(self, import_meshes: ImportMeshes) -> None:
        super().__init__()
        self._import_meshes = import_meshes
        self._meshes: List[MeshRef] = []
        self._state = ""

    def _get_state(self) -> str:
        return self._state

    def _set_state(self, value: str) -> None:
        if self._state != value:
            self._state = value
            self.statusMessageChanged.emit()

    state = Property(str, _get_state, _set_state, notify=statusMessageChanged)

    def _show_state(self, state: str) -> None:
        self._set_state(state)
        QTimer.singleShot(5000, lambda: self._set_state(""))


    @Property('QStringList', notify=changed)
    def files(self) -> List[str]:
        # should use logger print("getting meshes > updated now len = ", len(self._meshes))
        return [m.name for m in self._meshes]

    # Call this from your dialog result 
    def get_files(self, dir_path: str) -> None:
        try:
            meshes = self._import_meshes.run(dir_path)
            self._meshes.extend(m for m in meshes if m not in self._meshes)
        except Exception as exc:
            print(f"[VM][ERROR] get_files failed: {exc}")
            self._show_state(f"Error loading files: {exc}")
            self.errorOccurred.emit("Error in loading files. \n Only folders or .vtu files are allowed.")
        else:
            files_loaded = [m.path for m in self._meshes]
            if len(files_loaded) == 0:
                self._show_state("No .vtu files found in selection")
                self.errorOccurred.emit("No .vtu files found in selection")
            else:
                self._show_state(f"files = {files_loaded} are loaded")
        finally:
            self.changed.emit()
            

# --------- slots ---------------
    @Slot()
    def show_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        dialog = QFileDialog()
        # Only show .vtu files when browsing files
        dialog.setNameFilter("VTU files (*.vtu);;All files (*)")
        
        dialog.setFileMode(QFileDialog.ExistingFiles)  # Select files (multiple allowed)
        dialog.setOptions(options)
        dialog.setOption(QFileDialog.ShowDirsOnly, False)  # Show both files and folders

        if dialog.exec():
            selected = dialog.selectedFiles()
            for path in selected:  # Handle multiple selections
                if os.path.isdir(path) or path.endswith('.vtu'):
                    self.get_files(path)
                else:
                    print("Please select a folder or a .vtu file.")

    @Slot(str)
    def load_folder(self, folder_path):
        print("Loading folder:", folder_path)
        if len(folder_path) > 0:
            self.get_files(folder_path)
