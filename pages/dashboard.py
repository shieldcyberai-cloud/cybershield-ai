import streamlit as st

# ==================================================
# 🔒 SECURITY CHECK: Bina login ke dashboard access roko
# ==================================================
if not st.session_state.get('logged_in', False):
    st.switch_page("app.py")

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Dashboard | CyberShield AI", layout="wide", page_icon="📊")

# ==================================================
# 🎨 ENHANCED PROFESSIONAL CSS (MOBILE OPTIMIZED)
# ==================================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        
        /* Sidebar se default app/dashboard page links hatane ke liye */
        [data-testid="stSidebarNav"] { display: none !important; }
        
        /* Header ko transparent rakha hai taaki mobile ka menu (☰) button dikhta rahe */
        header { background: transparent !important; } 

        .stApp { 
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); 
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #f8fafc;
        }
        
        [data-testid="stSidebar"] { 
            background-color: rgba(2, 6, 23, 0.95) !important; 
            border-right: 1px solid rgba(255,255,255,0.05); 
        }
        
        .profile-container {
            text-align: center;
            padding: 20px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
        }
        
        .profile-name {
            font-size: 1.2rem;
            font-weight: 700;
            color: #f8fafc;
            margin-top: 10px;
            letter-spacing: 1px;
        }
        
        .profile-role {
            font-size: 0.9rem;
            color: #94a3b8;
        }
        
        .dash-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }
        
        .dash-card:hover {
            transform: translateY(-5px);
            border: 1px solid rgba(56, 189, 248, 0.3);
            box-shadow: 0 10px 20px rgba(56, 189, 248, 0.1);
        }
        
        .dash-number {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(to right, #ffffff, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 10px;
        }
        
        .dash-title {
            color: #cbd5e1;
            font-size: 1.1rem;
            font-weight: 600;
        }

        .section-header {
            font-size: 1.4rem;
            font-weight: 700;
            color: #38bdf8;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 1px solid rgba(56, 189, 248, 0.2);
            padding-bottom: 5px;
        }

        .upcoming-card {
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 15px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .cyber-image {
            border-radius: 15px;
            border: 1px solid rgba(56, 189, 248, 0.3);
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
            width: 100%;
            height: auto;
            max-height: 200px;
            object-fit: cover;
        }
        
        /* ==================================================
           📱 MOBILE RESPONSIVE FIXES
           ================================================== */
        @media (max-width: 768px) {
            h1, .hero-title { font-size: 1.8rem !important; }
            .dash-number { font-size: 2rem !important; }
            .dash-card { padding: 20px !important; margin-bottom: 15px !important;}
            
            div[data-testid="stHorizontalBlock"] {
                display: flex;
                flex-direction: column;
            }
            
            .mobile-action-buttons {
                margin-top: 20px;
                margin-bottom: 20px;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ==================================================
# 📌 SIDEBAR NAVIGATION & PROFILE
# ==================================================
username = st.session_state.get('user_info', {}).get('username', 'Operator').upper()

with st.sidebar:
    st.markdown(f"""
        <div class="profile-container">
            <img src="https://cdn-icons-png.flaticon.com/512/10046/10046755.png" width="80" style="border-radius: 50%; border: 2px solid #38bdf8; padding: 5px; background: rgba(0,0,0,0.5); margin-bottom:10px;">
            <div class="profile-name">{username}</div>
            <div class="profile-role">Secure Operative</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    if st.button("💬 Open AI Assistant", use_container_width=True, type="primary", key="side_ai"):
        st.switch_page("app.py")
        
    if st.button("📊 Scan Reports", use_container_width=True, key="side_rep"):
        st.info("Reports section coming soon!")
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state['logged_in'] = False
        st.switch_page("app.py")

# ==================================================
# 🏠 MAIN DASHBOARD CONTENT
# ==================================================

# 1. Official Header & Professional Digital Scan Image
head_c1, head_c2 = st.columns([1.5, 3.5])
with head_c1:
    # High quality Cyber / Matrix code scanning image
    st.markdown("""
        <img src="https://www.keepitrealonline.govt.nz/__data/assets/image/0021/45642/Spam,-scams,-maleware-and-phishing.png" class="cyber-image">
    """, unsafe_allow_html=True)
    
with head_c2:
    st.markdown(f"<h1 style='margin-top:10px;'>Welcome, Operative {username}! 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #cbd5e1; font-size: 1.1rem;'>CyberShield AI - Security Authorization Level 4.<br>Operational Telemetry & Threat Defense Overview.</p>", unsafe_allow_html=True)

# --- MOBILE FRIENDLY ACTION BUTTONS (DIRECTLY ON MAIN SCREEN) ---
st.markdown("<div class='mobile-action-buttons'></div>", unsafe_allow_html=True)
act_c1, act_c2, act_spacer = st.columns([1.5, 1.5, 2])
with act_c1:
    if st.button("💬 Launch Threat Scanner", use_container_width=True, type="primary"):
        st.switch_page("app.py")
with act_c2:
    if st.button("📊 View Full Reports", use_container_width=True):
         st.info("Analytics module compiling...")

st.markdown("<br>", unsafe_allow_html=True)

# 2. Platform Metrics (Detailed)
st.markdown("<div class='section-header'>Platform Critical Metrics</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="dash-card">
            <div class="dash-title">Total Payloads Scanned</div>
            <div class="dash-number">142</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="dash-card">
            <div class="dash-title">Threats Intercepted</div>
            <div class="dash-number" style="color: #ef4444; -webkit-text-fill-color: #ef4444;">12</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="dash-card">
            <div class="dash-title">System Defense Status</div>
            <div class="dash-number" style="background: #4ade80; -webkit-background-clip: text;">Optimal</div>
        </div>
    """, unsafe_allow_html=True)

# 3. Upcoming Protocols & Detailed Features
st.markdown("<div class='section-header'>Upcoming Security Protocols (Details)</div>", unsafe_allow_html=True)

up1, up2 = st.columns(2)
with up1:
    st.markdown("""
        <div class="upcoming-card">
            <div style="font-size: 35px; color: #38bdf8; background: rgba(56,189,248,0.1); padding: 10px; border-radius: 12px;">🌍</div>
            <div>
                <h4 style="margin: 0; font-weight:700;">Vector Map Deployment</h4>
                <p style="margin: 0; font-size: 13px; color: #94a3b8; line-height:1.4;">Interactive geospatial analysis of intercepted threat sources. Projected Q3 2026.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True) 

with up2:
    st.markdown("""
        <div class="upcoming-card">
            <div style="font-size: 35px; color: #a855f7; background: rgba(168,85,247,0.1); padding: 10px; border-radius: 12px;">📧</div>
            <div>
                <h4 style="margin: 0; font-weight:700;">Asset Leak Scanning</h4>
                <p style="margin: 0; font-size: 13px; color: #94a3b8; line-height:1.4;">Scheduled monitoring of registered operative emails against known public breaches.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
