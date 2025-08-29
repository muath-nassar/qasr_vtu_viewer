from collections.abc import Set
import os
from typing import Dict, List
from PySide6.QtCore import QObject, Signal, Property, Slot, QTimer
from app.application.fit_view_all import FitViewAll
from app.application.import_meshes import ImportMeshes
from PySide6.QtWidgets import QFileDialog, QMessageBox

from app.application.load_mesh import LoadMesh
from app.application.set_visibility import SetVisibility
from app.domain.types import MeshRef
from app.domain.ports import Logger


class MainViewModel(QObject):
    changed = Signal()
    statusMessageChanged = Signal()
    errorOccurred = Signal(str)

    def __init__(self,
                log: Logger,
                import_meshes: ImportMeshes,
                load_mesh: LoadMesh,
                set_visibility: SetVisibility,
                fit_view_all: FitViewAll) -> None:
        super().__init__()
        self._log = log
        self._import_meshes = import_meshes
        self._load_mesh = load_mesh
        self._set_visibility = set_visibility
        self._fit_view_all = fit_view_all

        # ---- UI related variables -------
        self._meshes_ref: List[MeshRef] = []
        self._state = ""
        self._meshs_ids: Dict[str, str] = {} # path -> mesh_id

    # ---- state management strat-------
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

    # ---- state management end -------

    @Property('QStringList', notify=changed)
    def files(self) -> List[str]:
        # should use logger print("getting meshes > updated now len = ", len(self._meshes))
        return [m.name for m in self._meshes_ref]

    # called from file dialog or by the open folder 
    def get_files(self, dir_path: str) -> None:
        try:
            meshes = self._import_meshes.run(dir_path)
            if not meshes:
                self._show_state("No .vtu files found in selection")
                self.errorOccurred.emit("No .vtu files found in selection")
                self.changed.emit()
                return

            for m in meshes:
                try:
                    self._register_mesh_to_scene(m)
                    self._meshes_ref.append(m)
                    self.changed.emit()
                except Exception as e:
                    self._log.error(f"[VM] failed to register mesh: {m.name} error: {e}")
                    self._show_state(f"Error registering mesh: {m.name}")

            files_loaded = [m.path for m in self._meshes_ref]
            self._show_state(f"files = {files_loaded} are loaded")

        except Exception as exc:
            print(f"[VM][ERROR] get_files failed: {exc}")
            self._show_state(f"Error loading files: {exc}")
            self.errorOccurred.emit("Error in loading files. \n Only folders or .vtu files are allowed.")

    def _register_mesh_to_scene(self, ref: MeshRef) -> None:
        self._log.info(f"[VM] registering mesh: {ref.name}")
        mesh_id = self._load_mesh.run(ref.path, ref.name)
        self._meshs_ids[ref.path] = mesh_id

 


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

    @Slot(int, bool)
    def toggleVisible(self, index: int, on: bool) -> None:
        if index < 0 or index >= len(self._meshes_ref):
            return
        ref = self._meshes_ref[index]
        mesh_id = self._meshs_ids.get(ref.path)
        if mesh_id:
            self._set_visibility.run(mesh_id, on)

    @Slot()
    def fitAll(self) -> None:
        if self._fit_view_all:
            self._fit_view_all.run()
