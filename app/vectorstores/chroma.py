from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from vectorstores.utils import load_split_docs_pypdf


def get_chroma_vector_store(path):
    documents=load_split_docs_pypdf(path=path)
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small")
    )

    return vectorstore