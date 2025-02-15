import json, os
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from classes.agent import Agent

from models.models import Conversation_Chat

from routers.file_manager import get_conversation_content

IAAgents = APIRouter()

#KEEP THE AGENT IN MEMORY
active_agents = {}

this_path = os.path.dirname(__file__)
default_agent_path = os.path.join(this_path, "..", "default_agent", "default_agents.json")

# GETS FILE
def get_agents_from_file() -> list:
    """
    Returns the agents stored in the default_agents.json file
    """
    try:
        with open(default_agent_path, "r", encoding="utf-8") as agents:
            return json.load(agents)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="File not found")
    

@IAAgents.get("/agents", tags=["Agents"])
def get_ollama_local_agents() -> list:
    """
    Returns a list of agents with a format: id, name, resume, model
    """

    try:
        agent_list: list = [{
            "id":agent.get("id"), 
            "name":agent.get("name"), 
            "resume":agent.get("resume"), 
            "model":agent.get("model")
            } for agent in get_agents_from_file()]
            
        return agent_list
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="File default agents corrupted")
    

#CHAT
def chat_with_agent(conversation: Conversation_Chat) -> StreamingResponse:
    """
    Returns the response of an agent in stream format taking the agent configuration from a conversation file by its id and keeping the agent in memory.
    :param conversation: {conversation_id: str, message: str}
    """
    
    agent: Agent = None
    conversation_content = get_conversation_content(conversation.conversation_id)
    
    agent_id: str = conversation_content["agent_id"]
    
    agent_config = {
        "model": conversation_content["agent_config"]["model"],
        'system_prompt': conversation_content["agent_config"]["system_prompt"], 
        'num_answers': conversation_content["agent_config"]["num_answers"], 
        'options': conversation_content["agent_config"]["options"], 
        'max_history': conversation_content["agent_config"]["max_history"], 
        'summary_model': conversation_content["agent_config"]["summary_model"],
        'chat_history': conversation_content["messages_history"],
        'file_id': conversation.conversation_id
        }
    
    #Keeps agents in memory
    if(agent_id not in active_agents):
        agent = Agent(**agent_config)
        active_agents[agent_id] = agent
        
    agent = active_agents[agent_id]
    
    return StreamingResponse(agent.generate_response(conversation.message), media_type="text/plain")