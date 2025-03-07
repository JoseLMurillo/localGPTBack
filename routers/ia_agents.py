import json, os
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from calculations.utilities import id_generator

from classes.agent import Agent

from models.models import Conversation_Chat, AgentModel, AgentModelPut

from routers.file_manager import get_conversation_content

IAAgents = APIRouter()

#KEEP THE AGENT IN MEMORY
active_agents = {}

this_path = os.path.dirname(__file__)
default_agent_path = os.path.join(this_path, "..", "default_agent", "default_agents.json")


# FILE
def get_agents_from_file() -> list:
    """
    Returns the agents stored in the default_agents.json file
    """
    if not os.path.exists(default_agent_path):
        raise HTTPException(status_code=404, detail="Agents file no fount")

    try:
        with open(default_agent_path, "r", encoding="utf-8") as agents:
            return json.load(agents)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="File not found")


def change_agent_file(file_content: list):
    """
    Modify and add data to the agent file
    :param file_content
    """
    if not os.path.exists(default_agent_path):
        raise HTTPException(status_code=404, detail="Agents file not fount")

    try:
        with open(default_agent_path, "w", encoding="utf-8") as file:
            json.dump(file_content, file, indent=4, ensure_ascii=False)
            
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="File not found")
       
    
#AGENT       
@IAAgents.get("/agents", tags=["Agents"])
def get_ollama_local_agents() -> list:
    """
    Returns a list of agents with a format: id, name, resume, model
    """
    
    agent_list: dict  = get_agents_from_file()

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


@IAAgents.post("/agent", tags=["Agents"])
def add_ollama_local_agents(agent: AgentModel) -> dict:
    """
    Add a new agent.
    :param agent
    :return agent name
    """
    
    agent.id = id_generator()
   
    file_content: list  = get_agents_from_file()
    file_content.append(dict(agent))
    
    change_agent_file(file_content)
    
    return {"message": "Agent added"}


@IAAgents.put("/agent/{id}", tags=["Agents"])
def update_ollama_local_agent(id: str, agent: AgentModelPut) -> dict:
    """
    Update an agent.
    :param id: Agent id
    :param agent
    """
    
    file_content = get_agents_from_file()

    for i, local_agent in enumerate(file_content):
        if local_agent["id"] == id:
            break 
    else:
        raise HTTPException(status_code=404, detail="Agent not found")

    updated_agent = local_agent.copy()

    updated_agent["name"] = agent.name if agent.name is not None else local_agent.get("name", agent.name)
    updated_agent["resume"] = agent.resume if agent.resume is not None else local_agent.get("resume", agent.resume)
    updated_agent["prompt"] = agent.prompt if agent.prompt is not None else local_agent.get("prompt", agent.prompt)
    updated_agent["model"] = agent.model if agent.model is not None else local_agent.get("model", agent.model)

    if updated_agent != local_agent:
        file_content[i] = updated_agent
        change_agent_file(file_content)
        return {"message": "Agent updated"}
    
    return {"message": "Agent not updated"}
    

@IAAgents.delete("/agent/{id}", tags=["Agents"])
def delete_ollama_local_agent(id: str) -> dict:
    """
    Delete an agent.
    :param id
    """
    file_content: list  = get_agents_from_file()
    
    new_file_content = [agent for agent in file_content if agent["id"] != id]
    
    if(len(new_file_content) == len(file_content)):
        raise HTTPException(status_code=404, detail="Agent not fount")
    
    change_agent_file(new_file_content)
    return {"message": "Agent deleted"}


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
    