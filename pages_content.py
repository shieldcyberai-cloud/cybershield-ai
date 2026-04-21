import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Core Email Transmission Function ---
def send_real_email(user_name, user_email, user_message):
    # 🚨 Insert Authentication Credentials Below 🚨
    SENDER_EMAIL = "shieldcyberai@gmail.com" 
    APP_PASSWORD = "fbel yyls ptlm secx" # Application-Specific Password
    RECEIVER_EMAIL = "shieldcyberai@gmail.com" 
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"🚨 CyberShield AI Support: Query from {user_name}"
        
        body = f"New Support Query Received:\n\nName: {user_name}\nEmail: {user_email}\n\nMessage:\n{user_message}"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(SENDER_EMAIL, APP_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Mail Transmission Failure: {e}")
        return False

# ----------------------------------------

def show_architecture_page():
    if st.button("← Return to Home", key="back_arch"): 
        st.session_state['public_page'] = "home"
        st.rerun()
        
    st.markdown("<h1 style='font-weight: 800; font-size: 3rem; margin-top: 15px;'>System <span style='color:#38bdf8;'>Architecture</span></h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:#f8fafc; font-weight:700;">1. Executive Summary & Mission Objective</h3>
        <p style="color:#94a3b8; font-size:15px; line-height:1.7;">CyberShield AI is an enterprise-grade threat-intelligence platform engineered to bridge the gap between complex cybersecurity telemetry and end-user accessibility. Designed as an advanced research prototype, it provides a unified, highly-scalable interface for real-time payload scanning, heuristic analysis, and AI-driven mitigation strategies.</p>
        <hr style="border-color: rgba(255,255,255,0.05); margin: 30px 0;">
        <h3 style="color:#f8fafc; font-weight:700;">2. Core Neural Components & Tech Stack</h3>
        <div style="display:flex; flex-direction:column; gap:15px; margin-top:20px;">
            <div style="background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; border-left: 4px solid #38bdf8;">
                <h4 style="margin:0 0 5px 0; color:#e2e8f0;">Heuristic ML Engine (Vector Classification)</h4>
                <p style="margin:0; color:#94a3b8; font-size:14px;">Utilizes Scikit-Learn based NLP vectorization frameworks (TF-IDF/CountVectorizer) to classify raw text payloads. The model calculates statistical threat probabilities for phishing, SQL injection attempts, and malicious spam in real-time with sub-millisecond latency.</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; border-left: 4px solid #818cf8;">
                <h4 style="margin:0 0 5px 0; color:#e2e8f0;">Vision OCR Subsystem (Image Extraction)</h4>
                <p style="margin:0; color:#94a3b8; font-size:14px;">Integrates the EasyOCR engine backed by OpenCV to extract hidden, obfuscated textual payloads from images. This counters modern steganographic delivery methods often utilized by Advanced Persistent Threats (APTs).</p>
            </div>
            <div style="background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; border-left: 4px solid #c084fc;">
                <h4 style="margin:0 0 5px 0; color:#e2e8f0;">Cyber Operative (LLM Integration)</h4>
                <p style="margin:0; color:#94a3b8; font-size:14px;">A context-aware AI assistant powered by state-of-the-art Large Language Models via API. It acts as an interactive SOC (Security Operations Center) analyst, explaining vulnerabilities, providing remediation steps, and generating real-time voice synthesis alerts via Edge-TTS.</p>
            </div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.05); margin: 30px 0;">
        <h3 style="color:#f8fafc; font-weight:700;">3. Data Flow Pipeline</h3>
        <p style="color:#94a3b8; font-size:15px; line-height:1.7;">When a payload is injected into the system, it undergoes a stringent multi-tier analysis: <br><b>Ingestion -> Sanitization (RegEx/Stopwords) -> Vectorization -> Probability Scoring -> LLM Contextualization -> User Dashboard.</b><br>All operations occur within a sandboxed environment to prevent arbitrary code execution on the host machine.</p>
    </div>
    """, unsafe_allow_html=True)

def show_terms_page():
    if st.button("← Return to Home", key="back_terms"): 
        st.session_state['public_page'] = "home"
        st.rerun()
        
    st.markdown("<h1 style='font-weight: 800; font-size: 3rem; margin-top: 15px;'>Terms of <span style='color:#38bdf8;'>Service</span></h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:#f8fafc; font-weight:700;">1. Protocol Acceptance & Binding Agreement</h3>
        <p style="color:#94a3b8; font-size:14px; margin-bottom: 20px;">By initializing a session, creating an operator account, or utilizing the API endpoints of the CyberShield AI network, you explicitly agree to adhere to these operational guidelines. If you do not agree with any part of these terms, you must immediately terminate your connection and purge local caches.</p>
        <h3 style="color:#f8fafc; font-weight:700;">2. Acceptable Use Policy (AUP)</h3>
        <p style="color:#94a3b8; font-size:14px; margin-bottom: 20px;">This platform is designated exclusively for <strong>defensive analysis, educational research, and preemptive threat detection</strong>. <br><br>Operators are strictly prohibited from:<br>• Utilizing the AI infrastructure to generate, obfuscate, or test malicious payloads intended for deployment.<br>• Reverse-engineering the Machine Learning models or attempting to poison the dataset.<br>• Employing automated scraping bots or performing Denial of Service (DoS) stress tests against the platform.</p>
        <h3 style="color:#f8fafc; font-weight:700;">3. System Limitations & Disclaimer of Warranties</h3>
        <p style="color:#94a3b8; font-size:14px; margin-bottom: 20px;">The ML Scanner and Cyber Operative provide <em>heuristic predictions</em> based on historically trained datasets. The platform is provided on an "AS IS" and "AS AVAILABLE" basis. We do not constitute an absolute guarantee of safety, nor do we claim a 100% detection rate for zero-day vulnerabilities. CyberShield AI is an analytical tool and should not act as a total replacement for enterprise Endpoint Detection and Response (EDR) hardware.</p>
        <h3 style="color:#f8fafc; font-weight:700;">4. Limitation of Liability</h3>
        <p style="color:#94a3b8; font-size:14px; margin-bottom: 20px;">Under no circumstances shall CyberShield Intelligence, its developers, or its affiliates be held liable for any indirect, incidental, consequential, or punitive damages arising from:<br>• Missed threat detections resulting in system compromise.<br>• Data loss or hardware failure resulting from user negligence.<br>• Actions taken by users based on the AI assistant's recommendations.</p>
        <h3 style="color:#f8fafc; font-weight:700;">5. Access Termination Rights</h3>
        <p style="color:#94a3b8; font-size:14px;">Administrators reserve the unreserved right to sever connections, blacklist IP ranges, and permanently purge account telemetry for any operator found violating these terms, engaging in hostile reconnaissance, or exhibiting anomalous operational behavior.</p>
    </div>
    """, unsafe_allow_html=True)

