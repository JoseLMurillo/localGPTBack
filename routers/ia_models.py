from fastapi import APIRouter, HTTPException
from ollama import list as ollamaList

IAModels = APIRouter()


@IAModels.get("/models", tags=["Models"])
def get_ollama_intalled_models() -> list[str] | str:
    """
    Returns the list of all installed ollama models installed
    """
    try:
        model_data: dict = ollamaList().models 

        if(len(model_data) == 0):
            raise HTTPException(status_code=404, detail="There are no ollama models installed.")
        
        modelList: list = [element.model for element in model_data]
        return modelList

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading ollama models: {str(e)}")
    