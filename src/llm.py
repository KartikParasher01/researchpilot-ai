from openai import OpenAI

from src.config import (
    LLM_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)

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

        prompt = self.build_prompt(query, articles)

        response = self.call_model(prompt)

        summary = self.parse_response(response)

        return summary


    def build_prompt(self, query, articles):
        """
        Builds the prompt that will be sent to the LLM.
        """
        parts = []

        parts.append("You are an expert AI Research Assistant.")
        parts.append(f"User Query:\n{query}")

        for i, article in enumerate(articles, start=1):
            parts.append(f"""
        Article {i}

        Title:
        {article['title']}

        Content:
        {article['content']}
        """)

        parts.append("""
        Instructions:
        - Summarize the articles.
        - Remove duplicates.
        - Use bullet points.
        """)

        prompt = "\n".join(parts)

        return prompt

       

    def call_model(self, prompt):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        return response
    
    def parse_response(self, response):
        return response.choices[0].message.content