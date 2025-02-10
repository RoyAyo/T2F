from openai import OpenAI

api_key = ""
openAiClient = OpenAI(api_key=api_key)

from app.model.prompt import text_2_fart_prompt

class AI:
    def get_fart_audios_to_user(text):
            response = openAiClient.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": text_2_fart_prompt
                    },
                    {"role": "user", "content": text}
                ],
            )

            if response.choices:
                message = dict(response.choices[0].message)
                answer = message.get("content")
                print(answer)
                return answer
            return None