import json
import logging
from typing import Any, Dict

from httpx import AsyncClient, HTTPStatusError, TimeoutException

from settings import Settings


class AskService:
    def __init__(self):
        self.url = Settings.load().url
        self.client = AsyncClient(timeout=30.0)

    async def send(self, data: Dict[str, Any]) -> str:
        try:
            async with self.client as client:
                response = await client.post(
                    self.url, json=data, headers={"Content-Type": "application/json"}
                )

                response.raise_for_status()
                return json.dumps(response.json(), indent=2, ensure_ascii=False)

        except TimeoutException:
            logging.error("Timeout при обращении к API")
            raise Exception("Превышено время ожидания ответа от сервера")

        except HTTPStatusError as e:
            logging.error(f"HTTP ошибка: {e.response.status_code}")
            raise Exception(f"Ошибка API: {e.response.status_code}")

        except Exception as e:
            logging.error(f"Ошибка при обращении к API: {e}")
            raise Exception("Произошла ошибка при обращении к API")
