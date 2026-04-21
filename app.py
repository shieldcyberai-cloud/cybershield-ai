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
        
        # Personalized Email Body
        body = f"Greetings {username},\n\nProtocol initiated.\n\nYour OTP for password recovery is: {otp_code}\n\nDo not share this authorization key with anyone."
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True, "Success"
    except Exception as e:
        print(f"OTP Transmission Error: {e}")
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
    """Triggers on 'Enter': saves input to state and clears the field."""
    st.session_state['submit_val'] = st.session_state['inline_txt']
    st.session_state['inline_txt'] = ""

# ==================================================
# 🎨 DYNAMIC CSS (WITH MOBILE RESPONSIVENESS)
# ==================================================
bg_css = ""
if not st.session_state['logged_in'] and st.session_state['public_page'] == "home":
    bg_css = """
    .stApp { 
        background: linear-gradient(135deg, rgba(2, 6, 23, 0.85) 0%, rgba(9, 9, 11, 0.85) 100%), 
                    url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    """
else:
    bg_css = """
    .stApp { 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
        background-size: cover;
        background-attachment: fixed;
    }
    """

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    {bg_css}
    
    h1, h2, h3, h4, h5, h6, p, span, li {{ font-family: 'Inter', sans-serif; color: #f8fafc; }}
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {{ 
        background-color: rgba(255, 255, 255, 0.05) !important; 
        color: #e2e8f0 !important; 
        border: 1px solid rgba(255, 255, 255, 0.1) !important; 
        border-radius: 12px;
    }}
    
    .stChatMessage {{ 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        border-radius: 16px; 
        padding: 15px; 
        margin-bottom: 15px; 
        background: rgba(255, 255, 255, 0.03); 
        backdrop-filter: blur(10px);
    }}
    
    button[kind="secondary"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 5px 10px !important;
    }}
    button[kind="secondary"]:hover {{
        color: #38bdf8 !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }}

    button[kind="primary"] {{ 
        width: 100%; 
        border-radius: 12px !important; 
        font-weight: 600 !important; 
        background: linear-gradient(135deg, #0ea5e9, #4f46e5) !important; 
        color: white !important; 
        border: none !important;
    }}
    button[kind="primary"]:hover {{ 
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(14, 165, 233, 0.4) !important; 
    }}

    div[role="radiogroup"] {{
        flex-direction: row;
        justify-content: center;
        gap: 15px;
        margin-bottom: 20px;
    }}
    div[role="radiogroup"] > label > div:first-child {{ display: none; }}
    div[role="radiogroup"] > label {{
        padding: 10px 20px !important;
        background: rgba(255,255,255,0.05) !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        cursor: pointer;
    }}
    div[role="radiogroup"] > label[data-checked="true"] {{
        background: rgba(14, 165, 233, 0.2) !important;
        border-color: #0ea5e9 !important;
        color: #38bdf8 !important;
    }}

    [data-testid="stSidebar"] {{ 
        background-color: rgba(2, 6, 23, 0.95) !important; 
        border-right: 1px solid rgba(255,255,255,0.05); 
    }}
    
    .glass-card {{
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }}
    
    .hero-title {{
        background: linear-gradient(to right, #ffffff, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        line-height: 1.1;
    }}

    /* ==================================================
       🚀 CUSTOM INLINE CHAT COMPONENT
       ================================================== */
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) {{
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 90% !important;
        max-width: 800px !important;
        background-color: #2f3136 !important; 
        border-radius: 30px !important;
        padding: 6px 10px !important;
        z-index: 9999 !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.5) !important;
        border: 1px solid rgba(255,255,255,0.03) !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) > div[data-testid="column"] {{
        width: auto !important;
        flex: 0 0 auto !important;
        min-width: 0 !important;
        padding: 0 !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) > div[data-testid="column"]:nth-child(2) {{
        flex: 1 1 100% !important; 
    }}

    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] {{
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] section {{
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] section > div,
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] section > small,
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploaderDropzoneInstructions"],
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] svg {{
        display: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] button {{
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        box-shadow: none !important;
        position: relative;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] button::after {{
        content: "＋";
        font-size: 26px !important;
        font-weight: 300 !important;
        color: #a1a1aa !important;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        visibility: visible !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) .stTextInput > div > div > input {{
        border: none !important;
        background: transparent !important;
        color: #f8fafc !important;
        padding-left: 10px !important;
        box-shadow: none !important;
        font-size: 15px !important;
        height: 40px !important;
        outline: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) .stTextInput > div > div > input:focus {{
        border: none !important;
        box-shadow: none !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) button[kind="primary"] {{
        background: #404249 !important; 
        color: #f8fafc !important;
        border-radius: 20px !important;
        padding: 0 14px !important;
        height: 36px !important;
        border: none !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }}

    /* ==================================================
       📱 MOBILE RESPONSIVE FIXES 
       ================================================== */
    @media (max-width: 768px) {{
        .hero-title {{
            font-size: 2.8rem !important;
            margin-top: 20px !important;
        }}
        p {{
            font-size: 1rem !important;
        }}
        .glass-card {{
            padding: 20px !important;
            margin-bottom: 10px !important;
        }}
        /* Fix Navigation buttons stacking and sizing on mobile */
        div[data-testid="column"] {{
            text-align: center !important;
            margin-bottom: 10px !important;
        }}
        button[kind="secondary"], button[kind="primary"] {{
            width: 100% !important;
            margin: 0 auto !important;
        }}
        /* Fix Chat Input Bar on mobile */
        div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) {{
            width: 95% !important;
            bottom: 15px !important;
            padding: 4px 6px !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) .stTextInput > div > div > input {{
            font-size: 14px !important;
            padding-left: 5px !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) button[kind="primary"] {{
            padding: 0 10px !important;
            font-size: 12px !important;
            height: 32px !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# --- CORE FUNCTIONS ---
def clean_text_for_speech(text):
    if not text: return ""
    text = re.sub(r'[*_#`~>\[\]]', '', text) 
    return text.strip()

def speak(text, priority="Normal"):
    if not text: return
    try:
        VOICE = "en-IN-NeerjaNeural"
        rate, pitch = "+5%", "+0Hz"
        if priority.lower() in ["high priority", "urgent", "high"]:
            rate, pitch = "+15%", "+10Hz" 
        filename = "temp_ai_voice.mp3"
        async def _generate_audio():
            communicate = edge_tts.Communicate(text, VOICE, rate=rate, pitch=pitch)
            await communicate.save(filename)
        asyncio.run(_generate_audio())
        with open(filename, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay="true" style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        os.remove(filename)
    except Exception as e:
        pass

def listen():
    st.toast("⚠️ Voice input is restricted in the Cloud Environment.")
    return ""

vectorizer, model = train_assistant()

# ====================================================
# 🚀 1. FRONTEND SYSTEM (LANDING PAGE OR INFO PAGES)
# ====================================================
if not st.session_state['logged_in']:
    
    if st.session_state['show_auth_page']:
        col_back, _ = st.columns([1, 5])
        with col_back:
            if st.button("← Back to Home", type="secondary"):
                st.session_state['show_auth_page'] = False
                st.rerun()
            
        st.markdown("<div style='margin-top: 5vh;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        with col2:
            st.markdown("""
            <div class="glass-card" style="padding: 40px; text-align:center; background: rgba(255,255,255,0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; backdrop-filter: blur(10px);">
                <div style='font-size: 40px; margin-bottom: 10px;'>🔐</div>
                <h2 style="margin-top:0; color: #f8fafc; font-weight: 800;">System Access</h2>
                <p style="color: #94a3b8; font-size: 14px; margin-bottom: 20px;">Authenticate to initialize session.</p>
            """, unsafe_allow_html=True)
            
            # --- PASSWORD RECOVERY PROTOCOL ---
            if st.session_state['auth_mode'] == "Forgot Password":
                st.markdown("<h4 style='color:#38bdf8;'>Password Recovery Protocol</h4>", unsafe_allow_html=True)
                
                if st.session_state['reset_step'] == 1:
                    e_reset = st.text_input("Enter Registered Secure Email", key="e_reset")
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    
                    if st.button("Send Recovery OTP", type="primary"):
                        # Added .strip() to fix mobile keyboard spaces
                        clean_e = e_reset.strip() if e_reset else ""
                        if clean_e:
                            fetched_username = get_username_by_email(clean_e)
                            
                            if fetched_username:
                                otp = str(random.randint(100000, 999999))
                                with st.spinner("Transmitting Authorization Code via secure channel..."):
                                    success, status_msg = send_otp_email(clean_e, otp, fetched_username)
                                    
                                    if success:
                                        st.session_state['reset_otp'] = otp
                                        st.session_state['reset_email'] = clean_e
                                        st.session_state['reset_step'] = 2
                                        st.success("✅ Authorization code dispatched to your email address.")
                                        st.rerun()
                                    elif status_msg == "DEV_MODE":
                                        st.session_state['reset_otp'] = otp
                                        st.session_state['reset_email'] = clean_e
                                        st.session_state['reset_step'] = 2
                                        st.warning(f"⚠️ SMTP Configuration Missing. (DEV TEST OTP: {otp})")
                                    else:
                                        st.error(f"❌ Transmission Error: {status_msg}")
                            else:
                                st.error("❌ Associated email address not found in Database Records.")
                        else:
                            st.warning("Please provide a valid email address.")
                            
                    if st.button("Cancel Recovery", type="secondary"):
                        st.session_state['auth_mode'] = "Login"
                        st.rerun()
                        
                elif st.session_state['reset_step'] == 2:
                    otp_inp = st.text_input("Enter 6-Digit Authorization Code", key="otp_inp")
                    new_pass = st.text_input("Enter New Access Key (Password)", type="password", key="n_pass")
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    if st.button("Reset Password", type="primary"):
                        if otp_inp.strip() == st.session_state['reset_otp']:
                            clean_n_pass = new_pass.strip() if new_pass else ""
                            if clean_n_pass:
                                if update_user_password(st.session_state['reset_email'], clean_n_pass):
                                    st.success("✅ Access Key Successfully Updated. You may now log in.")
                                    st.session_state['auth_mode'] = "Login"
                                    st.session_state['reset_step'] = 1
                                    st.rerun()
                                else:
                                    st.error("❌ Email not found in Database Records.")
                            else:
                                st.warning("Access key cannot be empty.")
                        else:
                            st.error("❌ Invalid Authorization Code.")
                    if st.button("Cancel Recovery", type="secondary"):
                        st.session_state['auth_mode'] = "Login"
                        st.session_state['reset_step'] = 1
                        st.rerun()

            else:
                # --- AUTHENTICATION TABS (LOGIN / REGISTRATION) ---
                
default_index = 0 if st.session_state['auth_mode'] == "Login" else 1

auth_choice = st.radio("Auth Action", ["Login", "Register New Node"], index=default_index, label_visibility="collapsed")


# Custom Modules 
from db_controller import init_db, register_user, login_user, save_chat, get_user_chats, clear_user_chats, update_user_password, get_username_by_email
from brain import train_assistant, smart_cleaner, get_ai_response
from pages_content import show_architecture_page, show_terms_page, show_privacy_page, show_contact_page

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
        
        # Personalized Email Body
        body = f"Greetings {username},\n\nProtocol initiated.\n\nYour OTP for password recovery is: {otp_code}\n\nDo not share this authorization key with anyone."
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True, "Success"
    except Exception as e:
        print(f"OTP Transmission Error: {e}")
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
    """Triggers on 'Enter': saves input to state and clears the field."""
    st.session_state['submit_val'] = st.session_state['inline_txt']
    st.session_state['inline_txt'] = ""

# ==================================================
# 🎨 DYNAMIC CSS (WITH MOBILE RESPONSIVENESS)
# ==================================================
bg_css = ""
if not st.session_state['logged_in'] and st.session_state['public_page'] == "home":
    bg_css = """
    .stApp { 
        background: linear-gradient(135deg, rgba(2, 6, 23, 0.85) 0%, rgba(9, 9, 11, 0.85) 100%), 
                    url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    """
else:
    bg_css = """
    .stApp { 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
        background-size: cover;
        background-attachment: fixed;
    }
    """

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    {bg_css}
    
    h1, h2, h3, h4, h5, h6, p, span, li {{ font-family: 'Inter', sans-serif; color: #f8fafc; }}
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {{ 
        background-color: rgba(255, 255, 255, 0.05) !important; 
        color: #e2e8f0 !important; 
        border: 1px solid rgba(255, 255, 255, 0.1) !important; 
        border-radius: 12px;
    }}
    
    .stChatMessage {{ 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        border-radius: 16px; 
        padding: 15px; 
        margin-bottom: 15px; 
        background: rgba(255, 255, 255, 0.03); 
        backdrop-filter: blur(10px);
    }}
    
    button[kind="secondary"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 5px 10px !important;
    }}
    button[kind="secondary"]:hover {{
        color: #38bdf8 !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }}

    button[kind="primary"] {{ 
        width: 100%; 
        border-radius: 12px !important; 
        font-weight: 600 !important; 
        background: linear-gradient(135deg, #0ea5e9, #4f46e5) !important; 
        color: white !important; 
        border: none !important;
    }}
    button[kind="primary"]:hover {{ 
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(14, 165, 233, 0.4) !important; 
    }}

    div[role="radiogroup"] {{
        flex-direction: row;
        justify-content: center;
        gap: 15px;
        margin-bottom: 20px;
    }}
    div[role="radiogroup"] > label > div:first-child {{ display: none; }}
    div[role="radiogroup"] > label {{
        padding: 10px 20px !important;
        background: rgba(255,255,255,0.05) !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        cursor: pointer;
    }}
    div[role="radiogroup"] > label[data-checked="true"] {{
        background: rgba(14, 165, 233, 0.2) !important;
        border-color: #0ea5e9 !important;
        color: #38bdf8 !important;
    }}

    [data-testid="stSidebar"] {{ 
        background-color: rgba(2, 6, 23, 0.95) !important; 
        border-right: 1px solid rgba(255,255,255,0.05); 
    }}
    
    .glass-card {{
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }}
    
    .hero-title {{
        background: linear-gradient(to right, #ffffff, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        line-height: 1.1;
    }}

    /* ==================================================
       🚀 CUSTOM INLINE CHAT COMPONENT
       ================================================== */
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) {{
        position: fixed !important;
        bottom: 25px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 90% !important;
        max-width: 800px !important;
        background-color: #2f3136 !important; 
        border-radius: 30px !important;
        padding: 6px 10px !important;
        z-index: 9999 !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        flex-wrap: nowrap !important;
        gap: 5px !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.5) !important;
        border: 1px solid rgba(255,255,255,0.03) !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) > div[data-testid="column"] {{
        width: auto !important;
        flex: 0 0 auto !important;
        min-width: 0 !important;
        padding: 0 !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) > div[data-testid="column"]:nth-child(2) {{
        flex: 1 1 100% !important; 
    }}

    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] {{
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] section {{
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] section > div,
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] section > small,
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploaderDropzoneInstructions"],
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] svg {{
        display: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] button {{
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        box-shadow: none !important;
        position: relative;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) [data-testid="stFileUploader"] button::after {{
        content: "＋";
        font-size: 26px !important;
        font-weight: 300 !important;
        color: #a1a1aa !important;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        visibility: visible !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) .stTextInput > div > div > input {{
        border: none !important;
        background: transparent !important;
        color: #f8fafc !important;
        padding-left: 10px !important;
        box-shadow: none !important;
        font-size: 15px !important;
        height: 40px !important;
        outline: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) .stTextInput > div > div > input:focus {{
        border: none !important;
        box-shadow: none !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) button[kind="primary"] {{
        background: #404249 !important; 
        color: #f8fafc !important;
        border-radius: 20px !important;
        padding: 0 14px !important;
        height: 36px !important;
        border: none !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }}

    /* ==================================================
       📱 MOBILE RESPONSIVE FIXES 
       ================================================== */
    @media (max-width: 768px) {{
        .hero-title {{
            font-size: 2.8rem !important;
            margin-top: 20px !important;
        }}
        p {{
            font-size: 1rem !important;
        }}
        .glass-card {{
            padding: 20px !important;
            margin-bottom: 10px !important;
        }}
        /* Fix Navigation buttons stacking and sizing on mobile */
        div[data-testid="column"] {{
            text-align: center !important;
            margin-bottom: 10px !important;
        }}
        button[kind="secondary"], button[kind="primary"] {{
            width: 100% !important;
            margin: 0 auto !important;
        }}
        /* Fix Chat Input Bar on mobile */
        div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) {{
            width: 95% !important;
            bottom: 15px !important;
            padding: 4px 6px !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) .stTextInput > div > div > input {{
            font-size: 14px !important;
            padding-left: 5px !important;
        }}
        div[data-testid="stHorizontalBlock"]:has(input[placeholder="Ask anything"]) button[kind="primary"] {{
            padding: 0 10px !important;
            font-size: 12px !important;
            height: 32px !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# --- CORE FUNCTIONS ---
def clean_text_for_speech(text):
    if not text: return ""
    text = re.sub(r'[*_#`~>\[\]]', '', text) 
    return text.strip()

def speak(text, priority="Normal"):
    if not text: return
    try:
        VOICE = "en-IN-NeerjaNeural"
        rate, pitch = "+5%", "+0Hz"
        if priority.lower() in ["high priority", "urgent", "high"]:
            rate, pitch = "+15%", "+10Hz" 
        filename = "temp_ai_voice.mp3"
        async def _generate_audio():
            communicate = edge_tts.Communicate(text, VOICE, rate=rate, pitch=pitch)
            await communicate.save(filename)
        asyncio.run(_generate_audio())
        with open(filename, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<audio autoplay="true" style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        os.remove(filename)
    except Exception as e:
        pass

def listen():
    st.toast("⚠️ Voice input is restricted in the Cloud Environment.")
    return ""

vectorizer, model = train_assistant()

# ====================================================
# 🚀 1. FRONTEND SYSTEM (LANDING PAGE OR INFO PAGES)
# ====================================================
if not st.session_state['logged_in']:
    
    if st.session_state['show_auth_page']:
        col_back, _ = st.columns([1, 5])
        with col_back:
            if st.button("← Back to Home", type="secondary"):
                st.session_state['show_auth_page'] = False
                st.rerun()
            
        st.markdown("<div style='margin-top: 5vh;'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.2, 1])
        
        with col2:
            st.markdown("""
            <div class="glass-card" style="padding: 40px; text-align:center; background: rgba(255,255,255,0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; backdrop-filter: blur(10px);">
                <div style='font-size: 40px; margin-bottom: 10px;'>🔐</div>
                <h2 style="margin-top:0; color: #f8fafc; font-weight: 800;">System Access</h2>
                <p style="color: #94a3b8; font-size: 14px; margin-bottom: 20px;">Authenticate to initialize session.</p>
            """, unsafe_allow_html=True)
            
            # --- PASSWORD RECOVERY PROTOCOL ---
            if st.session_state['auth_mode'] == "Forgot Password":
                st.markdown("<h4 style='color:#38bdf8;'>Password Recovery Protocol</h4>", unsafe_allow_html=True)
                
                if st.session_state['reset_step'] == 1:
                    e_reset = st.text_input("Enter Registered Secure Email", key="e_reset")
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    
                    if st.button("Send Recovery OTP", type="primary"):
                        # Added .strip() to fix mobile keyboard spaces
                        clean_e = e_reset.strip() if e_reset else ""
                        if clean_e:
                            fetched_username = get_username_by_email(clean_e)
                            
                            if fetched_username:
                                otp = str(random.randint(100000, 999999))
                                with st.spinner("Transmitting Authorization Code via secure channel..."):
                                    success, status_msg = send_otp_email(clean_e, otp, fetched_username)
                                    
                                    if success:
                                        st.session_state['reset_otp'] = otp
                                        st.session_state['reset_email'] = clean_e
                                        st.session_state['reset_step'] = 2
                                        st.success("✅ Authorization code dispatched to your email address.")
                                        st.rerun()
                                    elif status_msg == "DEV_MODE":
                                        st.session_state['reset_otp'] = otp
                                        st.session_state['reset_email'] = clean_e
                                        st.session_state['reset_step'] = 2
                                        st.warning(f"⚠️ SMTP Configuration Missing. (DEV TEST OTP: {otp})")
                                    else:
                                        st.error(f"❌ Transmission Error: {status_msg}")
                            else:
                                st.error("❌ Associated email address not found in Database Records.")
                        else:
                            st.warning("Please provide a valid email address.")
                            
                    if st.button("Cancel Recovery", type="secondary"):
                        st.session_state['auth_mode'] = "Login"
                        st.rerun()
                        
                elif st.session_state['reset_step'] == 2:
                    otp_inp = st.text_input("Enter 6-Digit Authorization Code", key="otp_inp")
                    new_pass = st.text_input("Enter New Access Key (Password)", type="password", key="n_pass")
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    if st.button("Reset Password", type="primary"):
                        if otp_inp.strip() == st.session_state['reset_otp']:
                            clean_n_pass = new_pass.strip() if new_pass else ""
                            if clean_n_pass:
                                if update_user_password(st.session_state['reset_email'], clean_n_pass):
                                    st.success("✅ Access Key Successfully Updated. You may now log in.")
                                    st.session_state['auth_mode'] = "Login"
                                    st.session_state['reset_step'] = 1
                                    st.rerun()
                                else:
                                    st.error("❌ Email not found in Database Records.")
                            else:
                                st.warning("Access key cannot be empty.")
                        else:
                            st.error("❌ Invalid Authorization Code.")
                    if st.button("Cancel Recovery", type="secondary"):
                        st.session_state['auth_mode'] = "Login"
                        st.session_state['reset_step'] = 1
                        st.rerun()

            else:
                # --- AUTHENTICATION TABS (LOGIN / REGISTRATION) ---
                default_index = 0 if st.session_state['auth_mode'] == "Login" else 1
                auth_choice = st.radio("Auth Action", ["Login", "Register New Node"], index=default_index, label_visibility="collapsed")
                
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                
                if auth_choice == "Register New Node":
                    u = st.text_input("Operator ID (Username)", key="reg_u")
                    e = st.text_input("Secure Email", key="reg_e")
                    p = st.text_input("Access Key (Password)", type='password', key="reg_p")
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    if st.button("Initialize Platform", type="primary", key="reg_btn"):
                        # Added .strip() to fix mobile keyboard spaces
                        clean_u = u.strip() if u else ""
                        clean_e = e.strip() if e else ""
                        clean_p = p.strip() if p else ""
                        success, msg = register_user(clean_u, clean_e, clean_p)
                        if success: 
                            st.success(msg)
                            st.session_state['auth_mode'] = "Login" 
                            st.rerun()
                        else: st.error(msg)
                        
                else: 
                    u_log = st.text_input("Operator ID", key="login_u")
                    p_log = st.text_input("Access Key", type='password', key="login_p")
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    if st.button("Authenticate Sequence", type="primary", key="log_btn"):
                        # Added .strip() to fix mobile keyboard spaces
                        clean_u_log = u_log.strip() if u_log else ""
                        clean_p_log = p_log.strip() if p_log else ""
                        user = login_user(clean_u_log, clean_p_log)
                        if user:
                            st.session_state['logged_in'] = True
                            st.session_state['user_info'] = user
                            db_chats = get_user_chats(user['id'])
                            st.session_state['messages'] = [{"role": ("user" if c['role']=="user" else "model"), "parts": [c['message']]} for c in db_chats]
                            st.rerun()
                        else: 
                            st.error("Authentication Denied.")
                    
                    st.markdown("<div style='text-align:center; margin-top:10px;'>", unsafe_allow_html=True)
                    if st.button("Forgot Password?", type="secondary", key="forgot_btn"):
                        st.session_state['auth_mode'] = "Forgot Password"
                        st.session_state['reset_step'] = 1
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                    
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state['public_page'] == "about":
        show_architecture_page()

    elif st.session_state['public_page'] == "terms":
        show_terms_page()

    elif st.session_state['public_page'] == "privacy":
        show_privacy_page()
        
    elif st.session_state['public_page'] == "contact":
        show_contact_page()

    else:
        # --- LANDING PAGE INTEGRATION ---
        nav_c1, nav_spacer, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns([3, 2, 1.2, 1.3, 1, 1.2])
        
        with nav_c1:
            st.markdown("""
            <div style='display: flex; align-items: center; gap: 10px;'>
                <div style='background: #0ea5e9; padding: 6px; border-radius: 8px; font-size: 20px;'>🛡️</div>
                <h3 style='margin:0; font-weight: 800;'>CyberShield<span style='color:#38bdf8;'>.AI</span></h3>
            </div>
            """, unsafe_allow_html=True)
        with nav_spacer: st.write("") 
        with nav_c2:
            st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
            if st.button("Architecture", type="secondary", key="nav_arch"): 
                st.session_state['public_page'] = "about"; st.rerun()
        with nav_c3:
            st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
            if st.button("👤 Contact us", type="secondary", key="nav_contact"): 
                st.session_state['public_page'] = "contact"; st.rerun()
        with nav_c4:
            st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
            if st.button("Sign in", type="secondary", key="nav_signin"):
                st.session_state['show_auth_page'] = True; st.session_state['auth_mode'] = "Login"; st.rerun()
        with nav_c5:
            if st.button("Sign up", key="nav_signup", type="primary"):
                st.session_state['show_auth_page'] = True; st.session_state['auth_mode'] = "Register New Node"; st.rerun()
                
        st.markdown("""<div style="height: 2px; background: linear-gradient(90deg, transparent, #10b981, transparent); box-shadow: 0 0 15px #10b981; margin-top: 10px; margin-bottom: 20px;"></div>""", unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 10vh;'></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; margin-bottom: 20px;'><span style='background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #10b981; padding: 6px 15px; border-radius: 20px; font-size: 13px; font-weight: 600;'>🟢 Core Systems Operational</span></div>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>Intelligence Meets<br>Cyber Defense</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 1.2rem; max-width: 600px; margin: 0 auto 40px auto;'>A next-generation neural platform integrating real-time threat scanning, optical extraction, and an adaptive LLM operative.</p>", unsafe_allow_html=True)
        
        btn_c1, btn_c2, btn_c3, btn_c4 = st.columns([1, 0.8, 0.8, 1])
        with btn_c2:
            if st.button("Initialize Scan 🚀", key="hero_start", type="primary"): st.session_state['show_auth_page'] = True; st.rerun()
        with btn_c3:
            if st.button("View Documentation", type="secondary", key="hero_doc"): st.session_state['public_page'] = "about"; st.rerun()
                
        st.markdown("<div style='margin-top: 20vh;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; margin-bottom: 40px;'>Architected for <span style='color:#38bdf8;'>Security</span></h2>", unsafe_allow_html=True)
        
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        with f_col1:
            st.markdown("""
            <div class="glass-card">
                <div style="font-size: 30px; margin-bottom: 10px;">⚡</div>
                <div style="font-weight: bold; font-size: 18px; margin-bottom: 10px;">Real-Time ML</div>
                <div style="color: #94a3b8; font-size: 14px;">Vector models instantly intercept Phishing & Spam payloads.</div>
            </div>
            """, unsafe_allow_html=True)
        with f_col2:
            st.markdown("""
            <div class="glass-card">
                <div style="font-size: 30px; margin-bottom: 10px;">🧠</div>
                <div style="font-weight: bold; font-size: 18px; margin-bottom: 10px;">Cyber Operative</div>
                <div style="color: #94a3b8; font-size: 14px;">Adaptive AI companion engineered for security intelligence.</div>
            </div>
            """, unsafe_allow_html=True)
        with f_col3:
            st.markdown("""
            <div class="glass-card">
                <div style="font-size: 30px; margin-bottom: 10px;">👁️</div>
                <div style="font-weight: bold; font-size: 18px; margin-bottom: 10px;">Neural Vision</div>
                <div style="color: #94a3b8; font-size: 14px;">EasyOCR extracts hidden text-based threats in imagery.</div>
            </div>
            """, unsafe_allow_html=True)
        with f_col4:
            st.markdown("""
            <div class="glass-card">
                <div style="font-size: 30px; margin-bottom: 10px;">🔐</div>
                <div style="font-weight: bold; font-size: 18px; margin-bottom: 10px;">Zero-Trust DB</div>
                <div style="color: #94a3b8; font-size: 14px;">Encrypted persistence ensuring data remains secure.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin-top: 80px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        foot_left, foot_spacer, foot_link1, foot_link2, foot_link3 = st.columns([5, 2, 1.5, 1.5, 1.5])
        
        with foot_left:
            st.markdown("<p style='color:#94a3b8; font-size:14px;'>© 2026 CyberShield Intelligence. All rights reserved.</p>", unsafe_allow_html=True)
            
        with foot_link1:
            if st.button("Terms", type="secondary", key="ft_terms"): 
                st.session_state['public_page'] = "terms"; st.rerun()
        with foot_link2:
            if st.button("Privacy", type="secondary", key="ft_priv"): 
                st.session_state['public_page'] = "privacy"; st.rerun()
        with foot_link3:
            if st.button("Contact", type="secondary", key="ft_contact"): 
                st.session_state['public_page'] = "contact"; st.rerun()

# ====================================================
# 🛡️ 2. MAIN CYBERSHIELD DASHBOARD (AUTHENTICATED)
# ====================================================
else:
    user_id = st.session_state['user_info']['id']
    username = st.session_state['user_info']['username']

    with st.sidebar:
        st.markdown(f"""
            <div style='text-align: center; padding: 20px 0;'>
                <div style='width: 80px; height: 80px; border-radius: 50%; border: 2px solid #38bdf8; display: inline-flex; align-items: center; justify-content: center; margin: 0 auto;'>
                    <span style="font-size: 35px;">👤</span>
                </div>
                <h3 style='margin-top: 15px; margin-bottom: 8px; color: #f8fafc;'>{username.upper()}</h3>
                <span style='color: #10b981; font-size: 12px; font-weight: bold;'>● SECURE OPERATIVE</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        st.session_state['persona'] = st.selectbox("Operational Mode", ["Professional Mode", "Friendly Mode", "Sarcastic Mode"])
        
        st.markdown("<br><b>Navigation</b>", unsafe_allow_html=True)
        current_index = 0 if st.session_state['nav_view'] == "Threat Scanner" else 1
        selected_nav = st.radio("Select View:", ["Threat Scanner", "Cyber Assistant"], index=current_index, label_visibility="collapsed")
        
        if selected_nav != st.session_state['nav_view']:
            st.session_state['nav_view'] = selected_nav
            st.rerun()
        
        st.write("---")
        if st.button("✨ New Session", type="secondary"):
            st.session_state['messages'] = [] 
            st.rerun() 
            
        if st.button("🗑️ Purge Telemetry", type="secondary"):
            clear_user_chats(user_id)            
            st.session_state['messages'] = []    
            st.toast("Logs securely erased.")  
            st.rerun()                                    
        
        st.write("---")
        if st.button("Logout", type="secondary"):
            st.session_state['logged_in'] = False
            st.session_state['show_auth_page'] = False 
            st.session_state['public_page'] = "home"
            st.session_state['messages'] = []
            st.session_state['nav_view'] = "Threat Scanner"
            st.rerun()

    if st.session_state['nav_view'] == "Threat Scanner":
        st.markdown("<h2>Message Integrity Assessment</h2>", unsafe_allow_html=True)
        
        with st.expander("📷 Optical Character Recognition (Scan Image)"):
            uploaded_file = st.file_uploader("Upload Image Payload", type=["jpg", "png", "jpeg"])
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, width=300)
                if st.button("Execute Extraction", type="primary"):
                    with st.spinner("Decoding image payload..."):
                        img_array = np.array(image)
                        results = reader.readtext(img_array)
                        full_text = " ".join([res[1] for res in results])
                        st.session_state['extracted_text'] = full_text
                        st.rerun()

        msg_box = st.text_area("Input Text Payload:", value=st.session_state['extracted_text'], height=120)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Analyze Threat Level", type="primary"):
                if msg_box:
                    cleaned, extra_risk = smart_cleaner(msg_box)
                    if vectorizer and model:
                        vec = vectorizer.transform([cleaned])
                        base_prob = model.predict_proba(vec)[0][1]
                        
                        if len(cleaned.split()) <= 3 and extra_risk == 0.0: base_prob = 0.05
                        final_prob = min(base_prob + extra_risk, 1.0)
                        pct = round(final_prob * 100, 2)
                        
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number", value = pct,
                            number = {'suffix': "%", 'font': {'color': '#f8fafc'}},
                            title = {'text': "Threat Probability", 'font': {'color': '#94a3b8'}},
                            gauge = {
                                'axis': {'range': [0, 100], 'tickcolor': "#38bdf8"},
                                'bar': {'color': "#ef4444" if pct >= 70 else "#eab308" if pct >= 45 else "#10b981"},
                                'bgcolor': "rgba(255,255,255,0.05)", 'borderwidth': 0,
                                'steps': [
                                    {'range': [0, 45], 'color': "rgba(16, 185, 129, 0.1)"},
                                    {'range': [45, 70], 'color': "rgba(234, 179, 8, 0.1)"},
                                    {'range': [70, 100], 'color': "rgba(239, 68, 68, 0.1)"}]
                            }
                        ))
                        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "#f8fafc"}, height=250, margin=dict(l=20, r=20, t=40, b=20))
                        st.plotly_chart(fig, use_container_width=True)

                        if final_prob >= 0.70: 
                            st.error("CRITICAL THREAT DETECTED.")
                            speak("Alert. Critical threat detected in payload.", priority="High")
                        elif final_prob >= 0.45: 
                            st.warning("SUSPICIOUS ACTIVITY.")
                            speak("Caution. Payload exhibits suspicious patterns.")
                        else: 
                            st.success("PAYLOAD VERIFIED SAFE.")
                            speak("Scan complete. Payload is secure.")
        
        with c2:
            if st.button("Send to AI Assistant", type="primary"):
                if msg_box:
                    cleaned, extra_risk = smart_cleaner(msg_box)
                    pct = 0
                    if vectorizer and model:
                        vec = vectorizer.transform([cleaned])
                        base_prob = model.predict_proba(vec)[0][1]
                        if len(cleaned.split()) <= 3 and extra_risk == 0.0: base_prob = 0.05
                        final_prob = min(base_prob + extra_risk, 1.0)
                        pct = round(final_prob * 100, 2)
                    
                    st.session_state['auto_send_msg'] = f"🚨 [THREAT ANALYSIS REQUIRED]: Score {pct}%. Payload: '{msg_box}'"
                    st.session_state['nav_view'] = "Cyber Assistant"
                    st.rerun()

        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 40px 0 20px 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 25px; margin-top: 20px;">
            <h3 style="color: #38bdf8; font-size: 1.2rem; margin-top: 0; margin-bottom: 15px;">🛡️ Operational Guidelines & System Instructions</h3>
            <div style="margin-bottom: 15px;">
                <h4 style="color: #e2e8f0; font-size: 1rem; margin-bottom: 5px;">1. Payload Analysis Protocol</h4>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin-top: 0;">
                Input suspicious text payloads manually into the text area, or utilize the <strong>Optical Character Recognition (OCR)</strong> module to extract textual data directly from uploaded image evidence. Click <strong>"Analyze Threat Level"</strong> to initialize the heuristic Machine Learning engine.
                </p>
            </div>
            <div style="margin-bottom: 15px;">
                <h4 style="color: #e2e8f0; font-size: 1rem; margin-bottom: 5px;">2. AI Escalation Protocol</h4>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin-top: 0;">
                If a payload is flagged as suspicious, utilize the <strong>"Send to AI Assistant"</strong> directive. This will forward the raw payload directly to the Cyber Operative for deep contextual analysis.
                </p>
            </div>
            <div>
                <h4 style="color: #f87171; font-size: 1rem; margin-bottom: 5px;">3. Security & Compliance Notice</h4>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.6; margin-top: 0;">
                While all telemetry is processed securely, operators are advised <strong>not</strong> to input highly sensitive PII. The system is calibrated strictly for threat vector identification.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


    # ==================================================
    # 🤖 CYBER ASSISTANT MODULE
    # ==================================================
    elif st.session_state['nav_view'] == "Cyber Assistant":
        st.markdown(f"<h2>Cyber Assistant <span style='font-size:14px; color:#94a3b8;'>({st.session_state['persona']})</span></h2>", unsafe_allow_html=True)
        
        for msg in st.session_state['messages']:
            role = msg['role']
            with st.chat_message(role, avatar="👤" if role == "user" else "✨"):
                if role == "model":
                    try:
                        data = json.loads(msg['parts'][0])
                        st.markdown(data.get("reply", ""))
                    except:
                        st.markdown(msg['parts'][0])
                else:
                    display_text = msg['parts'][0]
                    if "I have uploaded an image evidence." in display_text:
                        try: 
                            clean_display = "📎 *Image Evidence Uploaded:*\n\n" + display_text.split("extracted from it: '")[1].split("'. Please analyze")[0]
                            display_text = clean_display
                        except: pass
                    elif "🚨 [THREAT ANALYSIS REQUIRED]" in display_text:
                        try: display_text = display_text.split("Payload: '")[1][:-1]
                        except: pass
                    st.markdown(display_text)

        st.markdown("<div style='margin-bottom: 100px;'></div>", unsafe_allow_html=True) 

        # --- CUSTOM INLINE CHAT COMPONENT ---
        c_upload, c_input, c_voice = st.columns([0.5, 7, 1.5])
        
        with c_upload:
            chat_img = st.file_uploader("Upload", type=["jpg", "png", "jpeg"], key="inline_vision", label_visibility="collapsed")
            if chat_img and "img_toast" not in st.session_state:
                st.toast("📎 Image Data Buffered. Input prompt and press 'Enter' to transmit.")
                st.session_state["img_toast"] = True
                
        with c_input:
            txt_input = st.text_input("Message", key="inline_txt", label_visibility="collapsed", placeholder="Ask anything", autocomplete="off", on_change=submit_chat)
            
        with c_voice:
            voice_input = listen() if st.button("ılı Voice", key="btn_voice", type="primary") else None

        final_in = None
        
        if st.session_state.get('auto_send_msg'): 
            final_in = st.session_state['auto_send_msg']
            st.session_state['auto_send_msg'] = None
            
        elif voice_input:
            final_in = voice_input
            
        elif st.session_state['submit_val'] != "":
            if chat_img is not None:
                with st.spinner("Cyber Vision Initialization: Analyzing image geometry..."):
                    img_view = Image.open(chat_img)
                    img_array = np.array(img_view)
                    results = reader.readtext(img_array)
                    extracted_txt = " ".join([res[1] for res in results])
                    
                    if extracted_txt.strip():
                        user_context = f"\n\nUser Directive: {st.session_state['submit_val']}"
                        final_in = f"I have uploaded an image evidence. Here is the text extracted from it: '{extracted_txt}'. Please analyze this for any cyber threats, phishing attempts, or explain what it means.{user_context}"
                    else:
                        st.error("Extraction Failed: No discernible text artifacts detected.")
                        final_in = st.session_state['submit_val']
                
                if "img_toast" in st.session_state: del st.session_state["img_toast"]
            
            else:
                final_in = st.session_state['submit_val']
                
            st.session_state['submit_val'] = "" 

        if final_in:
            st.session_state['messages'].append({"role": "user", "parts": [final_in]})
            save_chat(user_id, "user", final_in)
            
            with st.chat_message("user", avatar="👤"):
                display_user = final_in
                if "I have uploaded an image evidence." in display_user:
                    try: 
                        clean_display = "📎 *Image Evidence Uploaded:*\n\n" + display_user.split("extracted from it: '")[1].split("'. Please analyze")[0]
                        display_user = clean_display
                    except: pass
                elif "🚨 [THREAT ANALYSIS REQUIRED]" in display_user:
                    try: display_user = display_user.split("Payload: '")[1][:-1]
                    except: pass
                st.markdown(display_user)

            with st.spinner("Analyzing operational telemetry..."):
                reply_json_str = get_ai_response(final_in, st.session_state['messages'][:-1], st.session_state['persona'])
            
            st.session_state['messages'].append({"role": "model", "parts": [reply_json_str]})
            save_chat(user_id, "assistant", reply_json_str)
            
            with st.chat_message("model", avatar="✨"):
                try:
                    data = json.loads(reply_json_str)
                    st.markdown(f"**{data.get('tone', 'Neutral')} | Priority: {data.get('priority', 'Normal')}**")
                    reply_text = data.get("reply", "...")
                    st.markdown(reply_text)
                    if data.get("actions"): st.caption(f"⚡ Actions: {', '.join(data.get('actions', []))}")
                    speak(clean_text_for_speech(reply_text), priority=data.get("priority", "Normal"))
                except:
                    st.markdown(reply_json_str)
                    speak(clean_text_for_speech(reply_json_str))
