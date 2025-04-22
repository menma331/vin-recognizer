import logging

from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
import mimetypes
import base64
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

    import base64
    import mimetypes
    import os
    from typing import Union

    async def recognize_vin(self, image_source: Union[str, bytes]) -> str:
        """Пытается распознать VIN. Работает как с URL, так и с локальными файлами.

        Args:
            image_source: Может быть:
                - URL изображения в интернете (начинается с http:// или https://)
                - Путь к локальному файлу
                - Байты содержимого изображения

        Returns:
            Предполагаемый VIN
        """
        if isinstance(image_source, bytes):
            # Если переданы байты изображения
            image_content = image_source
        elif image_source.startswith(('http://', 'https://')):
            # Если это URL - используем старый формат
            completion = await self.client.chat.completions.create(
                model="qwen-vl-max",
                messages=[
                    {
                        "role": "user", "content": [
                        {"type": "text", "text": vin_recognition},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_source}
                        }
                    ],
                    }]
            )
        else:
            # Локальный файл - читаем и кодируем в base64
            if not os.path.exists(image_source):
                raise FileNotFoundError(f"Файл не найден: {image_source}")

            # Определяем MIME тип
            mime_type, _ = mimetypes.guess_type(image_source)
            if mime_type is None:
                mime_type = 'application/octet-stream'

            with open(image_source, 'rb') as image_file:
                image_content = image_file.read()

            base64_image = base64.b64encode(image_content).decode('utf-8')
            data_url = f"data:{mime_type};base64,{base64_image}"

            completion = await self.client.chat.completions.create(
                model="qwen-vl-max",
                messages=[
                    {
                        "role": "user", "content": [
                        {"type": "text", "text": vin_recognition},
                        {
                            "type": "image_url",
                            "image_url": {"url": data_url}
                        }
                    ],
                    }]
            )

        supposed_vin = completion.model_dump()['choices'][0]['message'].get('content')
        logging.info(f'Распознанный vin: {supposed_vin}')

        return supposed_vin
ai = AIManager(os.getenv('DASHSCOPE_API_KEY'))
