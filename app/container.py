from __future__ import annotations
from dependency_injector import containers, providers
from app.application.fit_view_all import FitViewAll
from app.application.load_mesh import LoadMesh
from app.application.set_visibility import SetVisibility
from app.data.loggers import StdoutLogger
from app.data.fs_repo import LocalMeshRepository
from app.application.import_meshes import ImportMeshes
from app.presentation.main_vm import MainViewModel
from app.vtk_adapters.reader import VTKMeshReader
from app.vtk_adapters.scene import VTKScene


class AppContainer(containers.DeclarativeContainer):
    """DI container assembling adapters, use-cases, and VMs."""
    wiring_config = containers.WiringConfiguration(packages=["app"])

    # Adapters
    logger = providers.Singleton(StdoutLogger)
    repo = providers.Factory(LocalMeshRepository)
    # --- VTK 
    scene = providers.Singleton(VTKScene, log=logger)
    mesh_reader = providers.Singleton(VTKMeshReader, log=logger)

    # Use-cases
    import_meshes = providers.Factory(ImportMeshes, repo=repo, log=logger)
    load_mesh = providers.Factory(LoadMesh, reader=mesh_reader , scene=scene, log=logger)
    set_visibility = providers.Factory(SetVisibility, scene=scene, log=logger)
    fit_view_all = providers.Factory(FitViewAll, scene=scene, log=logger)

    # ViewModels
    main_vm = providers.Singleton(
        MainViewModel,
        import_meshes=import_meshes,
        load_mesh=load_mesh,
        set_visibility=set_visibility,
        fit_view_all=fit_view_all
    )
