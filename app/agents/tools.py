
from langchain_core.tools import tool
from app.retrieval.vector_store import search_chunks


@tool
def search_company_docs(question: str) -> str:
    """Search NovaRetail company documents for IT support instructions,
    troubleshooting steps, and company policies."""

    results = search_chunks(question)

    if not results:
        return "No relevant information was found in the company documents."

    formatted_results = []

    for item in results:
        formatted_results.append(
            f"Source: {item['source']}, Page: {item['page']}\n"
            f"{item['text']}"
        )

    return "\n\n".join(formatted_results)


@tool
def search_web(query: str) -> str:
    """Search the public web for current information when company documents
    are insufficient or external information is needed."""

    from langchain_community.tools.tavily_search import TavilySearchResults

    search_tool = TavilySearchResults(max_results=3)
    results = search_tool.invoke({"query": query})

    if not results:
        return "No web search results were found."

    return str(results)
