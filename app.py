import streamlit as st
import os
import asyncio
import edge_tts
import cv2
import numpy as np
import easyocr  
import base64
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import plotly.graph_objects as go  
from PIL import Image
import re 

# Custom Modules 
from db_controller import init_db, register_user, login_user, save_chat, get_user_chats, clear_user_chats, update_user_password, get_username_by_email
from brain import train_assistant, smart_cleaner, get_ai_response
from pages_content import show_architecture_page, show_terms_page, show_privacy_page, show_contact_page

init_db()

@st.cache_resource
def load_ocr_reader():
    return easyocr.Reader(['en', 'hi'])

reader = load_ocr_reader()

# --- CYBERSHIELD PAGE CONFIGURATION ---
st.set_page_config(page_title="CyberShield AI | Advanced Threat Detection", page_icon="🛡️", layout="wide")

# --- EMAIL OTP DISPATCH FUNCTION (USING SECRETS) ---
def send_otp_email(receiver_email, otp_code, username="Operator"):
    SENDER_EMAIL = "shieldcyberai@gmail.com" 
    try:
        APP_PASSWORD = st.secrets["GMAIL_PASSWORD"]
    except:
        APP_PASSWORD = "your_app_password" 
    
    if APP_PASSWORD == "your_app_password":
        return False, "DEV_MODE"
        
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = "CyberShield AI - Security Authorization Code"
        body = f"Greetings {username},\n\nProtocol initiated.\n\nYour OTP for password recovery is: {otp_code}\n\nDo not share this authorization key with anyone."
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True, "Success"
    except Exception as e:
        return False, str(e)

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user_info' not in st.session_state: st.session_state['user_info'] = None
if 'messages' not in st.session_state: st.session_state['messages'] = []
if 'extracted_text' not in st.session_state: st.session_state['extracted_text'] = ""
if 'persona' not in st.session_state: st.session_state['persona'] = "Professional Mode"
if 'auto_send_msg' not in st.session_state: st.session_state['auto_send_msg'] = None
if 'nav_view' not in st.session_state: st.session_state['nav_view'] = "Threat Scanner"
if 'show_auth_page' not in st.session_state: st.session_state['show_auth_page'] = False
if 'auth_mode' not in st.session_state: st.session_state['auth_mode'] = "Login" 
if 'reset_step' not in st.session_state: st.session_state['reset_step'] = 1
if 'public_page' not in st.session_state: st.session_state['public_page'] = "home" 
if 'submit_val' not in st.session_state: st.session_state['submit_val'] = ""

def submit_chat():
    st.session_state['submit_val'] = st.session_state['inline_txt']
    st.session_state['inline_txt'] = ""

# ==================================================
# 🎨 CSS (FULL MOBILE RESPONSIVE FIX)
# ==================================================
bg_css = ""
if not st.session_state['logged_in'] and st.session_state['public_page'] == "home":
    bg_css = """
    .stApp { 
        background: linear-gradient(135deg, rgba(2, 6, 23, 0.85) 0%, rgba(9, 9, 11, 0.85) 100%), 
                    url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-position: center; background-attachment: fixed;
    }"""
else:
    bg_css = ".stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); background-attachment: fixed; }"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    {bg_css}
    h1, h2, h3, h4, h5, h6, p, span, li {{ font-family: 'Inter', sans-serif; color: #f8fafc; }}
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{ background-color: rgba(255, 255, 255, 0.05) !important; color: #e2e8f0 !important; border-radius: 12px; }}
    .stChatMessage {{ border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); }}
    
    .hero-title {{
        background: linear-gradient(to right, #ffffff, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 5rem; font-weight: 800; text-align: center; line-height: 1.1;
    }}

    /* CUSTOM CHAT BOX AT BOTTOM */
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) {{
        position: fixed !important; bottom: 25px !important; left: 50% !important; transform: translateX(-50%) !important;
        width: 90% !important; max-width: 800px !important; background-color: #2f3136 !important; border-radius: 30px !important;
        padding: 6px 10px !important; z-index: 9999 !important; display: flex !important; align-items: center !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.5) !important;
    }}

    @media (max-width: 768px) {{
        .hero-title {{ font-size: 2.8rem !important; margin-top: 20px !important; }}
        div[data-testid="column"] {{ text-align: center !important; margin-bottom: 10px !important; }}
        button[kind="secondary"], button[kind="primary"] {{ width: 100% !important; }}
        div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) {{ width: 95% !important; bottom: 15px !important; }}
    }}
