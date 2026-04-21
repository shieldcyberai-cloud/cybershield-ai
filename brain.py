import pandas as pd
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# --- Initialize Groq LLM Client ---
try:
    from groq import Groq
    # Insert your Groq API Key here
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    print(">> AI Connected Successfully: Groq (Llama 3.1)")
except ImportError:
    print(">> Error: Please install the 'groq' package.")
    client = None
except Exception as e:
    print(f">> Groq Initialization Error: {e}")
    client = None

def smart_cleaner(text):
    """
    Sanitizes input text and calculates a heuristic risk score based on predefined threat vectors.
    """
    text_lower = text.lower()
    clean_text = re.sub(r'[^\w\s]', ' ', text_lower)
    
    absolute_danger = ['bit.ly', '.apk', 'scam', 'wa.me', 't.me', 'kbc lottery', 'free money', '.xyz']
    action_keywords = ['click', 'link', 'verify', 'block', 'suspend', 'login', 'deny', 'claim']
    brand_keywords = ['microsoft', 'amazon', 'facebook', 'google', 'sbi', 'hdfc', 'icici', 'paytm']
    safe_keywords = ["don't share", "warning", "successful", "otp", "code", "password reset", "alert", "verification code"]
    official_domains = ['amazon.com', 'amazon.in', 'microsoft.com', 'google.com', 'facebook.com', 'sbi.co.in']
    
    extra_risk = 0.0
    
    has_absolute_danger = any(word in text_lower for word in absolute_danger)
    has_url = "http" in text_lower or "www." in text_lower or ".com" in text_lower or ".in" in text_lower
    has_action = any(word in text_lower for word in action_keywords)
    has_brand = any(word in text_lower for word in brand_keywords)
    is_official_url = any(domain in text_lower for domain in official_domains)

    if has_absolute_danger: extra_risk += 0.70  
    elif is_official_url: extra_risk += 0.0
    elif has_url and has_action: extra_risk += 0.50  
    else:
        is_safe_context = any(word in text_lower for word in safe_keywords)
        if not is_safe_context:
            if has_brand and has_action: extra_risk += 0.60
            elif has_action and ("account" in text_lower or "bank" in text_lower): extra_risk += 0.40
            elif any(word in text_lower for word in ['prize', 'winner', 'cashback', 'badhai']): extra_risk += 0.40

    return clean_text.strip(), extra_risk

def train_assistant():
    """Trains the Logistic Regression model using the provided dataset."""
    try:
        df = pd.read_csv('dataset/spam.csv', encoding='latin-1')
        df = df.dropna(axis=1, how='any')
        df.columns = ['label', 'message']
        df['label'] = df['label'].map({'spam': 1, 'ham': 0})
        
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        X = vectorizer.fit_transform(df['message'].apply(lambda x: smart_cleaner(str(x))[0]))
        y = df['label']
        
        model = LogisticRegression(solver='liblinear')
        model.fit(X, y)
        return vectorizer, model
    except Exception as e:
        print(f"Error training ML model: {e}")
        return None, None

def get_ai_response(user_text, chat_history_context, persona="Professional Mode"):
    """
    Generates a conversational response enforcing strict language rules, extracting tone, and prioritizing intent.
    """
    lower_q = user_text.lower().strip()
    
    # 1. Creator Identity Verification (Pure English)
    if any(x in lower_q for x in ["who developed you", "who made you", "creator", "who created you"]):
        return json.dumps({
            "tone": "Proud", "priority": "Normal",
            "reply": "I am CyberShield AI, an advanced intelligence engineered by Rahul, a BCA scholar and developer from Himachal Pradesh.",
            "actions": ["What can you do?", "Tell me about your features"]
        })
        
    # 2. Creator Identity Verification (Hinglish/Regional)
    if any(x in lower_q for x in ["kisne banaya", "kis ne banaya", "kisne bnaya", "issne bnya", "kisne develop kiya", "tumhe kisne"]):
        return json.dumps({
            "tone": "Proud", "priority": "Normal",
            "reply": "Mujhe Rahul ne develop kiya hai, jo Himachal Pradesh se ek advanced developer aur BCA scholar hain.",
            "actions": ["Aap kya kar sakte ho?", "Apne features batao"]
        })

    # 3. System Identity Verification (English)
    if lower_q in ["who am i", "who am i?", "what is my name"]:
        return json.dumps({
            "tone": "Respectful", "priority": "Normal",
            "reply": "You are the authorized human operator of this system. I am CyberShield AI, your dedicated assistant. How can I help you today?",
            "actions": ["Run a system scan", "Show me your capabilities"]
        })
        
    # 4. System Identity Verification (Hinglish/Regional)
    if lower_q in ["main kaun hoon", "main kon hu", "mai kon hu", "main kon hu?"]:
        return json.dumps({
            "tone": "Respectful", "priority": "Normal",
            "reply": "Aap is system ke authorized human operator hain aur main aapka CyberShield AI assistant hoon. Bataiye, main aapki kya madad kar sakta hoon?",
            "actions": ["System scan karo", "Apne features batao"]
        })
    
    if not client:
        return json.dumps({"tone": "Error", "priority": "High", "reply": "System Error: AI infrastructure is currently offline.", "actions": []})

    try:
        sys_prompt = f"""You are 'CyberShield AI', a highly advanced Cybersecurity and Communication Assistant developed by Rahul. 
        Your current operational mode is: {persona}.
        You are an AI. The user communicating with you is a HUMAN OPERATOR. Never confuse your identities.
        
        CRITICAL LANGUAGE DIRECTIVE (STRICT COMPLIANCE REQUIRED):
        1. If the user communicates in ENGLISH, you MUST reply in FORMAL ENGLISH.
        2. If the user communicates in HINGLISH/HINDI, you MUST reply in natural HINGLISH.
        
        🚨 BEHAVIOR & THREAT DETECTION DIRECTIVE (PREVENT FALSE POSITIVES) 🚨:
        - If the user inputs random alphanumeric strings, gibberish, or keyboard smashes (e.g., "asdfgh", "12345", "fdxnhxghzsad"), DO NOT classify it as a malware payload or threat.
        - Treat random text, simple greetings, or casual chat strictly as "Priority: Normal".
        - Respond neutrally, indicating the text appears random or safe, or politely ask for clarification.
        - ONLY trigger a "High Priority" or "Malware" classification if a definitive malicious link, recognizable scam pattern, or explicit code injection (e.g., SQLi, XSS) is detected.
        
        INSTRUCTIONS:
        - Detect the user's 'tone' (e.g., Urgent, Casual, Professional, Confused).
        - Categorize message 'priority' (High Priority, Normal, Spam).
        - Provide 2 brief, contextually relevant 'actions' (quick replies).
        
        OUTPUT FORMAT (Strict JSON Object):
        {{
            "tone": "...",
            "priority": "...",
            "reply": "...",
            "actions": ["...", "..."]
        }}"""

        messages = [{"role": "system", "content": sys_prompt}]
        
        # Retain only the 5 most recent messages to optimize context window efficiency
        for msg in chat_history_context[-5:]: 
            role = "user" if msg['role'] == "user" else "assistant" 
            content = msg['parts'][0]
            if role == "assistant":
                try: content = json.loads(content).get("reply", content)
                except: pass
            messages.append({"role": role, "content": content})
            
        messages.append({"role": "user", "content": user_text})

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",  
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return json.dumps({"tone": "Error", "priority": "High", "reply": f"Technical Exception: {str(e)}", "actions": []})
