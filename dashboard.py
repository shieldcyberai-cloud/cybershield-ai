import streamlit as st

# ==================================================
# 🔒 SECURITY CHECK: Bina login ke dashboard access roko
# ==================================================
if not st.session_state.get('logged_in', False):
    st.switch_page("app.py") # Agar login nahi hai toh wapas app.py par bhej do

# ==================================================
# 🎨 PROFESSIONAL DASHBOARD CSS
# ==================================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        
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
    </style>
""", unsafe_allow_html=True)

# ==================================================
# 📌 SIDEBAR NAVIGATION & PROFILE
# ==================================================
with st.sidebar:
    # Profile Section
    st.markdown("""
        <div class="profile-container">
            <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="100" style="border-radius: 50%; border: 2px solid #38bdf8;">
            <div class="profile-name">Bikram Singh</div>
            <div class="profile-role">BCA Final Year | App Developer</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation Buttons
    if st.button("💬 Message Integrity Chat", use_container_width=True):
        st.switch_page("app.py")
        
    if st.button("📊 Scan Reports", use_container_width=True):
        st.info("Reports section coming soon!")
        
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Logout
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state['logged_in'] = False
        st.switch_page("app.py")

# ==================================================
# 🏠 MAIN DASHBOARD CONTENT
# ==================================================
st.title("Welcome to your Dashboard! 🚀")
st.markdown("Here is a quick overview of your system's activity.")

st.markdown("<br>", unsafe_allow_html=True)

# Metrics/Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="dash-card">
            <div class="dash-title">Total Messages Scanned</div>
            <div class="dash-number">142</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="dash-card">
            <div class="dash-title">Threats Detected</div>
            <div class="dash-number">12</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="dash-card">
            <div class="dash-title">System Status</div>
            <div class="dash-number" style="background: #4ade80; -webkit-background-clip: text;">Secure</div>
        </div>
    """, unsafe_allow_html=True)
