from os import listdir
from os.path import isfile, join

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_split_docs_pypdf(path: str):
    if path.endswith("/"):
        files = [f for f in listdir(path) if isfile(join(path, f))]
        
        docs = []
        for file in files:
            loader = PyPDFLoader((join(path, file)))
            docs += loader.load()
    else:
        loader = PyPDFLoader(path)

        docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    return splits