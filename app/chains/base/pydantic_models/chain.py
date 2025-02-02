from pydantic import BaseModel


class ChainInput(BaseModel):
    """
    Chain input
    """

    input: str