def show_privacy_page():
    if st.button("← Return to Home", key="back_priv"): 
        st.session_state['public_page'] = "home"
        st.rerun()
        
    st.markdown("<h1 style='font-weight: 800; font-size: 3rem; margin-top: 15px;'>Privacy <span style='color:#38bdf8;'>Architecture</span></h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:#f8fafc; font-weight:700;">Data Sovereignty & Zero-Trust Philosophy</h3>
        <p style="color:#94a3b8; font-size:15px; line-height:1.7;">CyberShield AI is architected on the foundational principle of Data Minimization and Zero-Trust. We do not harvest, sell, aggregate, or distribute operator telemetry to third-party data brokers, advertising agencies, or external analytical services. Your digital footprint remains strictly within the encrypted confines of the local deployment environment.</p>
        <hr style="border-color: rgba(255,255,255,0.05); margin: 30px 0;">
        <div style="display:flex; flex-direction:row; gap:20px; flex-wrap:wrap; margin-bottom: 20px;">
            <div style="flex: 1; min-width: 250px; background: rgba(0,0,0,0.3); padding: 25px; border-radius: 12px; border-top: 3px solid #38bdf8;">
                <span style="font-size: 28px; color:#38bdf8;">🔐</span>
                <h4 style="margin:15px 0 10px 0; color:#e2e8f0; font-weight:700;">Cryptographic Standards</h4>
                <p style="margin:0; color:#94a3b8; font-size:13px; line-height:1.6;">Operator access keys (passwords) are subjected to rigorous cryptographic hashing algorithms (such as bcrypt or SHA-256 with dynamic salting) prior to database injection. Raw credentials are never stored in plaintext. This ensures that even in the event of a total database breach, operator credentials remain mathematically impossible to reverse-engineer.</p>
            </div>
            <div style="flex: 1; min-width: 250px; background: rgba(0,0,0,0.3); padding: 25px; border-radius: 12px; border-top: 3px solid #10b981;">
                <span style="font-size: 28px; color:#10b981;">🗑️</span>
                <h4 style="margin:15px 0 10px 0; color:#e2e8f0; font-weight:700;">Ephemeral Processing</h4>
                <p style="margin:0; color:#94a3b8; font-size:13px; line-height:1.6;">Images uploaded via the OCR module and texts inputted into the ML Scanner are processed exclusively in volatile memory (RAM). Post-extraction and classification, the raw data structures are instantly garbage-collected by the backend. We maintain a zero-disk-write policy for scanned payloads.</p>
            </div>
        </div>
        <div style="display:flex; flex-direction:row; gap:20px; flex-wrap:wrap;">
            <div style="flex: 1; min-width: 250px; background: rgba(0,0,0,0.3); padding: 25px; border-radius: 12px; border-top: 3px solid #c084fc;">
                <span style="font-size: 28px; color:#c084fc;">👤</span>
                <h4 style="margin:15px 0 10px 0; color:#e2e8f0; font-weight:700;">Operator Data Rights & Purging</h4>
                <p style="margin:0; color:#94a3b8; font-size:13px; line-height:1.6;">Operators maintain ultimate and unilateral authority over their session telemetry. The 'Delete Chat Logs' command available on the main dashboard executes a hard cascade purge, permanently eradicating your conversation history, cached AI responses, and metadata from the SQL tables without any recovery option.</p>
            </div>
            <div style="flex: 1; min-width: 250px; background: rgba(0,0,0,0.3); padding: 25px; border-radius: 12px; border-top: 3px solid #f59e0b;">
                <span style="font-size: 28px; color:#f59e0b;">🌐</span>
                <h4 style="margin:15px 0 10px 0; color:#e2e8f0; font-weight:700;">Third-Party Integrations</h4>
                <p style="margin:0; color:#94a3b8; font-size:13px; line-height:1.6;">Interaction with the Cyber Operative utilizes secure API tunnels to external LLM providers. Only the specific chat prompt is transmitted via encrypted TLS 1.3 tunnels for response generation. No personally identifiable information (PII) or IP metadata is appended to these inference requests.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_contact_page():
    if st.button("← Return to Home", key="back_contact"): 
        st.session_state['public_page'] = "home"
        st.rerun()
        
    st.markdown("<h1 style='font-weight: 800; font-size: 3rem; margin-top: 15px;'>Support & <span style='color:#00b4d8;'>Contact</span></h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:#f8fafc; font-weight:700;">1. Operational Guidelines & Recommendations</h3>
        <p style="color:#94a3b8; font-size:15px; line-height:1.7;">Before escalating an issue to our Threat Intelligence team, please ensure you have followed the standard operational protocols:</p>
        <ul style="color:#94a3b8; font-size:14px; line-height:1.8; margin-bottom: 0;">
            <li><strong style='color:#f8fafc;'>Session Telemetry:</strong> Have your Operator ID ready for faster resolution.</li>
            <li><strong style='color:#f8fafc;'>False Positives:</strong> If the ML scanner misclassified a safe payload, note the Exact Threat Probability Score.</li>
            <li><strong style='color:#f8fafc;'>AI Anomalies:</strong> If the Cyber Operative responds unexpectedly, please use the 'Delete Chat Logs' function to reset the context window before reporting.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    
    # CSS Customization for the embedded dark framed container
    st.markdown("""
    <style>
    .contact-form-frame {
        background: rgba(255, 255, 255, 0.03);
        border: 2px solid rgba(255, 255, 255, 0.1); 
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        overflow: hidden;
    }
    
    .contact-form-frame input, .contact-form-frame textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 30px !important; 
        padding: 15px 20px 15px 45px !important; 
        color: white !important;
        font-size: 15px !important;
        width: 100%;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .contact-form-frame textarea {
        border-radius: 20px !important; 
        padding-top: 20px !important;
        min-height: 150px;
    }

    .contact-form-frame input:focus, .contact-form-frame textarea:focus {
        border-color: #00b4d8 !important;
        background-color: rgba(0, 180, 216, 0.05) !important;
        box-shadow: 0 0 10px rgba(0, 180, 216, 0.2) !important;
    }
    
    div[data-testid="stForm"] label {
        display: none !important;
    }

    [data-testid="stFormSubmitButton"] button {
        background: #00b4d8 !important; 
        color: white !important;
        border: none !important;
        border-radius: 30px !important; 
        font-weight: 700 !important;
        font-size: 16px !important;
        width: 100% !important;
        padding: 15px !important;
        margin-top: 10px !important;
        box-shadow: 0 4px 15px rgba(0, 180, 216, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        background: #0096b4 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 180, 216, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Native Streamlit Form utilizing custom CSS for inline icons
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("<div class='contact-form-frame'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #00b4d8; font-weight: 700; font-size: 2.5rem; margin-top: 0; margin-bottom: 30px;'>Contact us</h2>", unsafe_allow_html=True)
        
        with st.form("contact_form", clear_on_submit=True):
            st.markdown("<div style='position: relative;'><span style='position: absolute; left: 15px; top: 15px; z-index: 10; font-size: 18px;'>👤</span>", unsafe_allow_html=True)
            name = st.text_input("Name", placeholder="Name")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='position: relative; margin-top: -10px;'><span style='position: absolute; left: 15px; top: 15px; z-index: 10; font-size: 18px;'>📧</span>", unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="Email")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='position: relative; margin-top: -10px;'><span style='position: absolute; left: 15px; top: 15px; z-index: 10; font-size: 18px;'>📝</span>", unsafe_allow_html=True)
            msg = st.text_area("Message", placeholder="Message", height=150)
            st.markdown("</div>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Send Message")
            
            if submitted:
                if name and email and msg:
                    with st.spinner("Transmitting message..."):
                        is_sent = send_real_email(name, email, msg)
                        
                    if is_sent:
                        st.success(f"✅ Message dispatched successfully to shieldcyberai@gmail.com!")
                        st.balloons()
                    else:
                        st.error("❌ Transmission failed. Please verify SMTP configuration within the module.")
                else:
                    st.error("⚠️ All input fields are required.")
        st.markdown("</div>", unsafe_allow_html=True)
                    
    with col2:
        # Decorative illustration for visual alignment
        st.markdown("""
        <div style="height: 100%; display: flex; align-items: center; justify-content: center; padding: 20px;">
            <img src="https://img.freepik.com/free-vector/email-campaign-concept-illustration_114360-1633.jpg?w=740&t=st=1708849495~exp=1708850095~hmac=62d988d4073e527d42ea04581c8d50b4f8d3876101c518fb145520977224f8d4" style="width: 100%; max-width: 400px; border-radius: 20px; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));" alt="Contact Illustration">
        </div>
        """, unsafe_allow_html=True)