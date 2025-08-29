# app/viewer/viewer_widget.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from app.vtk_adapters.scene import VTKScene

class VTKViewerWindow(QMainWindow):
    def __init__(self, scene: VTKScene, parent=None):
        super().__init__(parent)
        self.setWindowTitle("VTK Viewer")

        central = QWidget(self)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        # VTK widget
        self.vtk = QVTKRenderWindowInteractor(central)
        layout.addWidget(self.vtk)
        self.setCentralWidget(central)

        # Attach your scene to this window's vtkRenderWindow
        rw = self.vtk.GetRenderWindow()
        scene.attach_render_window(rw)

        # Initialize interactor (do NOT call Start() in Qt apps)
        iren = rw.GetInteractor()
        if iren is not None:
            iren.Initialize()
