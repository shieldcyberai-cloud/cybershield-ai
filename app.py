import streamlit as st
import os
import asyncio
import edge_tts
import speech_recognition as sr
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

# --- Custom Modules ---
# Ensure these files (db_controller.py, brain.py, pages_content.py) are in the same folder
from db_controller import init_db, register_user, login_user, save_chat, get_user_chats, clear_user_chats, update_user_password, get_username_by_email
from brain import train_assistant, smart_cleaner, get_ai_response
from pages_content import show_architecture_page, show_terms_page, show_privacy_page, show_contact_page

# Initialize Database
init_db()

@st.cache_resource
def load_ocr_reader():
    """Initializes and caches the EasyOCR Engine."""
    return easyocr.Reader(['en', 'hi'])

reader = load_ocr_reader()

# --- CYBERSHIELD PAGE CONFIGURATION ---
st.set_page_config(page_title="CyberShield AI | Advanced Threat Detection", page_icon="🛡️", layout="wide")

# --- EMAIL OTP DISPATCH FUNCTION ---
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
states = {
    'logged_in': False, 'user_info': None, 'messages': [], 
    'extracted_text': "", 'persona': "Professional Mode", 
    'auto_send_msg': None, 'nav_view': "Threat Scanner", 
    'show_auth_page': False, 'auth_mode': "Login", 
    'reset_step': 1, 'public_page': "home", 'submit_val': ""
}
for key, value in states.items():
    if key not in st.session_state:
        st.session_state[key] = value

def submit_chat():
    st.session_state['submit_val'] = st.session_state['inline_txt']
    st.session_state['inline_txt'] = ""

# --- DYNAMIC CSS ---
bg_css = """
.stApp { 
    background: linear-gradient(135deg, rgba(2, 6, 23, 0.85) 0%, rgba(9, 9, 11, 0.85) 100%), 
                url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop'); 
    background-size: cover; background-position: center; background-attachment: fixed;
}
""" if not st.session_state['logged_in'] and st.session_state['public_page'] == "home" else """
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); background-attachment: fixed; }
"""

st.markdown(f"<style>{bg_css} ... (Rest of CSS) ... </style>", unsafe_allow_html=True) # CSS short for readability here

# --- CORE FUNCTIONS ---
def clean_text_for_speech(text):
    return re.sub(r'[*_#`~>\[\]]', '', text).strip() if text else ""

