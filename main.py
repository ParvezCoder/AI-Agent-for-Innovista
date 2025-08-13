import streamlit as st
# testing parvez
st.set_page_config(page_title="Innovista Complaint AI Agent", layout="wide")
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI 
import asyncio
from get_data import get_all_complaints_data

from instructions import complain_agent_instructions
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
    tools=[get_all_complaints_data]
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
            border-radius: 999px;   
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease-in-out;
        }}
         .stButton {{
        margin-top: -10px;   
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

# Form fields
import requests

# Custom CSS for form fields and labels
st.markdown("""
<style>
    /* Input, dropdown, textarea background black, text white */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: black !important;
        color: white !important;
        border: 1px solid white !important;
    }
    /* Placeholder text white */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: white !important;
        opacity: 0.7;
    }
    /* Dropdown text white */
    div[data-baseweb="select"] span {
        color: white !important;
    }
    /* Labels white */
    label, .stSelectbox label, .stTextArea label {
        color: white !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

with left_col:
    # Initialize session_state for form fields
    if "form_data" not in st.session_state:
        st.session_state.form_data = {
            "name": "",
            "company_name": "Select Company Name",
            "phone": "",
            "complaint_type": "Select Complaint Type",
            "description": ""
        }

    with st.form("complaint_form"):
        name = st.text_input("👤 Your Name", value=st.session_state.form_data["name"], placeholder="Enter your name")
        company_name = st.selectbox("🏢 Company Name or Location", ["Select Company Name","Innovista","Digilyzr","Viper","Telec"], 
                                    index=["Select Company Name","Innovista","Digilyzr","Viper","Telec"].index(st.session_state.form_data["company_name"]))

        phone = st.text_input("📞 Phone Number", value=st.session_state.form_data["phone"], placeholder="Enter phone number")
        
        # Dropdown for complaint type
        complaint_types = [
            "Select Complaint Type",
            "AC Issue",
            "WiFi Problem",
            "Noise",
            "Billing",
            "Other"
        ]
        complaint_type = st.selectbox(
            "📌 Type of Complaint",
            complaint_types,
            index=complaint_types.index(st.session_state.form_data["complaint_type"]) if st.session_state.form_data["complaint_type"] in complaint_types else 0
        )

        description = st.text_area("📝 Description of the Issue", value=st.session_state.form_data["description"], placeholder="Write your complaint details here...")
        
        submitted = st.form_submit_button("📨 Submit Complaint")

        if submitted:
            if not name or not company_name or not phone or complaint_type == "Select Complaint Type" or not description:
                st.error("⚠️ Please fill in all the fields.")
            else:
                payload = {
                    "name": name,
                    "company_name": company_name,
                    "phone": phone,
                    "complaint_type": complaint_type,
                    "description": description,
                    "status": "Pending"
                }
                url = "https://script.google.com/macros/s/AKfycbxv9tBKo1C8oBOS8A5EnIkFF642weWjL7KFbMxbbmZVoEhwi6NQuMnT1-eFXPJmklbpFQ/exec"
                try:
                    res = requests.post(url, json=payload)
                    if res.status_code == 200:
                        st.success("✅ Complaint successfully submitted!")
                        # Reset form fields
                        st.session_state.form_data = {
                            "name": "",
                            "company_name": "Select Company Name",
                            "phone": "",
                            "complaint_type": "Select Complaint Type",
                            "description": ""
                        }
            
                    else:
                        st.error(f"❌ Failed to submit complaint. Status: {res.status_code}")
                except Exception as e:
                    st.error(f"🚨 Error: {e}")




    # This is now inside left_col ✅
    prompt = st.text_area("📝 Chat Us..:")
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("📨 Chat Us"):
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
            animation: fadeAnimation 34s infinite;
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
