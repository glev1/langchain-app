from os import listdir
from os.path import isfile, join

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_split_docs_pypdf(path: str):
    """
    Loads and splits PDF documents from a specified path.

    This function handles both individual PDF files and directories containing multiple PDF files.
    It uses `PyPDFLoader` to load the content of the PDF files and then splits the loaded documents
    into chunks using `RecursiveCharacterTextSplitter`.

    Args:
        path (str): The path to the PDF file or directory containing PDF files. If it's a directory,
                    it should end with a `/`.

    Returns:
        list: A list of document chunks, where each chunk is a portion of the original PDF documents,
              split according to the specified chunk size and overlap.
    """
    if path.endswith("/"):
        files = [f for f in listdir(path) if isfile(join(path, f))]

        docs = []
        for file in files:
            loader = PyPDFLoader((join(path, file)))
            docs += loader.load()
    else:
        loader = PyPDFLoader(path)

        docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)

    return splits