def speak(text, priority="Normal"):
    if not text: return
    try:
        VOICE = "en-IN-NeerjaNeural"
        rate = "+15%" if priority.lower() in ["high", "urgent"] else "+5%"
        filename = "temp_ai_voice.mp3"
        async def _gen():
            c = edge_tts.Communicate(text, VOICE, rate=rate)
            await c.save(filename)
        asyncio.run(_gen())
        with open(filename, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay="true" style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        os.remove(filename)
    except: pass

def listen():
    st.toast("⚠️ Voice input is restricted in Cloud Environment.")
    return ""

vectorizer, model = train_assistant()

# ====================================================
# 🚀 1. FRONTEND / AUTHENTICATION SYSTEM
# ====================================================
if not st.session_state['logged_in']:
    if st.session_state['show_auth_page']:
        if st.button("← Back to Home", type="secondary"):
            st.session_state['show_auth_page'] = False
            st.rerun()
            
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.markdown('<div class="glass-card" style="text-align:center;"><h2>System Access</h2>', unsafe_allow_html=True)
            
            # --- Forgot Password Flow ---
            if st.session_state['auth_mode'] == "Forgot Password":
                if st.session_state['reset_step'] == 1:
                    e_reset = st.text_input("Registered Email").strip()
                    if st.button("Send Recovery OTP", type="primary"):
                        user_name = get_username_by_email(e_reset)
                        if user_name:
                            otp = str(random.randint(100000, 999999))
                            success, status = send_otp_email(e_reset, otp, user_name)
                            if success or status == "DEV_MODE":
                                st.session_state['reset_otp'], st.session_state['reset_email'], st.session_state['reset_step'] = otp, e_reset, 2
                                st.rerun()
                        else: st.error("Email not found.")
                
                elif st.session_state['reset_step'] == 2:
                    otp_i = st.text_input("6-Digit OTP").strip()
                    n_p = st.text_input("New Password", type="password").strip()
                    if st.button("Reset Password", type="primary"):
                        if otp_i == st.session_state['reset_otp'] and n_p:
                            update_user_password(st.session_state['reset_email'], n_p)
                            st.session_state['auth_mode'], st.session_state['reset_step'] = "Login", 1
                            st.rerun()
                if st.button("Cancel"): 
                    st.session_state['auth_mode'] = "Login"; st.rerun()

            # --- Login / Register Flow ---
            else:
                choice = st.radio("Action", ["Login", "Register"], label_visibility="collapsed")
                if choice == "Register":
                    u, e, p = st.text_input("Username").strip(), st.text_input("Email").strip(), st.text_input("Password", type="password").strip()
                    if st.button("Initialize"):
                        s, m = register_user(u, e, p)
                        if s: st.session_state['auth_mode'] = "Login"; st.rerun()
                        else: st.error(m)
                else:
                    u_l, p_l = st.text_input("Operator ID").strip(), st.text_input("Access Key", type="password").strip()
                    if st.button("Authenticate"):
                        user = login_user(u_l, p_l)
                        if user:
                            st.session_state.update({'logged_in': True, 'user_info': user})
                            st.rerun()
                        else: st.error("Denied.")
                    if st.button("Forgot Password?", type="secondary"):
                        st.session_state['auth_mode'] = "Forgot Password"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Static Pages ---
    elif st.session_state['public_page'] == "about": show_architecture_page()
    elif st.session_state['public_page'] == "terms": show_terms_page()
    elif st.session_state['public_page'] == "privacy": show_privacy_page()
    elif st.session_state['public_page'] == "contact": show_contact_page()
    else:
        # --- Landing Page Content ---
        st.markdown("<h1 class='hero-title'>Intelligence Meets<br>Cyber Defense</h1>", unsafe_allow_html=True)
        if st.button("Initialize Scan 🚀", type="primary"): 
            st.session_state['show_auth_page'] = True; st.rerun()

# ====================================================
# 🛡️ 2. MAIN DASHBOARD (AUTHENTICATED)
# ====================================================
else:
    with st.sidebar:
        st.markdown(f"<h3>{st.session_state['user_info']['username'].upper()}</h3>", unsafe_allow_html=True)
        st.session_state['nav_view'] = st.radio("Navigation", ["Threat Scanner", "Cyber Assistant"])
        if st.button("Logout"):
            st.session_state.update({'logged_in': False, 'public_page': "home"}); st.rerun()

    if st.session_state['nav_view'] == "Threat Scanner":
        st.header("Message Integrity Assessment")
        up = st.file_uploader("Scan Image", type=["jpg", "png", "jpeg"])
        if up:
            res = reader.readtext(np.array(Image.open(up)))
            st.session_state['extracted_text'] = " ".join([r[1] for r in res])
        
        msg = st.text_area("Input Payload:", value=st.session_state['extracted_text'])
        if st.button("Analyze Threat", type="primary"):
            # Threat Analysis Logic...
            st.success("Scan Complete.")

    elif st.session_state['nav_view'] == "Cyber Assistant":
        st.header("Cyber Assistant")
        for m in st.session_state['messages']:
            with st.chat_message(m['role']): st.markdown(m['parts'][0])
        
        # Chat Logic...
        if prompt := st.chat_input("Ask CyberShield AI"):
            st.session_state['messages'].append({"role": "user", "parts": [prompt]})
            resp = get_ai_response(prompt, st.session_state['messages'][:-1], st.session_state['persona'])
            st.session_state['messages'].append({"role": "model", "parts": [resp]})
            st.rerun()
            
