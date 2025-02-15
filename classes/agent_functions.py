import numpy as np
from ollama import embed, chat

#EMBEDDINGS
def generate_embedding(text: str) -> np.ndarray:
    """
    Use the nomic-embed-text model to create an embed.
    :param text: Texto to embed
    :return embedding in format np.array
    """
    response = embed(model='nomic-embed-text:latest', input=text)
    return np.array(response.embeddings[0])


def find_relevant_context(query_embedding, embeddings_vectors, embeddings_history, top_k: int = 3) -> str:
    """
    Find the most relevant messages in history using cosine similarity.
    :param query_embedding: Message converted to embed.
    :param embeddings_vectors: List of all stored embeds.
    :param embeddings_history: Full conversation history in text format with list.
    :param top_k(optional)
    
    :return str
    """
    if not embeddings_history:
        return ""
    
    # Calculate cosine similarities
    similarities = [
        np.dot(query_embedding, vec) / (np.linalg.norm(query_embedding) * np.linalg.norm(vec))
        for vec in embeddings_vectors
    ]
    
    # Get the indexes of the top_k most similar
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Building the relevant context
    relevant_messages = [
        embeddings_history[i]['content']
        for i in top_indices
        if similarities[i] > 0.7  # Threshold of similarity
    ]
    
    return "\n".join(relevant_messages)


#MODELS
def summarize_history(messages_history, summary_model) -> str:
    """
    Generate a summary of the conversation history using the summary model.
    """
    if len(messages_history) <= 2:  # Only the system message and one more
        return ""
        
    # Set the context for the summary
    conversation = "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in messages_history[1:]  # Exclude system message
        ])
    
    prompt_system = {
        "role": "system",
        "content": f"Summarize the following conversation keeping the most important points and who said them."
        }
        
    summary_prompt = {
        "role": "user",
        "content": conversation
        }
    
    # Generate the summary
    summary_response = chat(
        model= summary_model,
        messages=[prompt_system, summary_prompt]
    )
    
    return summary_response['message']['content']