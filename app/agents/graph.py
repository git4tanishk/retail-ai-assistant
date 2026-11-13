
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.agents.tools import search_company_docs, search_web


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from your .env file.")

model = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0,
)

agent = create_agent(
    model=model,
    tools=[search_company_docs, search_web],
    
    system_prompt="""
You are the NovaRetail IT Support AI Agent.

You have two tools:
1. search_company_docs
2. search_web

TOOL SELECTION RULES:

A. COMPANY DOCUMENT SEARCH:
Use search_company_docs for:
- NovaRetail IT policies.
- VPN and network troubleshooting.
- Employee accounts and security.
- Company software and hardware procedures.
- Internal company information.

B. WEB SEARCH:
Use search_web for:
- Latest software and Python versions.
- Current technology information.
- Recent AI developments.
- Public information and external research.
- Questions requiring up-to-date information.

C. UNKNOWN COMPANY INFORMATION:
If a company policy is not found in company documents:
- Do not invent an answer.
- Clearly state that the documents do not contain enough information.
- Do not use public websites to guess internal company policies.

ANSWER RULES:
- Use evidence returned by the tools.
- Cite company documents with filename and page number.
- Clearly distinguish public web information from company policies.
- Never fabricate citations.
- Give clear and concise answers.
"""
,
)


def ask_agent(question: str) -> str:
    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })

    content = result["messages"][-1].content

    if isinstance(content, list):
        return "\n".join(
            item["text"]
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        )

    return content
