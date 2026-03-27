from app.core.config import settings
from langchain_openai import AzureChatOpenAI
from app.schemas.digest.filter_response import DigestFilterResponse
from langchain_core.prompts import ChatPromptTemplate
from app.core.app_constants import AppConstants

chat_llm = AzureChatOpenAI(
    model=settings.AZURE_CHAT_MODEL,
    api_key=settings.AZURE_OPENAI_API_KEY,
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    api_version=settings.AZURE_OPENAI_VERSION,
    max_retries=2,
)

digest_filter_llm = chat_llm.with_structured_output(DigestFilterResponse)


DIGEST_FILTER_PROMPT = ChatPromptTemplate([
    ("system", AppConstants.DIGEST_FILTER_SYS_PROMPT),
    ("human", "Title: {title}\nContent: {content}\n\nDecision (ReadyToTake/Ignore):")
])

digest_filter_chain = DIGEST_FILTER_PROMPT | digest_filter_llm

async def filter_digest(title: str, content: str) -> str:
    response = await digest_filter_chain.ainvoke({
        "title": title,
        "content": content
    })
    return response.decision