from pydantic import BaseModel


class GraphInput(BaseModel):
    """
    Graph Input
    """

    question: str