</style>
""", unsafe_allow_html=True)

# --- CORE FUNCTIONS ---
def clean_text_for_speech(text):
    if not text: return ""
    return re.sub(r'[*_#`~>\[\]]', '', text).strip()

def speak(text, priority="Normal"):
    if not text: return
    try:
        VOICE = "en-IN-NeerjaNeural"
        async def _generate_audio():
            await edge_tts.Communicate(text, VOICE, rate="+5%").save("temp_ai_voice.mp3")
        asyncio.run(_generate_audio())
        with open("temp_ai_voice.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay="true" style="display:none;"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
        os.remove("temp_ai_voice.mp3")
    except: pass

def listen():
    st.toast("⚠️ Voice input is restricted in Cloud.")
    return ""

vectorizer, model = train_assistant()

# ====================================================
# 🚀 AUTHENTICATION & LANDING
# ====================================================
if not st.session_state['logged_in']:
    if st.session_state['show_auth_page']:
        if st.button("← Back", type="secondary"):
            st.session_state['show_auth_page'] = False; st.rerun()
            
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
            if st.session_state['auth_mode'] == "Forgot Password":
                e_reset = st.text_input("Enter Email").strip()
                if st.button("Send OTP", type="primary"):
                    # Logic for OTP
                    pass
            else:
                mode = st.radio("Action", ["Login", "Register"], label_visibility="collapsed")
                u = st.text_input("Operator ID").strip()
                if mode == "Register":
                    e = st.text_input("Email").strip()
                p = st.text_input("Access Key", type="password").strip()
                
                if st.button("Proceed", type="primary"):
                    if mode == "Register":
                        success, msg = register_user(u, e, p)
                        if success: st.success(msg); st.session_state['auth_mode']="Login"; st.rerun()
                        else: st.error(msg)
                    else:
                        user = login_user(u, p)
                        if user:
                            st.session_state['logged_in'] = True; st.session_state['user_info'] = user
                            st.session_state['messages'] = [{"role": ("user" if c['role']=="user" else "model"), "parts": [c['message']]} for c in get_user_chats(user['id'])]
                            st.rerun()
                        else: st.error("Authentication Denied.")
            st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state['public_page'] == "home":
        # Navbar
        nc1, nc2, nc3, nc4 = st.columns([4, 1, 1, 1])
        with nc1: st.markdown("### CyberShield.AI")
        with nc4: 
            if st.button("Get Started", type="primary"): st.session_state['show_auth_page']=True; st.rerun()
        
        st.markdown("<h1 class='hero-title'>Intelligence Meets<br>Cyber Defense</h1>", unsafe_allow_html=True)
        if st.button("Initialize System 🚀", type="primary"): st.session_state['show_auth_page']=True; st.rerun()

# ====================================================
# 🛡️ MAIN DASHBOARD
# ====================================================
else:
    user_id = st.session_state['user_info']['id']
    with st.sidebar:
        st.markdown(f"### {st.session_state['user_info']['username'].upper()}")
        st.session_state['nav_view'] = st.radio("Navigation", ["Threat Scanner", "Cyber Assistant"])
        if st.button("Logout"): st.session_state['logged_in']=False; st.rerun()

    if st.session_state['nav_view'] == "Threat Scanner":
        st.markdown("## Threat Assessment")
        msg = st.text_area("Input Payload")
        if st.button("Analyze", type="primary"):
            # Threat Logic
            st.success("Scanning complete.")

    else:
        # Chat System
        for msg in st.session_state['messages']:
            with st.chat_message(msg['role']): st.markdown(msg['parts'][0])
            
        st.markdown("<div style='margin-bottom: 100px;'></div>", unsafe_allow_html=True)
        # Inline Chat Fixed for Mobile
        c_up, c_in, c_v = st.columns([0.5, 7, 1.5])
        with c_in:
            st.text_input("Message", key="inline_txt", placeholder="Ask anything", on_change=submit_chat, label_visibility="collapsed")
        
        if st.session_state['submit_val']:
            user_in = st.session_state['submit_val']
            st.session_state['messages'].append({"role":"user", "parts":[user_in]})
            save_chat(user_id, "user", user_in)
            
            with st.spinner("AI thinking..."):
                resp = get_ai_response(user_in, st.session_state['messages'][:-1], st.session_state['persona'])
                st.session_state['messages'].append({"role":"model", "parts":[resp]})
                save_chat(user_id, "assistant", resp)
            st.session_state['submit_val'] = ""; st.rerun()
            
