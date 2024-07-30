from fastapi import FastAPI

from langserve import add_routes
from langchain_community.chat_models import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig

from langfuse.callback import CallbackHandler
from pydantic import BaseModel

from chains.pdf_rag import pdf_rag_chain

from dotenv import load_dotenv
load_dotenv()

langfuse_handler = CallbackHandler()
langfuse_handler.auth_check()
config = RunnableConfig(callbacks=[langfuse_handler])

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

add_routes(
    app,
    ChatOpenAI(model="gpt-4o-mini").with_config(config),
    path="/openai",
)

class Input(BaseModel):
    input: str
    
add_routes(
    app,
    pdf_rag_chain.with_types(input_type=Input).with_config(config),
    path="/pdf_rag",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)