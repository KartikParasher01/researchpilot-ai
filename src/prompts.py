def build_research_messages(query, articles):
    system_prompt = """
You are ResearchPilot AI, an expert research assistant.

Your mission is to analyze the supplied articles and generate an accurate, objective, and well-structured research report.

Rules:
- Use ONLY the supplied articles as your source of information.
- Never invent facts, statistics, quotes, URLs, or sources.
- Never infer information that is not directly supported by the articles.
- If the available information is insufficient, clearly state that instead of guessing.
- Be factual, unbiased, and concise.
- Return ONLY a single valid JSON object.
- Do NOT wrap the JSON inside markdown or code fences.
- Do NOT include explanations before or after the JSON.
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

Task:
Answer the user's question using ONLY the supplied articles.

Your response should:
- Directly answer the user's question.
- Summarize the relevant information.
- Highlight the most important findings.
- Compare viewpoints if multiple articles disagree.
- Mention limitations or missing information when necessary.
- Do NOT guess or hallucinate.

Field Descriptions:

summary:
- Write a concise overview that answers the user's question.

key_points:
- Return 3 to 6 important findings.
- Each item must be a JSON string.
- Do NOT use Markdown bullets (* or -).

analysis:
- Explain how the conclusion was reached.
- Mention trade-offs, limitations, or conflicting evidence if applicable.

confidence:
Choose EXACTLY one of the following values:

- High
- Medium
- Low

Confidence Guidelines:
- High: The supplied articles clearly support the conclusion.
- Medium: The evidence is partially complete or somewhat limited.
- Low: The articles contain insufficient, weak, or conflicting information.

If the supplied articles do not contain enough information:
- Do NOT guess.
- Clearly state that the available information is insufficient.
- Set confidence to "Low".

Return ONLY valid JSON using EXACTLY this schema:

{{
    "summary": "",
    "key_points": [
        ""
    ],
    "analysis": "",
    "confidence": ""
}}
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