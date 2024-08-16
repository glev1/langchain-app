from fastapi import FastAPI

from langserve import add_routes
from langchain_community.chat_models import ChatOpenAI
from langchain_core.runnables.config import RunnableConfig

from langfuse.callback import CallbackHandler
from pydantic import BaseModel

from chains.pdf_rag import pdf_rag_chain
from graphs.adaptative_rag.graph import adaptative_rag

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

<<<<<<< HEAD
<<<<<<< HEAD

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
    adaptative_rag.with_types(
        input_type=GraphInput, output_type=dict
    ).with_config(config),
    path="/graph/adaptative_rag",
=======
=======
>>>>>>> adaptative-rag
class Input(BaseModel):
    input: str
    
add_routes(
    app,
    pdf_rag_chain.with_types(input_type=Input).with_config(config),
    path="/pdf_rag",
<<<<<<< HEAD
>>>>>>> 6994aee (feat: RAG chain with PDF loader and FAISS)
=======
>>>>>>> adaptative-rag
)


if __name__ == "__main__":
    import uvicorn

<<<<<<< HEAD
<<<<<<< HEAD
    uvicorn.run(app, host="localhost", port=8000)
=======
    uvicorn.run(app, host="localhost", port=8000)
>>>>>>> 6994aee (feat: RAG chain with PDF loader and FAISS)
=======
    uvicorn.run(app, host="localhost", port=8000)
>>>>>>> adaptative-rag
