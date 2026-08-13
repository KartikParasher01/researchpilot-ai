import logging

from openai import OpenAI

from src.config import (
    LLM_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)


logger = logging.getLogger(__name__)


class LLMClient:

    def __init__(self):
        self.api_key = LLM_API_KEY
        self.model = LLM_MODEL
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    def generate(self, messages):
        """Generate a response from the LLM."""

        try:
            response = self.call_model(messages)

            return response.choices[0].message.content

        except Exception:
            logger.exception("LLM request failed")
            return None

    def call_model(self, messages):
        """Send messages to the Groq API."""

        logger.info("Calling Groq API")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        return response