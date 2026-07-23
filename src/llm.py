from openai import OpenAI
import logging
import json
from src.config import (LLM_API_KEY,LLM_MODEL,TEMPERATURE,MAX_TOKENS,)
from src.prompts import build_research_messages
from src.models import ResearchResponse
from pydantic import ValidationError
logger = logging.getLogger(__name__)



class LLMClient:

    def __init__(self):

        self.api_key = LLM_API_KEY
        self.model = LLM_MODEL
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        ) 



    def summarize(self, query, articles):
        messages = build_research_messages(query, articles)

        try:
            response = self.call_model(messages)
        except Exception:
            logger.exception("LLM request failed")
            return None

        result = self.parse_response(response)

        if result is None:
            return None

        result["sources"] = articles

        return result


    def call_model(self, messages):
        logger.info("Calling Groq API")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response

        except Exception:
            logger.exception("API request failed")
            raise

            
    def parse_response(self, response):
        content = response.choices[0].message.content

        try:
            data = json.loads(content)
            result = ResearchResponse.model_validate(data)

            return result.model_dump()

        except json.JSONDecodeError:
            logger.exception("LLM returned invalid JSON")
            return None

        except ValidationError:
            logger.exception("LLM response did not match schema")
            return None
                
    # def parse_response(self, response):
    #     content = response.choices[0].message.content

    #     print("=" * 80)
    #     print(content)
    #     print("=" * 80)

    #     data = json.loads(content)
    #     return ResearchResponse.model_validate(data)