from pydantic import BaseModel, constr

class ChatMessage(BaseModel):
    content: constr(max_length=500)  # Лимит 500 символов из тз
