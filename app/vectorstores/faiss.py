from os.path import isfile, join, isdir

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from vectorstores.utils import load_split_docs_pypdf

def get_faiss_vector_store(path, reload=True, save_local=True):
    if isdir(join(path, "faiss_index")) and reload:
        path=join(path, "faiss_index")
        return FAISS.load_local(
            path,
            embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
            allow_dangerous_deserialization=True
        )
    
    documents=load_split_docs_pypdf(path=path)

    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small")
    )

    if save_local:
        vectorstore.save_local(join(path,"faiss_index"))

    return vectorstore