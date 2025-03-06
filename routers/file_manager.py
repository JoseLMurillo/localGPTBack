import os, json
import numpy as np
from typing import List
from datetime import datetime

from calculations.utilities import id_generator

from fastapi import APIRouter, HTTPException

from models.models import ContentFileTemplate

Conversation_Files = APIRouter()

actual_path = os.path.dirname(__file__)
json_path = os.path.join("..", "conversations")
json_local_path = os.path.join(actual_path, json_path)


#INDEX
def add_file_to_index(file_path: str, conversation_name: str) -> str:
    """
    Add file to index
    :return index_file_id
    """
    index_file_id = id_generator()
    to_add = {"conversation_name":conversation_name, "file_path": file_path}
    file_content: dict  = read_file_index()
    file_content[index_file_id] = to_add
    
    if write_file_index(file_content): return index_file_id


def read_file_index() -> json:
    """
    Reads the index of files and returns the list of them in the format
    id: {
        conversation_name, 
        file_path
    }
    """
    
    index_file_path = os.path.join(json_local_path, "index.json")
    if not os.path.exists(index_file_path):
        raise HTTPException(status_code=404, detail="Index file no exist")
    
    try:
        with open(index_file_path, "r", encoding="utf-8") as file:
            return json.loads(file.read())
    except json.JSONDecodeError:
        raise HTTPException(status_code=404, detail="File not reader.")  


def write_file_index(content: dict) -> bool:
    """
    Writes a new value to the index file and returns True if created
    """
    index_file_path = os.path.join(json_local_path, "index.json")
    if not os.path.exists(index_file_path):
        raise HTTPException(status_code=404, detail="File no fount")
    
    try:
        with open(index_file_path, "w", encoding="utf-8") as file:     
            json.dump(content, file, indent=4, ensure_ascii=False)
            return True
    except json.JSONDecodeError:
        raise HTTPException(status_code=404, detail="File not found.")
    

def get_all_conversations_indexed() -> json:
    """
    Return a list with id and conversations name for a index with format {id, name}
    """
    file_content: dict = read_file_index()
    
    conversation_list: list = [{
        "id": conversation, 
        "name": file_content[conversation]["conversation_name"]
        } for conversation in file_content]

    return conversation_list


#FILE
def create_conversation_file(format_file_name: str, content: ContentFileTemplate):
    """
    Create a file.json with a info about a conversation with a unic id and content like 
    {
    conversation_name,
    agent_config: {model, system_prompt, num_answers, options, max_history, summary_model},
    messages_history: [{role, content}],
    resume_context,
    full_history: [{role, content}],
    embeddings_vectors": [[]],
    timestamp
    }
    
    :Param format_file_name
    :Param content
    :return create file_path
    """
    
    file_path = f"{json_local_path}/{format_file_name}"
    
    #Converts the BaseModel to dict
    file_content = dict(content)
    file_content["agent_config"] = dict(file_content["agent_config"])
    
    file_content["agent_id"] = id_generator()
    file_content["timestamp"] = datetime.now().isoformat()

    try:
        with open(file_path, "w",  encoding="utf-8") as file:
            json.dump(file_content, file, indent=4, ensure_ascii=False)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to create conversation file: {str(e)}")
    
    return os.path.join(json_path, format_file_name)


def add_embedding_to_conversation_file(file_id: str, embedding: np.ndarray):
    """
    Add new messages to the entire conversation history.
    """
    file_content: dict  = read_file_index()
    convert_embedding = embedding.tolist()
    
    if(file_id not in file_content):
        raise HTTPException(status_code=404, detail="File not found in index")
    
    file_path = file_content[file_id]["file_path"]
    conversation_content = get_conversation_content(file_id)
    
    conversation_content["embeddings_vectors"].append(convert_embedding)

    add_conversation_file(file_path, conversation_content)


def get_embeddings_of_conversation(file_id: str) -> List[np.ndarray]:
    """
    Get all info from a file of a conversation if file exist.
    :param file_id: Id in index
    :return List[np.ndarray]
    """

    file_content: dict  = read_file_index()
    
    if(file_id not in file_content):
        raise HTTPException(status_code=404, detail="File not found in index")
    
    file_path = file_content[file_id]["file_path"]

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Conversation file no fount")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = json.loads(file.read())
            embedding = file_content["embeddings_vectors"]
            return embedding
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="File JSON corrupted")

    
def get_full_history_of_conversation(file_id: str) -> dict:
    """
    Get all info from a file of a conversation if file exist.
    :param file_id: Id in index
    :return full_history at format dict
    """
    file_content: dict  = read_file_index()
    if(file_id not in file_content):
        raise HTTPException(status_code=404, detail="Conversation file no fount")
    
    file_path = file_content[file_id]["file_path"]    

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Conversation file no fount")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = json.loads(file.read())
            return file_content["full_history"]
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="File JSON corrupted")    


def add_conversation_file(file_path: str, file_content):
    """
    Agrega informacion a un archivo de conversación existente
    :Param file_name
    :Param content
    """
    try:
        with open(file_path, "w",  encoding="utf-8") as file:
            json.dump(file_content, file, indent=4, ensure_ascii=False)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to create file: {str(e)}")
    
    return file_path

    
# CONVERSATION
def create_conversation(file_content: ContentFileTemplate) -> str:
    """
    Create a new conversation with a unic id for a file with a format
    {
    conversation_name,
    agent_config: {model, system_prompt, num_answers, options, max_history, summary_model},
    messages_history: [{role, content}],
    resume_context,
    full_history: [{role, content}],
    embeddings_vectors": [[]],
    }
    
    and add to index.
    """
    
    format_file_name = f"{id_generator()}.json"
    
    file_path = create_conversation_file(format_file_name, file_content)
    conversation_id = add_file_to_index(file_path, conversation_name=file_content.conversation_name)

    return conversation_id


def get_conversation_content(file_id: str) -> json:
    """
    Get all info from a file of a conversation if file exist.
    :param file_id: Id in index
    """
    file_path = ""
    file_content: dict  = read_file_index()
    if(file_id in file_content):
        file_path = os.path.join(actual_path, file_content[file_id]["file_path"])

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Conversation file no fount")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.loads(file.read())
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="File JSON corrupted")


def add_to_full_history_conversation_file(file_id: str, messages: list):
    """
    Add new messages to the entire conversation history
    """
    file_content: dict  = read_file_index()
    
    if(file_id not in file_content):
        raise HTTPException(status_code=404, detail="Conversation file no fount")
    
    file_path = file_content[file_id]["file_path"]
    conversation_content = get_conversation_content(file_id)
    
    conversation_content["full_history"].extend(messages)

    add_conversation_file(file_path, conversation_content)


def update_message_to_conversation_file(file_id: str, messages: list):
    """
    Updates the message history that the agent has in memory to the conversation file
    """
    file_content: dict  = read_file_index()
    
    if(file_id not in file_content):
        raise HTTPException(status_code=404, detail="Conversation file no fount")

    file_path = file_content[file_id]["file_path"]
    
    conversation_content = get_conversation_content(file_id)
    conversation_content["messages_history"] = messages
    
    add_conversation_file(file_path, conversation_content)