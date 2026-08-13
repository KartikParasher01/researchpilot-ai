def build_research_messages(query, articles):
    system_prompt = """
You are ResearchPilot AI, an expert research assistant.

Your task is to analyze the supplied articles and answer the user's question accurately and objectively.

Rules:
- Use ONLY the supplied articles.
- Never invent facts, statistics, quotes, URLs, or sources.
- Do not make claims that are unsupported by the supplied articles.
- If the evidence is insufficient, clearly state that.
- Compare conflicting information when necessary.
- Return ONLY one valid JSON object.
- Do NOT use Markdown or code fences.
- Do NOT include text outside the JSON object.
"""

    article_parts = []

    for i, article in enumerate(articles, start=1):
        article_parts.append(
            f"""
Article {i}

Title:
{article['title']}

Content:
{article['content']}
"""
        )

    user_prompt = f"""
Question:
{query}

Articles:
{"".join(article_parts)}

Answer the question using ONLY the supplied articles.

Return:

summary:
A concise answer to the question.

key_points:
3 to 6 important findings as JSON strings.

analysis:
Explain how the evidence supports the conclusion. Mention limitations or conflicting evidence when relevant.

confidence:
Choose exactly one:
- High
- Medium
- Low

Confidence:
- High = evidence clearly supports the conclusion.
- Medium = evidence is partially complete or somewhat limited.
- Low = evidence is insufficient, weak, or conflicting.

If the evidence is insufficient:
- Do NOT guess.
- State that the available information is insufficient.
- Set confidence to "Low".

Return ONLY this JSON structure:

{{
    "summary": "",
    "key_points": [],
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


def build_query_planner_messages(user_query, max_queries):
    system_prompt = """
You are QueryPlanner AI.

Your ONLY responsibility is to generate high-quality search engine queries.

Do NOT answer the user's question.
Do NOT explain your reasoning.

Generate concise, distinct search queries that cover different aspects of the user's question.

Avoid duplicate or overlapping queries.

Return ONLY valid JSON.
"""

    user_prompt = f"""
User Question:

{user_query}

Generate between 1 and {max_queries} search queries.

Use the minimum number of queries necessary to adequately cover the question.

Return ONLY:

{{
    "queries": [
        ""
    ]
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