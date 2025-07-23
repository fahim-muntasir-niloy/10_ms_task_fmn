import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from tools import hsc_kb
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
SUPABASE_PG_CONN_URL = os.getenv("SUPABASE_PG_CONN_URL")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Project tracing -> Evaluation
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "10ms_fmn"

# LLM
llm = init_chat_model(
    model="gemini-2.5-flash", model_provider="google_genai", temperature=0.5
)

checkpointer = MemorySaver()  # in memory saver for short term memory of each thread


async def agent_chat(msg: str, thread_id: str):
    hsc_bot = create_react_agent(
        model=llm,
        tools=[hsc_kb],
        prompt="""You are an experienced Bangla teacher. 
                You will help students of HSC level with Bangla First paper topics.
                Always answer from the **hsc_kb** tool.
                You will always answer in professional tone,
                and keep the answer precise without any salutation or extra text.
                You will always answer in Bangla text.""",
        checkpointer=checkpointer,
    )

    config = {"configurable": {"thread_id": thread_id}}
    res = await hsc_bot.ainvoke({"messages": msg}, config)
    return res["messages"][-1].content
