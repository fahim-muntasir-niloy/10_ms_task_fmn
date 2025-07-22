import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from tools import hsc_kb
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import uuid

load_dotenv()
SUPABASE_PG_CONN_URL = os.getenv("SUPABASE_PG_CONN_URL")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# LLM
llm = init_chat_model(
    model="gemini-2.5-flash", model_provider="google_genai", temperature=0.8
)

checkpointer = MemorySaver()


async def chat(msg):
    hsc_bot = create_react_agent(
        model=llm,
        tools=[hsc_kb],
        prompt="""You are an experienced Bangla teacher. 
    You will help students of HSC level with Bangla First paper topics.
    Always answer from the **hsc_kb** tool.
    You will always answer in a friendly tone and Bangla text.""",
        checkpointer=checkpointer,
    )

    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    res = await hsc_bot.ainvoke({"messages": msg}, config)
    return res["messages"][-1].content
