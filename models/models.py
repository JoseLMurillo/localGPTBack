from pydantic import BaseModel, Field
from typing import Optional

class Conversation_Chat(BaseModel):
    conversation_id: str
    message: str
    
    
###
class Message(BaseModel):
    role: str
    content: str

class AgentConfig(BaseModel):
    model: str = Field(default="llama3.2:1b")
    system_prompt: Optional[str] = None
    num_answers: Optional[int] = None
    options: Optional[dict] = None
    max_history: int = Field(default= 10)
    summary_model: str
  
class ContentFileTemplate(BaseModel):
    conversation_name: Optional[str] = None
    agent_config: AgentConfig
    messages_history: Optional[list[Message]] = []
    resume_context: str
    full_history: Optional[list[Message]] = []
    embeddings_vectors: Optional[list[list[float]]] = []