from app.domain.ports import MeshReader, MeshScene, Logger

class LoadMesh:
    """Load a VTU from disk and add it to the scene; returns mesh_id."""
    def __init__(self, reader: MeshReader, scene: MeshScene, log: Logger) -> None:
        self._reader, self._scene, self._log = reader, scene, log

    def run(self, path: str, name: str) -> str:
        ds = self._reader.read_vtu(path)
        mesh_id = self._scene.add_dataset(ds, name)
        self._log.info(f"[LoadMesh] added {name}")
        return mesh_id
