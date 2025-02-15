# 🚀 AI Chatbot with FastAPI and Ollama  

This project is a **FastAPI**-based backend that integrates **Ollama** to provide an AI-powered chat, similar to ChatGPT, in a local environment.  

## 📌 Features  

- 🌍 Fast and lightweight API with **FastAPI**.  
- 🤖 Integration with **Ollama** for natural language processing.  
- 🔄 Modular architecture with well-defined routes and controllers.  
- 📝 Automatic documentation with **Swagger UI** and **ReDoc**.  

## 🛠️ Installation  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/your-repository.git  
cd your-repository  
```  

### 2️⃣ Create a virtual environment (optional but recommended)  
```bash
python -m venv venv  
source venv/bin/activate  # On Linux/Mac  
venv\Scripts\activate  # On Windows  
```  

### 3️⃣ Install dependencies  
```bash
pip install -r requirements.txt  
```  

### 4️⃣ Run the FastAPI server  
```bash
uvicorn main:app --reload  
```  

## 🔥 Usage  

1. Start the server and access the documentation at:  
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)  
   - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)  

2. You can test the endpoints directly from the documentation or use tools like **Postman** or `curl`.  

## 📁 Project Structure  

```
📂 your-repository/  
├── 📜 .gitignore  
├── 📜 README.md  
├── 📂 calculations/          # Business logic and calculations  
├── 📂 classes/               # Data classes and models  
├── 📂 conversations/         # Conversation handling  
├── 📂 default_agent/         # Default agent logic  
├── 📂 manage_document/       # Document management  
├── 📂 models/                # Models and schemas  
├── 📂 routers/               # Endpoints and routes  
├── 📜 main.py                # Backend entry point  
```  

## 📜 Main Endpoints  

### Models  
| Method | Endpoint   | Description |  
|--------|-----------|-------------|  
| `GET`  | `/models` | Get Ollama Installed Models |  

### Agents  
| Method | Endpoint  | Description |  
|--------|----------|-------------|  
| `GET`  | `/agents` | Get Ollama Local Agents |  

### Conversations  
| Method | Endpoint                      | Description |  
|--------|--------------------------------|-------------|  
| `POST` | `/new_conversation/`          | Create New Conversation |  
| `GET`  | `/get_conversations/`         | Get All Conversations |  
| `GET`  | `/conversation/{conversation_id}` | Get Conversation |  
| `POST` | `/chat/`                      | Chatting |  

### Config  
| Method | Endpoint   | Description |  
|--------|-----------|-------------|  
| `GET`  | `/config/` | Get basic config |  

## 📋 Data Schemas  

### **AgentConfig**  
```json
{
  "model": "string",
  "system_prompt": "string | null",
  "num_answers": "integer | null",
  "options": "object | null",
  "max_history": "integer",
  "summary_model": "string"
}
```  

### **ContentFileTemplate**  
```json
{
  "conversation_name": "string | null",
  "agent_config": "object",
  "messages_history": "array<object> | null",
  "resume_context": "string",
  "full_history": "array<object> | null",
  "embeddings_vectors": "array<array<number>> | null"
}
```  

### **Conversation_Chat**  
```json
{
  "conversation_id": "string",
  "message": "string"
}
```  

## 🛠 Technologies Used  

- 🐍 **Python 3.10+**  
- ⚡ **FastAPI**  
- 🔥 **Uvicorn**  
- 🤖 **Ollama AI**  
- 🗄 **SQLite/MySQL/PostgreSQL** (depending on configuration)  

## 🤝 Contributions  

Contributions are welcome! Please open an issue or a pull request.