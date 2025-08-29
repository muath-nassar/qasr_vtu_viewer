"""
This class is designed to read a VTU file and return vtkUnStructeredGrid
"""
from app.domain.ports import Logger, MeshReader
import vtk


class VTKMeshReader(MeshReader):
    def __init__(self, logg: Logger):
        self._log = logg

    def read_vtu(self, path: str) -> vtk.vtkUnstructuredGrid:
        self._log.info(f"[VTKMeshReader] reading VTU file: {path}")
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(path)
        reader.Update()  # Force reading the file
        output = reader.GetOutput()
        if output is None or output.GetNumberOfPoints() == 0:
            raise RuntimeError(f"VTKMeshReader Failed to read VTU file: {path}")
        return output
