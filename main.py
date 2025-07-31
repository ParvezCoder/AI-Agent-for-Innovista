import streamlit as st
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
# from whatsapp_sender import send_whatsapp_message
import asyncio
from get_data import get_all_complaints_data
from post_data import post_all_complaints_from_sheet
from instructions import complain_agent_instructions
from whatsapp_sender import send_complaint_to_staff

load_dotenv()
set_tracing_disabled(True)

API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

InnovistaCare = Agent(
    name="Innovista Complaints Hanlde Agent",
    instructions=complain_agent_instructions,
    model=model,
    tools=[post_all_complaints_from_sheet,get_all_complaints_data,send_complaint_to_staff],
)






# Streamlit App
st.title("📡 Innovista AI Smart Agent")

st.markdown("""
###
Your smart digital assistant that listens, understands, and delegates your concerns to the right team — instantly and intelligently.

Facing an issue with light, AC, internet, or any facility? Just type it in — our AI will forward it to the right department and keep track for you. Automated support, 24/7.
###
""")

prompt = st.text_area("📝 Enter Complaint Details:")

if "history" not in st.session_state:
    st.session_state.history = []


if st.button("📨 Submit Complaint"):
    with st.spinner("Submitting your complaint, please wait..."):
        st.session_state.history.append({"role": "user", "content": prompt})

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        result = loop.run_until_complete(
            Runner.run(
                starting_agent=InnovistaCare,
                input=st.session_state.history
            )
        )

        prompt = ""
        st.session_state.history.append({"role": "assistant", "content": result.final_output})

        st.success("Reply from Complaint Assistant:")
        st.write(result.final_output)
