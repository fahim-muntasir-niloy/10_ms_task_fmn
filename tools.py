import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

load_dotenv()
SUPABASE_PG_CONN_URL = os.getenv("SUPABASE_PG_CONN_URL")

# embedding engine
embedding_engine = OllamaEmbeddings(
    base_url=os.getenv("OLLAMA_EMBEDDING_URL"),
    model="bge-m3:latest",
)


@tool
def hsc_kb(query: str):
    """
    Retrieve information from knowledgebase similar to the user's query.
    """
    vector_store = PGVector(
        embeddings=embedding_engine,
        collection_name="hsc_bangla",
        connection=SUPABASE_PG_CONN_URL,
        use_jsonb=True,
    )

    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 10}
    )
    docs = retriever.invoke(query)

    return [doc.page_content for doc in docs]
