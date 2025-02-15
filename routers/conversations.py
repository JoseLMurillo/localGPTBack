from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.models import Conversation_Chat, ContentFileTemplate

from routers.ia_agents import chat_with_agent
from routers.file_manager import create_conversation, get_all_conversations_indexed, get_conversation_content

Conversations = APIRouter()

#CONVERSATION
@Conversations.post('/new_conversation/', tags=["Conversations"])
def create_new_conversation(content: ContentFileTemplate) -> dict:
    """
    Creates a new conversation with a receiving content in the ContentFileTemplate format.
    Returns the conversation_id
    """
    conversation_id = create_conversation(content)
    return {"conversation id": conversation_id}


@Conversations.get('/get_conversations/', tags=["Conversations"])
def get_all_conversations() -> list:
    """
    Return a list with id and conversations name for a index with format {id, name}
    """
    return get_all_conversations_indexed()


@Conversations.get('/conversation/{convesation_id}', tags=["Conversations"])
def get_conversation(convesation_id: str) -> dict:
    """
    Take all the content of a conversation.
    """
    return get_conversation_content(convesation_id)


#CHAT
@Conversations.post('/chat/', tags=["Conversations"])
def chatting(conversation: Conversation_Chat) -> StreamingResponse:
    """
    Start a chat with an AI agent defined in a conversation file.
    :param conversation: {conversation_id: str, message: str}
    :return StreamingResponse
    """
    
    return chat_with_agent(conversation)