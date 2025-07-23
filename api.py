from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import agent_chat
import uuid

app = FastAPI(
    title="HSC Bangla Bot",
    description="A bot that can answer questions about the HSC Bangla First Paper",
    version="1.0.0",
    contact={
        "name": "Fahim Muntasir",
        "email": "muntasirfahim.niloy@gmail.com",
    },
)

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    messages: str
    thread_id: str = str(uuid.uuid4())


@app.post("/chat", tags=["chat"])
async def chat_endpoint(request: ChatRequest):
    response = await agent_chat(request.messages, request.thread_id)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn

    print("""
    ██╗  ██╗███████╗ ██████╗    ██████╗  █████╗ ███╗   ██╗ ██████╗ ██╗      █████╗     ██████╗  ██████╗ ████████╗
    ██║  ██║██╔════╝██╔════╝    ██╔══██╗██╔══██╗████╗  ██║██╔════╝ ██║     ██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
    ███████║███████╗██║         ██████╔╝███████║██╔██╗ ██║██║  ███╗██║     ███████║    ██████╔╝██║   ██║   ██║   
    ██╔══██║╚════██║██║         ██╔══██╗██╔══██║██║╚██╗██║██║   ██║██║     ██╔══██║    ██╔══██╗██║   ██║   ██║   
    ██║  ██║███████║╚██████╗    ██████╔╝██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║    ██████╔╝╚██████╔╝   ██║   
    ╚═╝  ╚═╝╚══════╝ ╚═════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝   
    """)

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
