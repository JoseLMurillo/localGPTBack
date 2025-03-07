import numpy as np
from ollama import chat
from typing import List

from classes.agent_functions import generate_embedding, find_relevant_context, summarize_history

from routers.file_manager import update_message_to_conversation_file, add_to_full_history_conversation_file, add_embedding_to_conversation_file, get_embeddings_of_conversation, get_full_history_of_conversation


class Agent():
    def __init__(self, file_id: str, model: str, system_prompt:str = "", num_answers: int = 0, options: dict = {}, max_history: int = 10, summary_model: str = "ollama3.2:1b", chat_history: list = []):
        
        self.file_id = file_id
        
        self.model: str = model
        self.system_prompt = system_prompt
        self.num_answers = num_answers
        self.options = options
        self.max_history = max_history
        self.summary_model = summary_model
        self.chat_history = chat_history
        if(len(chat_history)): self.chat_history = [{"role":"system", "content": system_prompt}]
        
        self.embeddings_vectors: List[np.ndarray] = []
        self.resume_context = ""
 
    def __str__(self):
        """
        Returns the agent's shape.
        """
        return f"AGENT: model: {self.model}, system_prompt:{self.system_prompt}, num_answers: {self.num_answers}, options: {self.options}, max_history: {self.max_history}, summary_model: {self.summary_model}"
        
         
    def generate_response(self, message):
        current_embedding = generate_embedding(message)
        add_embedding_to_conversation_file(self.file_id, current_embedding)
        embeddings_vectors = get_embeddings_of_conversation(self.file_id)
        full_history = get_full_history_of_conversation(self.file_id)
        relevant_context = find_relevant_context(current_embedding, embeddings_vectors, full_history)
        
        # Check if history needs to be summarized
        if len(self.chat_history) >= self.max_history:
            self.resume_context = summarize_history(self.chat_history, self.summary_model)
            
            # Keep only the system message and the last two messages
            self.chat_history = [
                self.chat_history[0],
                {"role": "system", "content": f"Summary of the previous conversation:\n{self.resume_context}"},
                *self.chat_history[-2:]
            ]
            
        # Prepare the message with context
        context_message = (
            f"{message}\n\nRelevant context of the previous conversation:\n{relevant_context}\n"
            f"Summary of the conversation:\n{self.resume_context}" if self.resume_context else message
            )
        
        format_user_message = {"role":"user", "content": context_message}
        self.chat_history.append(format_user_message)
        
        total_response = ""
        
        response = chat(model = self.model, messages= self.chat_history, stream=True, keep_alive=60)
        
        for word in response:
            total_response += word['message']['content']
            yield word['message']['content']
            
        format_assitant_response = {"role":"assistant", "content": total_response}
                
        self.chat_history.append(format_assitant_response)
        
        if(self.file_id != ""):
            add_to_full_history_conversation_file(self.file_id, [format_user_message, format_assitant_response])
            update_message_to_conversation_file(self.file_id, self.chat_history) 