from __future__ import annotations
from typing import List
from app.domain.ports import MeshRepository, Logger
from app.domain.errors import PathNotFound, NotVTUFile


class ImportMeshes:
    """List direct *.vtu files under the provided path (file or dir)."""

    def __init__(self, repo: MeshRepository, log: Logger) -> None:
        self._repo = repo
        self._log = log

    def run(self, dir_or_file_path: str) -> List[str]:
        try:
            meshes = self._repo.list_meshes_in(dir_or_file_path)
        except PathNotFound as e:
            self._log.error(f"[UseCase] {e}")
            return []
        except NotVTUFile as e:
            self._log.error(f"[UseCase] {e}")
            return []
        names = [m.path for m in meshes]
        self._log.info(f"[UseCase] Found {len(names)} VTU files in selection")
        return names
