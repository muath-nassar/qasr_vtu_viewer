# check_vtk_qt.py
import sys, platform, importlib.util, pathlib, os

print("\nPlatform:")
print(f"  {platform.platform()} | {platform.machine()}")

# --- Core imports ---
ok = lambda name: print(f"[OK]   {name}") if importlib.util.find_spec(name) else print(f"[MISS] {name}")
ok("vtkmodules.vtkRenderingOpenGL2")
ok("dependency_injector")
ok("dependency_injector.containers")
ok("dependency_injector.providers")

# --- Qt version + simple QML smoke test ---
from PySide6.QtCore import qVersion, QUrl, QByteArray
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent

print("\nQt info:")
print(f"[OK]   Qt version: {qVersion()}")

app = QApplication.instance() or QApplication(sys.argv)

# 1) Plain QML works?
qml_min = b"import QtQuick 2.15\nRectangle { width: 100; height: 100; color: 'red' }"
engine = QQmlApplicationEngine()
engine.loadData(QByteArray(qml_min), QUrl("inmemory.qml"))
print("[OK]   QML basic load" if engine.rootObjects() else "[MISS] QML basic load")

# 2) Try to locate VTK's QML plugin dir (optional help)
try:
    import vtk
    vtk_dir = pathlib.Path(vtk.__file__).parent
    # heuristics: look for a 'vtk-* / qmldir' under the package
    candidates = list(vtk_dir.rglob("vtk-*/qmldir"))
    if candidates:
        qml_dir = str(candidates[0].parent)
        print(f"[hint] Found VTK qml dir candidate: {qml_dir}")
        # if needed, uncomment to force it:
        # os.environ["QML2_IMPORT_PATH"] = qml_dir + os.pathsep + os.environ.get("QML2_IMPORT_PATH","")
    else:
        print("[hint] No VTK qml plugin found under site-packages; Qt Quick support may be missing")
except Exception as e:
    print(f"[hint] vtk introspection error: {e}")

# 3) VTK QML import test
qml_vtk = b"""
import QtQuick 2.15
import VTK 9.3

VTKRenderWindow {
    id: rw
    width: 200
    height: 150
    VTKRenderItem {
        anchors.fill: parent
        renderWindow: rw
    }
}
"""
engine2 = QQmlApplicationEngine()
engine2.loadData(QByteArray(qml_vtk), QUrl("inmemory-vtk.qml"))
if engine2.rootObjects():
    print("[OK]   VTK QML (import VTK 9.3) loaded ✅")
else:
    print("[MISS] VTK QML (import VTK 9.3) failed ❌")
    print("       If error says 'module \"VTK\" is not installed', your wheel lacks Qt Quick support.")
