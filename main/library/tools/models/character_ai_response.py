from main.library.utils.models.custom_dict import CustomDict
import pytz


class CharacterAiResponse:
    def __init__(self, char_response: dict):
        response_custom_dict = CustomDict.build_recursivelly(char_response)
        brazilia_timezone = pytz.timezone("America/Sao_Paulo")
        self.created_at = response_custom_dict.create_time.astimezone(brazilia_timezone).strftime("%d/%m/%Y %H:%M:%S")
        self.session = CustomDict(
            {
                "chat_id": response_custom_dict.turn_key.chat_id,
                "turn_id": response_custom_dict.turn_key.turn_id,
            }
        )
        self.character = CustomDict(
            {
                "id": response_custom_dict.author.author_id,
                "name": response_custom_dict.author.name,
            }
        )
        self.candidates = [
            CustomDict(
                {
                    "candidate_id": candidate.candidate_id,
                    "message": candidate.raw_content,
                }
            )
            for candidate in response_custom_dict.candidates
        ]
        self.primary_candidate_id = response_custom_dict.primary_candidate_id
