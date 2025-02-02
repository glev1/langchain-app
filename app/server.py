import httpx
from fastapi import FastAPI

from langserve import add_routes
from langchain_community.chat_models import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig

from langfuse.callback import CallbackHandler

from chains.base.pydantic_models.chain import ChainInput
from chains.base.pydantic_models.graph import GraphInput
from chains.pdf_rag import pdf_rag_chain

from graphs.adaptive_rag.graph import adaptive_rag

from dotenv import load_dotenv

load_dotenv()


try:
    langfuse_handler = CallbackHandler()
    langfuse_handler.auth_check()
    config = RunnableConfig(callbacks=[langfuse_handler])
except httpx.ConnectError:
    config = RunnableConfig(callbacks=[])

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

# add_routes(
#     app,
#     ChatOpenAI(model="gpt-4o-mini").with_config(config),
#     path="/openai",
# )


add_routes(
    app,
    pdf_rag_chain.with_types(input_type=ChainInput).with_config(config),
    path="/chain/pdf_rag",
)


# @app.post("/chain/pdf_rag")
# async def handle_query(query: str):
#     """
#     TBD
#     """
#     # Process the input through the RAG chain
#     result = pdf_rag_chain.invoke(query)

#     return {"response": result}


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
