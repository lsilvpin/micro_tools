import sys, os, pytest
import characterai.aiocai

from main.library.tools.core.character_ai_tool import CharacterAiTool

sys.path.insert(0, os.path.abspath("."))
from main.library.di_container import Container
from main.library.tools.core.log_tool import LogTool

container: Container = Container()
character_ai_tool: CharacterAiTool = container.character_ai_tool()


@pytest.mark.asyncio
async def test_should_chat_with_character(mocker):
    # Samples
    token: str = ""
    response_sample: dict = {
        "id": "7IA8Bw3NsyjruZH-8gLLKqzo3UdZ_2QBvqrCBlS0__U",
        "name": "Character",
        "text": "Olá eu sou o chat gpt",
    }

    # Mocks
    mocker.patch.object(characterai.aiocai, "Client")
    client_mock = mocker.MagicMock()
    characterai.aiocai.Client.return_value = client_mock
    me_mock = mocker.Mock()
    client_mock.get_me = mocker.AsyncMock(return_value=me_mock)
    
    async with mocker.AsyncMock() as chat_mock:
        new_mock = mocker.Mock()
        answer_mock = mocker.Mock()
        chat_mock.new_chat = mocker.AsyncMock(return_value=(new_mock, answer_mock))
        response_text = response_sample["text"]
        chat_mock.send_message = mocker.AsyncMock(return_value=response_text)
        client_mock.connect = mocker.AsyncMock(return_value=chat_mock)
    
    # Arrange
    token: str = "token"
    char_id: str = "char_id"
    message: str = "Olá, com que eu falo?"

    # Act
    response: str = await character_ai_tool.chat(token, char_id, message)

    # Assert
    assert response is not None
