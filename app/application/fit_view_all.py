from app.domain.ports import MeshScene, Logger

class FitViewAll:
    """Fit camera to all currently visible meshes."""
    def __init__(self, scene: MeshScene, log: Logger) -> None:
        self._scene, self._log = scene, log

    def run(self) -> None:
        self._scene.fit_visible()
        self._log.info("[FitViewAll] camera fit to visible")
