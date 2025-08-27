from dataclasses import dataclass
@dataclass(frozen=True)
class MeshRef:
    path: str
    name: str