import openai

class AIBrain:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if api_key:
            openai.api_key = api_key
    
    def get_response(self, message):
        """Получить ответ от AI"""
        if not self.api_key:
            return "🤖 AI режим не настроен. Настройте API ключ OpenAI."
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты помощник в ресторане."},
                    {"role": "user", "content": message}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content
        except:
            return "Извините, произошла ошибка AI."

# Создаем экземпляр AI
ai = AIBrain()