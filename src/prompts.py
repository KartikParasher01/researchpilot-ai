def build_research_messages(query, articles):
    system_prompt = """
You are ResearchPilot AI.

You are an expert research assistant.

Use ONLY the supplied articles.

Never invent information.

Never invent sources.

Return ONLY one valid JSON object.

Do not wrap the JSON in markdown.

Do not include explanations before or after the JSON.
"""

    article_parts = []

    for i, article in enumerate(articles, start=1):
        article_parts.append(f"""
Article {i}

Title:
{article['title']}

Content:
{article['content']}
""")

    user_prompt = f"""
Question:
{query}

Articles:
{"".join(article_parts)}

Instructions:
- Return ONLY valid JSON in this format:
{{
    "summary": "",
    "key_points": [],
    "analysis": "",
    "sources": [
        {{
            "title": "",
            "url": ""
        }}
    ],
    "confidence": ""
}}
- Remove duplicates.
- Use bullet points.
"""

    return [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]