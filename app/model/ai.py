from app.model.prompt import text_2_fart_prompt
from openai import OpenAI

from app.settings.settings import settings

api_key = settings.OPENAI_API_KEY
openAiClient = OpenAI(api_key=api_key)

class AI:
    def get_fart_audios_to_user(self, text):
        response = openAiClient.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.1,
            top_p=0.0,
            messages=[
                {"role": "system", "content": text_2_fart_prompt
                },
                {"role": "user", "content": text}
            ],
        )

        if response.choices:
            message = dict(response.choices[0].message)
            answer = message.get("content")
            print("AI Response: ", answer)
            return answer
        return None
    
    def get_fitting_meme(self, text):
        response = openAiClient.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.1,
            top_p=0.0,
            messages=[
                {"role": "system", "content": text_2_fart_prompt
                },
                {"role": "user", "content": text}
            ],
        )

        if response.choices:
            message = dict(response.choices[0].message)
            answer = message.get("content")
            print("AI Response: ", answer)
            return answer
        return None