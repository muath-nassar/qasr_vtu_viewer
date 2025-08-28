"""
This class handles the 3D visualization of the mesh.
"""
from typing import Any, Dict, Tuple
import itertools
from uuid import uuid4
from app.domain.ports import MeshScene, Logger
import vtk


class VTKScene(MeshScene):
    """
    Owns the renderer and manages mesh actors by id"""
    def __init__(self, log: Logger):
        self._log = log
        self._renderer = vtk.vtkRenderer()
        self._render_window : vtk.vtkRenderWindow | None = None # ---this will be attached later
        self._actors: Dict[str, vtk.vtkActor] = {}

        # background to match app theme
        self._renderer.SetBackground(0.12, 0.12, 0.14) # color is dark

        # simple disrtinct color cycles 
        self.color_cycle = itertools.cycle([
            (0.85, 0.35, 0.35),  # red-ish
            (0.35, 0.65, 0.90),  # blue-ish
            (0.40, 0.80, 0.55),  # green-ish
            (0.90, 0.75, 0.35),  # yellow-ish
            (0.75, 0.45, 0.90),  # purple-ish
        ])

    

    def _render(self) -> None:
        """
        Render the scene.
        """
        if self._render_window is not None:
            self._render_window.Render()
    # --------- integration hook ---------
    def attach_render_window(self, rw: vtk.vtkRenderWindow) -> None:
        """
        Attach the VTK render window to this scene.
        This method is called from the VM
        """
        self._render_window = rw
        self._render_window.AddRenderer(self._renderer)
        self._render()

    # --------- MeshScene API -------------

    def add_dataset(self, dataset: Any, name: str) -> str:
        """
        Add a dataset to the scene. create mapper/actor 
        returns mesh_id
        """
        # Mapper
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(dataset)

        # Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        r, g, b = next(self.color_cycle)
        actor.GetProperty().SetColor(r, g, b)
        actor.GetProperty().SetOpacity(1.0)  # fully opaque
        actor.GetProperty().SetEdgeVisibilityOff()  # no edges
        actor.SetVisibility(1)

        self._renderer.AddActor(actor)  # visible by default

        # Unique mesh ID
        mesh_id = str(uuid4())
        self._actors[mesh_id] = actor

        self._log.info(f"[VTKScene] add_dataset: {name} -> {mesh_id}")
        self._reset_camera_if_first()
        self._render()

        return mesh_id

    def set_visible(self, mesh_id: str, on: bool) -> None:
        actor = self._actors.get(mesh_id)
        if actor:
            actor.SetVisibility(on)
            self._render()

    def reset_camera(self) -> None:
        self._renderer.ResetCamera()
        self._render()

    def fit_visible(self) -> None:
        bounds = self._visible_bounds()
        if bounds is None:
            self._log.info("[VTKScene] fit_visible: no visible actors")
            return
        self._renderer.ResetCamera(bounds)
        self._render()
    
    # --------- internal methods -------------

    def _reset_camera_if_first(self) -> None:
        """
        Reset the camera if this is the first actor added.
        """
        if len(self._actors) == 1:
            self._renderer.ResetCamera()

    def _visible_bounds(self) -> Tuple[float, float, float, float, float, float] | None:
        """
        Loops over all actors.
        Skips invisible ones (visibility == 0).
        Gets each actor’s 3D bounding box (xmin, xmax, ymin, ymax, zmin, zmax).
        Expands an aggregate bounding box to include all visible ones.
        Result: returns one bounding box that contains all visible actors. Returns None if no visible actors exist.

        Why:
        Used to reset the camera to “fit all visible meshes” only.
        Without this, ResetCamera() would zoom to everything ever added (even hidden ones).
        With it, you get a tighter, more accurate view for the current visible set.
        """
        first = True
        agg = [0.0] * 6
        for actor in self._actors.values():
            if actor.GetVisibility() == 0:
                continue
            b = [0.0] * 6
            actor.GetBounds(b)
            if first:
                agg[:] = b[:]
                first = False
            else:
                agg[0] = min(agg[0], b[0])
                agg[1] = max(agg[1], b[1])
                agg[2] = min(agg[2], b[2])
                agg[3] = max(agg[3], b[3])
                agg[4] = min(agg[4], b[4])
                agg[5] = max(agg[5], b[5])
        return None if first else tuple(agg)