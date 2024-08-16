from langgraph.graph import END, StateGraph, START

from graphs.adaptive_rag.state import GraphState

from graphs.adaptive_rag.nodes.index import retrieve
from graphs.adaptive_rag.nodes.web_search import web_search
from graphs.adaptive_rag.nodes.answer_generator import generate
from graphs.adaptive_rag.nodes.question_re_writer import transform_query
from graphs.adaptive_rag.nodes.retrieval_grader import grade_documents

from graphs.adaptive_rag.edges.edges import (
    decide_to_generate,
    grade_generation_v_documents_and_question,
    route_question,
)

from dotenv import load_dotenv

load_dotenv()

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("web_search", web_search)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("transform_query", transform_query)

# Build graph
workflow.add_conditional_edges(
    START,
    route_question,
    {
        "web_search": "web_search",
        "vectorstore": "retrieve",
    },
)
workflow.add_edge("web_search", "generate")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    },
)
workflow.add_edge("transform_query", "retrieve")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "transform_query",
    },
)

# Compile
adaptive_rag = workflow.compile()
