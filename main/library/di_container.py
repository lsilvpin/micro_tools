from dependency_injector import providers, containers
from main.library.tools.core.log_tool import LogTool


class Container(containers.DeclarativeContainer):
    """
    Container class for dependency injection.

    This class extends the `containers.DeclarativeContainer` class from the `dependency_injector` module.
    It provides instances for each services of the system.
    """
    log_tool = providers.Factory(LogTool)

    wiring_config = containers.WiringConfiguration(
        modules=[
            "main.entrypoint.controllers.main_controller",
        ]
    )