from typing import List

from pydantic import BaseModel
from app.data_model.expressions import Expressions
from app.model.prompt import text_2_fart_prompt, express_text_prompt
from openai import OpenAI

from app.settings.settings import settings

api_key = settings.OPENAI_API_KEY
openAiClient = OpenAI(api_key=api_key)

class ExpressionsResponse(BaseModel):
    expressions: List[Expressions]

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
    
    def sentiment_analysis(self, text):
        response = openAiClient.beta.chat.completions.parse(
            model="gpt-4o-mini",
            temperature=0.1,
            top_p=0.0,
            messages=[
                {"role": "system", "content": express_text_prompt
                },
                {"role": "user", "content": text}
            ],
            response_format=ExpressionsResponse,
        )

        print(response)

        if response.choices:
            message = dict(response.choices[0].message.parsed)
            print(message)
            return message
        return None