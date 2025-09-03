import streamlit as st
st.set_page_config(page_title="Innovista Complaint AI Agent", layout="wide")
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
import base64
import streamlit.components.v1 as components

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
 
dirImage = image_to_base64("images/d.png")    
img1 = image_to_base64("images/h1.jpeg")
img2 = image_to_base64("images/h2.jpeg")
img3 = image_to_base64("images/h3.jpeg")
img4 = image_to_base64("images/h4.jpeg")
img5 = image_to_base64("images/h5.jpeg")
img6 = image_to_base64("images/h6.jpeg")
img7 = image_to_base64("images/h7.jpeg")
img8 = image_to_base64("images/h8.jpeg")
img9 = image_to_base64("images/h9.jpeg")
img11 = image_to_base64("images/h11.jpeg")
img12 = image_to_base64("images/h12.jpeg")
img13 = image_to_base64("images/h13.jpeg")
bg_image = image_to_base64("images/h5.jpeg")
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
    name="Innovista Complaints Handle Agent",
    instructions=complain_agent_instructions,
    model=model,
    tools=[post_all_complaints_from_sheet,get_all_complaints_data,send_complaint_to_staff],
)
st.markdown(
    f"""
    <style>
      .stApp::before {{
     content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background-image: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)),
    url("data:image/jpeg;base64,{bg_image}");
    background-size: cover; 
    background-position: center center;
    background-repeat: no-repeat;
    z-index: -1;
}}

.stApp {{
   position: relative;
    min-height: 100vh;
    color: white;
    background-color: transparent;
}}
.header-container {{
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 10px;
    }}
    .circular-img {{
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    background-color: blue; 
    box-shadow: 0 0 12px 4px rgba(255, 255, 255, 0.9); 
     
}}

    .gradient-text {{
        background: linear-gradient(to right, red, blue);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: transparent;
        font-size: 1.6rem;
        font-weight: bold;
        margin: 0;
    }}
    
    
         /* ✅ Button styling */
        .stButton>button, .stForm button {{
            background-color: #FF0303;
            font-family: "Inter", Sans-serif
            color: white;
            font-size: 1em;
            padding: 0.5rem 1.8rem;
            border: none;
            border-radius: 999px;  /* full pill shape */
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease-in-out;
        }}
          

        .stButton>button:hover, .stForm button:hover {{
            background-color: white;
            color: #FF0303;
        }}

        .stTextArea textarea {{
        color: white !important;
        background-color: black !important;
        border: 1px solid white !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }}
    .stTextArea textarea::placeholder {{
        color: black !important;
    }}
     .stTextArea label {{
        color: white !important;
        font-size: 22px !important;
        font-weight: 600 !important;
        margin-bottom: 1rem;
        margin-top: 1rem;
    }}
    .agent-reply {{
        background-color: #393E46;  /* Dark gray */
        color: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid white !important;
        margin-top: 1rem;
        font-size: 16px;
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    
    label, .stTextInput label, .stTextArea label, .stSelectbox label {{
        color: white !important;
        font-weight: 600;
    }}

    /* Style text inputs and textarea */
    .stTextInput input, .stTextArea textarea {{
        background-color: black !important;
        color: white !important;
        border: 1px solid white !important;
        border-radius: 6px !important;
    }}

     div[data-baseweb="select"] > div {{
        background-color: black  !important;
        color: white !important;
        border: 1px solid white !important;
    }}

    /* Force text inside select box to stay white */
    div[data-baseweb="select"] span {{
        color: white !important;
    }}

    /* Dropdown popup menu */
    ul[role="listbox"] {{
        background-color: black  !important;
        border: 2px solid white !important;
    }}

    /* Dropdown options */
    li[role="option"] {{
        background-color:#222  !important;
        color: white !important;
    }}

    /* Hover effect */
    li[role="option"]:hover {{
        background-color: #333 !important;
        color: white !important;
    }}
 
          </style>
    """,
    unsafe_allow_html=True
)


