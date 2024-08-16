from os.path import join, isdir

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from vectorstores.utils import load_split_docs_pypdf


def get_faiss_vector_store(path, reload=True, save_local=True):
    """
    Retrieves or creates a FAISS vector store for document embeddings.

    This function first checks if a FAISS index exists at the specified path and,
    if it does and `reload` is set to `True`, loads the existing index. If the index
    does not exist or `reload` is set to `False`, it creates a new FAISS vector store
    from the documents located at the specified path using OpenAI's embeddings.

    Args:
        path (str): The path where the FAISS index is stored or where documents are located.
        reload (bool, optional): Whether to reload an existing FAISS index if it exists. Defaults to True.
        save_local (bool, optional): Whether to save the newly created FAISS index to the local path. Defaults to True.

    Returns:
        FAISS: An instance of the FAISS vector store containing document embeddings.
    """
    if isdir(join(path, "faiss_index")) and reload:
        path = join(path, "faiss_index")
        return FAISS.load_local(
            path,
            embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
            allow_dangerous_deserialization=True,
        )

    documents = load_split_docs_pypdf(path=path)

    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    )

    if save_local:
        vectorstore.save_local(join(path, "faiss_index"))

    return vectorstore
