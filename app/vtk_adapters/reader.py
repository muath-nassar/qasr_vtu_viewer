"""
This class is designed to read a VTU file and return vtkUnStructeredGrid
"""
from app.domain.ports import MeshReader
import vtk


class VTKMeshReader(MeshReader):
    def read_vtu(self, path: str) -> vtk.vtkUnstructuredGrid:
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(path)
        reader.Update()  # Force reading the file
        output = reader.GetOutput()
        if output is None or output.GetNumberOfPoints() == 0:
            raise RuntimeError(f"VTKMeshReader Failed to read VTU file: {path}")
        return output
