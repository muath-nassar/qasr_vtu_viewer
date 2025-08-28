from app.domain.ports import MeshScene, Logger

class SetVisibility:
    """Set visibility for a single mesh."""
    def __init__(self, scene: MeshScene, log: Logger) -> None:
        self._scene, self._log = scene, log

    def run(self, mesh_id: str, visible: bool) -> None:
        self._scene.set_visible(mesh_id, visible)
        self._log.debug(f"[SetVisibility] {mesh_id=} {visible=}")
