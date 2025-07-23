import streamlit as st
import httpx
import asyncio
import uuid

st.set_page_config(page_title="HSC Bangla Bot", page_icon="📚")
st.title("📚 HSC Bangla Bot")
st.markdown("আপনার যেকোনো প্রশ্ন লিখুন। বাংলা প্রথম পত্রের যেকোনো সাহায্য পেতে পারেন!\n")

if "history" not in st.session_state:
    st.session_state["history"] = []
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())

user_input = st.text_input("", key="user_input")

if st.button("প্রেরণ করুন") and user_input.strip():
    st.session_state["history"].append({"role": "user", "content": user_input})
    with st.spinner("উত্তর দিচ্ছে..."):
        try:

            async def get_response():
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "http://localhost:8000/chat",
                        json={
                            "messages": user_input,
                            "thread_id": st.session_state["thread_id"],
                        },
                        timeout=60,
                    )
                    resp.raise_for_status()
                    return resp.json()["response"]

            response = asyncio.run(get_response())
            st.session_state["history"].append(
                {"role": "assistant", "content": response}
            )
        except Exception as e:
            st.error(f"❌ কোনো সমস্যা হয়েছে: {e}")

# Display chat history
for msg in st.session_state["history"]:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(90deg, #232526 0%, #414345 100%);
                color: #e0e0e0;
                border-radius: 12px;
                padding: 14px 18px;
                margin-bottom: 10px;
                border: 1.5px solid #333;
                box-shadow: 0 2px 8px rgba(40,40,40,0.18);
                max-width: 80%;
                margin-left: 0;
            ">
            {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(90deg, #232a34 0%, #2c5364 100%);
                color: #f5e9c8;
                border-radius: 12px;
                padding: 14px 18px;
                margin-bottom: 18px;
                border: 1.5px solid #2c5364;
                box-shadow: 0 2px 8px rgba(44,83,100,0.12);
                max-width: 80%;
                margin-left: auto;
            ">
            {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True,
        )
