from back.config import TAVILY_API_KEY
from tavily import TavilyClient

_tavily_client = None

def get_tavily_client():
    global _tavily_client
    if _tavily_client is None:
        _tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    return _tavily_client