left_col, right_col = st.columns([2, 1])  # 2:1 ratio (left:right)

with left_col:
    st.markdown(f"""
    <div class="header-container">
        <img src="data:image/png;base64,{dirImage}" class="circular-img">
        <h1 class="gradient-text">Innovista Complaint AI Agent</h1>
    </div>
    """, unsafe_allow_html=True)

    # Row 1: Name + Contact
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
    with col2:
        contact = st.text_input("Contact")
    
    # Row 3: Company + Complaint Type
    col3, col4 = st.columns(2)
    with col3:
      company = st.selectbox("", options=["Select Company ","CloudLead", "Viper", "ReXon Solution","other"])

    with col4:
        complaint_type = st.selectbox("", [" complaint type","Internet Issue", "Cleaning Issue", "Technical", "Eletric issue", "other"])

    # Complaint details (textarea)
    prompt = st.text_area("📝 Enter Complaint Details:" )

if "history" not in st.session_state:
    st.session_state.history = []


if st.button("📨 Submit Complaint"):
    with st.spinner("Submitting your complaint, please wait..."):
        st.session_state.history.append({"role": "user", "content": f"{prompt} {name} {contact} {company} {complaint_type}"  })

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
        st.markdown(f"""
    <div class="agent-reply">
        🤖 {result.final_output}
    </div>
    """,
    unsafe_allow_html=True
)
with right_col:
    st.markdown("")
    components.html(
        f"""
        <div class="carousel-container">
            <style>
                .carousel-container {{
    position: relative;
    width: 100%;
    height: 300px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.3);  /* light white border */
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}}

            .carousel-container img {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            animation: fadeAnimation 36s infinite;
            opacity: 0;
        }}

    .carousel-container img:nth-child(1) {{ animation-delay: 0s; }}
    .carousel-container img:nth-child(2) {{ animation-delay: 3s; }}
    .carousel-container img:nth-child(3) {{ animation-delay: 6s; }}
    .carousel-container img:nth-child(4) {{ animation-delay: 9s; }}
    .carousel-container img:nth-child(5) {{ animation-delay: 12s; }}
    .carousel-container img:nth-child(6) {{ animation-delay: 15s; }}
    .carousel-container img:nth-child(7) {{ animation-delay: 18s; }}
    .carousel-container img:nth-child(8) {{ animation-delay: 21s; }}
    .carousel-container img:nth-child(9) {{ animation-delay: 24s; }}
    .carousel-container img:nth-child(10) {{ animation-delay: 27s; }}
    .carousel-container img:nth-child(11) {{ animation-delay: 30s; }}
    .carousel-container img:nth-child(12) {{ animation-delay: 33s; }}

        @keyframes fadeAnimation {{
            0% {{ opacity: 0; }}
            5% {{ opacity: 1; }}
            30% {{ opacity: 1; }}
            35% {{ opacity: 0; }}
            100% {{ opacity: 0; }}
        }}
            </style>

            <img src="data:image/jpeg;base64,{img1}" alt="Image 1" />
            <img src="data:image/jpeg;base64,{img2}" alt="Image 2" />
            <img src="data:image/jpeg;base64,{img3}" alt="Image 3" />
            <img src="data:image/jpeg;base64,{img4}" alt="Image 4" />
            <img src="data:image/jpeg;base64,{img5}" alt="Image 5" />
            <img src="data:image/jpeg;base64,{img6}" alt="Image 6" />
            <img src="data:image/jpeg;base64,{img7}" alt="Image 7" />
            <img src="data:image/jpeg;base64,{img8}" alt="Image 8" />
            <img src="data:image/jpeg;base64,{img9}" alt="Image 9" />
             <img src="data:image/jpeg;base64,{img11}" alt="Image 7" />
            <img src="data:image/jpeg;base64,{img12}" alt="Image 8" />
            <img src="data:image/jpeg;base64,{img13}" alt="Image 9" />
        </div>
        """,
        height=300
    )
