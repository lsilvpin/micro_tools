from dependency_injector import providers, containers
from main.library.repositories.notion.core.notion_block_manager import (
    NotionBlockManager,
)
from main.library.repositories.notion.core.notion_database_manager import (
    NotionDatabaseManager,
)
from main.library.repositories.notion.core.notion_page_manager import NotionPageManager
from main.library.repositories.notion.core.notion_searcher import NotionSearcher
from main.library.tools.core.character_ai_tool import CharacterAiTool
from main.library.tools.core.http_client_tool import HttpClientTool
from main.library.tools.core.log_tool import LogTool
from main.library.tools.core.settings_tool import SettingsTool


class Container(containers.DeclarativeContainer):
    """
    Container class for dependency injection.

    This class extends the `containers.DeclarativeContainer` class from the `dependency_injector` module.
    It provides instances for each services of the system.
    """

    log_tool = providers.Factory(LogTool)
    settings_tool = providers.Factory(SettingsTool)
    http_client_tool = providers.Factory(
        HttpClientTool, settings_tool=settings_tool, log_tool=log_tool
    )

    notion_block_manager = providers.Factory(
        NotionBlockManager, settings_tool=settings_tool, log_tool=log_tool
    )
    notion_page_manager = providers.Factory(
        NotionPageManager,
        settings_tool=settings_tool,
        log_tool=log_tool,
        notion_block_manager=notion_block_manager,
    )
    notion_database_manager = providers.Factory(
        NotionDatabaseManager,
        settings_tool=settings_tool,
        log_tool=log_tool,
    )
    notion_searcher = providers.Factory(
        NotionSearcher,
        settings_tool=settings_tool,
        log_tool=log_tool,
    )
    character_ai_tool = providers.Factory(
        CharacterAiTool,
        settings_tool=settings_tool,
        log_tool=log_tool,
    )

    wiring_config = containers.WiringConfiguration(
        modules=[
            "main.entrypoint.controllers.main_controller",
            "main.entrypoint.controllers.notion.notion_page_manager_controller",
            "main.entrypoint.controllers.notion.notion_database_manager_controller",
            "main.entrypoint.controllers.notion.notion_searcher_controller",
            "main.entrypoint.controllers.character_ai_controller",
        ]
    )
