from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from vectorstores.faiss import get_faiss_vector_store

vectorstore = get_faiss_vector_store("./documents/nike_form_2023/")
retriever = vectorstore.as_retriever()

# Model
llm = ChatOpenAI(
    model="gpt-4o-mini",
)

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
pdf_rag_chain = create_retrieval_chain(retriever, question_answer_chain)
