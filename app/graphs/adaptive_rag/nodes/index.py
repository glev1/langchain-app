from os import listdir
from os.path import isfile, join, isdir
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
    TextLoader,
)

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()


def generate_loader(path: str):
    """
    Generates a loader object based on the file extension of the provided path.

    This function selects the appropriate loader for handling different file types:
    - `.pdf` files are handled by `PyPDFLoader`.
    - `.md` files are handled by `UnstructuredMarkdownLoader`.
    - `.txt` files are handled by `TextLoader`.

    If the file extension is not supported, a `ValueError` is raised.

    Args:
        path (str): The file path, including the file name and extension.

    Returns:
        loader: An instance of the appropriate loader class based on the file extension.

    Raises:
        ValueError: If the file extension is not supported (.pdf, .md, .txt).
    """
    if path.endswith(".pdf"):
        loader = PyPDFLoader(path)
    elif path.endswith(".md"):
        loader = UnstructuredMarkdownLoader(path)
    elif path.endswith(".txt"):
        loader = TextLoader(path)
    else:
        # Catch error
        raise ValueError(f"Unsupported file extension: {path}")
    return loader


def load_split_docs(path: str):
    """
    Loads documents from a specified path and splits them into smaller chunks.

    This function handles both individual files and directories containing multiple files.
    It uses the appropriate loader based on the file type to load the content, then splits the
    loaded documents into chunks using a recursive character text splitter.

    Args:
        path (str): The path to the file or directory. If a directory, it should end with a `/`.

    Returns:
        list: A list of document chunks, where each chunk is a portion of the original documents
        split according to the specified chunk size and overlap.

    Raises:
        ValueError: If the file extension is not supported when processing individual files.
    """
    if path.endswith("/"):
        files = [f for f in listdir(path) if isfile(join(path, f))]
        docs = []
        for file in files:
            loader = generate_loader((join(path, file)))
            docs += loader.load()
    else:
        loader = generate_loader(path)
        docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)

    return splits


def get_faiss_vector_store(path, reload=True, save_local=True):
    """
    Retrieves or creates a FAISS vector store for document embeddings.

    This function checks if a FAISS index already exists at the specified path and,
    if so, loads it. If no index is found or if `reload` is set to `False`, it creates
    a new FAISS vector store from documents located at the path, using OpenAI's embeddings.

    Args:
        path (str): The path where the FAISS index is stored or where documents are located.
        reload (bool, optional): Whether to reload an existing FAISS index if it exists. Defaults to True.
        save_local (bool, optional): Whether to save the newly created FAISS index to the local path. Defaults to True.

    Returns:
        FAISS: An instance of the FAISS vector store containing document embeddings.

    Raises:
        ValueError: If there is an issue with loading documents or creating the FAISS index.
    """
    if isdir(join(path, "faiss_index")) and reload:
        path = join(path, "faiss_index")
        return FAISS.load_local(
            path,
            embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
            allow_dangerous_deserialization=True,
        )

    documents = load_split_docs(path=path)

    faissvectorstore = FAISS.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    )

    if save_local:
        faissvectorstore.save_local(join(path, "faiss_index"))

    return faissvectorstore


vectorstore = get_faiss_vector_store("./documents/levisbk/")
retriever = vectorstore.as_retriever()


def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]

    # Retrieval
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}
