import logging

from dotenv import load_dotenv
from openai import AsyncOpenAI
import os

load_dotenv()

vin_recognition = """
VIN-Validator (Strict AI Pipeline Mode)
1. Поиск VIN-кандидатов (а не случайного текста):
Ищем только строки длиной 17 символов (остальное игнорируем на первом этапе).
Если таких строк несколько → анализируем каждую и выбираем ту, что наиболее похожа на VIN (проверка паттернов: WMI, VDS, VIS).

2. Strict Confidence Calculation (новый подход):
Confidence = MIN(Confidence всех символов). Пример:
Если 16 символов с Confidence=100%, а 1 символ с Confidence=94% → общий Confidence=94% → LowQuality.

Пороги:
95-99% — требуется ручная проверка (возвращаем LowQuality).
<80% — отказ (LowQuality).

3. Жесткая проверка символов (никаких "может быть"):
Запрещенные символы (I, O, Q) → сразу InvalidChar.
Автозамена разрешена ТОЛЬКО если Confidence=100%:
I → 1 (если 100% уверен, что это не J или L).
O → 0 (если 100% уверен, что это не D или Q).
Q → всегда ошибка (никаких замен).
Перепроверяй S и 5. Не путай

4. Проверка ориентации:
Если текст перевернут (>15°) → NeedsRotation:[град]°.
Если поворот <15° → пытаемся распознать, но Confidence автоматически снижается на 5%.

5. Фильтрация ложных срабатываний:
Если строка не соответствует паттерну VIN (например, случайные цифры) → NoVIN.
Если символов меньше 17 → NoVIN (даже если часть видна).

📜 Формат ответа (без изменений — нарушение = ошибка)
Ты должен выдать только распознанный VIN. Много текста запрещается
✅ VIN: ```[17 символов]``` Confidence:95%

❌ Ошибки (в порядке приоритета):
InvalidChar:[символ]@[позиция]
LowQuality (если Confidence <95%)
NeedsRotation:[град]°
NoVIN
"""


class AIManager:
    def __init__(self, api_key):
        logging.basicConfig(level=logging.INFO)
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )

    async def recognize_vin(self, image_url) -> str:
        """Пытается распознать VIN. Предполагаемый VIN будет возвращен и далее пройдет валидацию"""
        completion = await self.client.chat.completions.create(
            model="qwen-vl-max",
            messages=[
                {
                    "role": "user", "content": [
                    {"type": "text", "text": vin_recognition},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url}
                    }
                ],
                }]
        )
        supposed_vin = completion.model_dump()['choices'][0]['message'].get('content')
        logging.info(f'Распознанный vin: {supposed_vin}')

        return supposed_vin

ai = AIManager(os.getenv('DASHSCOPE_API_KEY'))
