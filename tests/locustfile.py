import os
import time
import typing as t
import random as rd

from locust import HttpUser, task

QUESTIONS_PER_SESSION = 10
NEURO_TOKEN = os.environ["NEURO_TOKEN"]


class LLMUser(HttpUser):
    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {NEURO_TOKEN}",
            "Content-Type": "application/json",
        }
    
    @task
    def ask_chat(self) -> None:
        models = self.client.get("/v1/models", headers=self.headers).json()["data"]
        for model_info in models:
            model_name = model_info["id"]
            for _ in range(QUESTIONS_PER_SESSION):
                self.client.post(
                    "/v1/chat/completions",
                    json=self.chat_prompt(model_name),
                    headers=self.headers,
                )
                time.sleep(rd.randint(20, 60))

    @task
    def ask_completions(self) -> None:
        models = self.client.get("/v1/models", headers=self.headers).json()["data"]
        for model_info in models:
            model_name = model_info["id"]
            for _ in range(QUESTIONS_PER_SESSION):
                self.client.post(
                    "/v1/completions",
                    json=self.completions_prompt(
                        model_name,
                        tokens=rd.randint(40, 100),
                        temp=rd.randint(1, 9) / 10,
                    ),
                    headers=self.headers,
                )
                time.sleep(rd.randint(1, 5))

    
    def completions_prompt(self, model_name: str, tokens: int, temp: float) -> dict[str, t.Any]:
        return {
            "model": model_name,
            "prompt": "Once upon a time",
            "max_tokens": tokens,
            "temperature": temp,
        }
        

    def chat_prompt(self, model_name: str) -> dict[str, t.Any]:
        return {
            "model": model_name,
            "messages": [{"role": "user", "content": "Hello! What is your name?"}],
        }
