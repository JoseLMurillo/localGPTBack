from fastapi import APIRouter
from ollama import list as ollamaList

IAModels = APIRouter()


@IAModels.get("/models", tags=["Models"])
def get_ollama_intalled_models() -> list[str] | str:
    """
    Returns the list of all installed ollama models installed
    """
    try:
        if(len(ollamaList().models) == 0):
            return "There are no ollama models installed."
        
        modelList: list = [element.model for element in ollamaList().models]
        return modelList

    except:
        return ("Error loading ollama models")
    