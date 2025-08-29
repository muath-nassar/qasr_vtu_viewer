from __future__ import annotations
from typing import List
from app.domain.ports import MeshRepository, Logger
from app.domain.errors import PathNotFound, NotVTUFile
from app.domain.types import MeshRef


class ImportMeshes:
    """List direct *.vtu files under the provided path (file or dir)."""

    def __init__(self, repo: MeshRepository, log: Logger) -> None:
        self._repo = repo
        self._log = log

    def run(self, dir_or_file_path: str) -> List[MeshRef]:
        try:
            meshes = self._repo.list_meshes_in(dir_or_file_path)
            self._log.info(f"[ImportMeshes] Found {len(meshes)} VTU files in selection")
            return meshes
        except PathNotFound as e:
            self._log.error(f"[ImportMeshes] {e}")
        except NotVTUFile as e:
            self._log.error(f"[ImportMeshes] {e}")        
        return []
