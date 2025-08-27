from __future__ import annotations

from pathlib import Path
from typing import List, Sequence, Optional

from app.domain.ports import MeshRepository, Logger
from app.domain.types import MeshRef
from app.domain.errors import PathNotFound, NotVTUFile


class LocalMeshRepository(MeshRepository):
    """Discover *.vtu files for a given path (file or directory).

    - If `path` is a file:
        * return [path] if it ends with .vtu (case-insensitive)
        * otherwise raise NotVTUFile(path)
    - If `path` is a directory:
        * return direct children ending with .vtu (non-recursive)
        * ignore non-vtu files, do not raise
    - If `path` doesn't exist: raise PathNotFound(path)
    """


    def list_meshes_in(self, path: str) -> Sequence[MeshRef]:
        base = Path(path).expanduser()
        base = base if base.is_absolute() else base.resolve()

        if not base.exists():
            raise PathNotFound(str(base))

        # File case
        if base.is_file():
            if base.suffix.lower() == ".vtu":
                return [MeshRef(str(base))]
            raise NotVTUFile(str(base))

        # Directory case (non-recursive direct children)
        if base.is_dir():
            meshes: List[MeshRef] = []
            for entry in sorted(base.iterdir()):
                if entry.is_file() and entry.suffix.lower() == ".vtu":
                    meshes.append(MeshRef(str(entry.resolve())))
            return meshes

        # Neither file nor directory (rare)
        return []
