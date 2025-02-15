from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.ia_agents import IAAgents, get_ollama_local_agents
from routers.conversations import Conversations
from routers.file_manager import Conversation_Files
from routers.ia_models import IAModels, get_ollama_intalled_models



origins = [
    "http://localhost:5173",  # React (Vite)
    "http://127.0.0.1:5173",  # Otra forma de acceder a React
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router=IAModels)
app.include_router(router=IAAgents)
app.include_router(router=Conversation_Files)
app.include_router(router=Conversations)


@app.get("/config/", tags=["Config"], status_code=200)
def getBasicConfig():
    """
    Checks if there are any ollama models installed and if there are any agent configurations and returns them.
    """
    opciones = {
            "models": get_ollama_intalled_models(),
            "agents": get_ollama_local_agents()
            }
        
    return opciones
