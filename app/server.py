from fastapi import FastAPI

from langserve import add_routes
from langchain_community.chat_models import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig

from langfuse.callback import CallbackHandler
from pydantic import BaseModel

from chains.pdf_rag import pdf_rag_chain
from graphs.adaptive_rag.graph import adaptive_rag

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

class ChainInput(BaseModel):
    input: str


add_routes(
    app,
    pdf_rag_chain.with_types(input_type=ChainInput).with_config(config),
    path="/chain/pdf_rag",
)


class GraphInput(BaseModel):
    question: str


add_routes(
    app,
    adaptive_rag.with_types(
        input_type=GraphInput, output_type=dict
    ).with_config(config),
    path="/graph/adaptive_rag",
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
