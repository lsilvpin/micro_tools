import os, sys

from main.library.tools.models.character_ai_response import CharacterAiResponse

sys.path.insert(0, os.path.abspath("."))
from main.library.tools.core.log_tool import LogTool
from main.library.tools.core.settings_tool import SettingsTool
from characterai import aiocai, sendCode, authUser


class CharacterAiTool:
    def __init__(self, settings_tool: SettingsTool, log_tool: LogTool):
        self.settings_tool = settings_tool
        self.log_tool = log_tool

    def generate_token(self):
        self.log_tool.info("Generating token ...")
        email: str = input("Enter your email: ")
        code: str = sendCode(email)
        self.log_tool.info(f"Code sent to {email}: {code}")
        link: str = input("Enter the link from the e-mail: ")
        token: str = authUser(link, email)
        self.log_tool.info(f"Token generated: {token}")
        return token

    async def chat(
        self, token: str, char_id: str, message: str, chat_id: str | None = None
    ) -> CharacterAiResponse:
        assert token is not None, "Token is required"
        assert char_id is not None, "Character ID is required"
        assert message is not None, "Message is required"
        self.log_tool.info(f"Sending message {message} to character {char_id} ...")
        client = aiocai.Client(token)
        me = await client.get_me()
        char_ai_response: CharacterAiResponse | None = None
        async with await client.connect() as chat:
            if chat_id is None:
                new_chat = await chat.new_chat(char_id, me.id)
                new, answer = new_chat[0], new_chat[1]
                self.log_tool.info(f"{answer.name}: {answer.text}")
                char_response = await chat.send_message(char_id, new.chat_id, message)
                self.log_tool.info(f"{char_response.name}: {char_response.text}")
                char_ai_response = CharacterAiResponse(char_response)
                return char_ai_response
            else:
                char_response = await chat.send_message(char_id, chat_id, message)
                self.log_tool.info(f"{char_response.name}: {char_response.text}")
                char_ai_response = CharacterAiResponse(char_response)
                return char_ai_response


# Uncomment the following lines to generate a token and chat with a character
if __name__ == "__main__":
    settings_tool = SettingsTool()
    log_tool = LogTool()
    character_ai_tool = CharacterAiTool(settings_tool, log_tool)
    character_ai_tool.generate_token()
