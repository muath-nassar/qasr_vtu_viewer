from __future__ import annotations
from dependency_injector import containers, providers
from app.data.loggers import StdoutLogger
from app.data.fs_repo import LocalMeshRepository
from app.application.import_meshes import ImportMeshes
from app.presentation.main_vm import MainViewModel


class AppContainer(containers.DeclarativeContainer):
    """DI container assembling adapters, use-cases, and VMs."""
    wiring_config = containers.WiringConfiguration(packages=["app"])

    # Adapters
    logger = providers.Singleton(StdoutLogger)
    repo = providers.Factory(LocalMeshRepository)

    # Use-cases
    import_meshes = providers.Factory(ImportMeshes, repo=repo, log=logger)

    # ViewModels
    main_vm = providers.Factory(MainViewModel, import_meshes=import_meshes)
