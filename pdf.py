from fpdf import FPDF

class ProjectSynopsis(FPDF):
    def __init__(self):
        super().__init__()
        # 1-inch margins (25.4 mm) on all sides
        self.set_margins(25.4, 25.4, 25.4)
        
    def header(self):
        pass
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Times', '', 10)
        
        # DEPARTMENT OF COMPUTER APPLICATIONS ab HAR PAGE par center mein aayega
        self.cell(0, 10, 'DEPARTMENT OF COMPUTER APPLICATIONS', align='C')
        
        # Page Numbering sirf Abstract (5th physical page) se shuru hogi
        if self.page_no() >= 5:
            actual_page_num = self.page_no() - 4
            self.set_x(-20)
            self.cell(0, 10, str(actual_page_num), align='R')

# Initialize PDF
pdf = ProjectSynopsis()
pdf.set_auto_page_break(auto=True, margin=25.4)

# ================= PAGE 1: COVER PAGE =================
pdf.add_page()
pdf.ln(10)
pdf.set_font('Times', 'B', 24)
pdf.cell(0, 15, 'SRI SAI UNIVERSITY', align='C', new_x="LMARGIN", new_y="NEXT") 
pdf.set_font('Times', '', 14)
pdf.cell(0, 10, 'Transforming Dreams into Reality', align='C', new_x="LMARGIN", new_y="NEXT") 
pdf.ln(25)

pdf.set_font('Times', 'B', 16)
pdf.cell(0, 10, 'SYNOPSIS', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 10, 'ON', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_font('Times', 'B', 18)
pdf.cell(0, 10, 'PROJECT "AI MESSAGE ASSISTANT"', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(30)

pdf.set_font('Times', '', 14)
pdf.cell(0, 8, 'In Partial Fulfilment', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'of', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Bachelor of Computer Applications (BCA)', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(35)

pdf.set_font('Times', 'B', 12)
pdf.cell(80, 8, 'Submitted to:')
pdf.cell(0, 8, 'Submitted By:', align='R', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Times', '', 12)
pdf.cell(80, 8, 'Mr. Nirbhay (A.P.)') 
pdf.cell(0, 8, 'Mr. Rahul', align='R', new_x="LMARGIN", new_y="NEXT")
pdf.cell(80, 8, '')
pdf.cell(0, 8, 'Roll No: 123011019', align='R', new_x="LMARGIN", new_y="NEXT")
pdf.cell(80, 8, '')
pdf.cell(0, 8, 'BCA (6TH Sem)', align='R', new_x="LMARGIN", new_y="NEXT")
pdf.ln(35)

pdf.set_font('Times', 'B', 14)
pdf.cell(0, 8, 'SRI SAI UNIVERSITY, PALAMPUR (H.P.)', align='C', new_x="LMARGIN", new_y="NEXT") 
# Cover page ka apna footer hٹا diya kyunki ab function automatically sab pe daal raha hai
pdf.cell(0, 8, 'SESSION (2023-2026)', align='C', new_x="LMARGIN", new_y="NEXT") 

# ================= PAGE 2: CERTIFICATE =================
pdf.add_page()
pdf.set_font('Times', 'B', 16)
pdf.cell(0, 10, 'CERTIFICATE', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

cert_text = """This is to certify that the project entitled **"AI MESSAGE ASSISTANT"** is a bonafide work carried out by **Mr. RAHUL** , Roll No. 123011019, **a student of Bachelor of Computer Applications (BCA), 6th Semester**, during the academic session **2025-2026**.

The work has been completed under the guidance of **Mr. Nirbhay (A.P.) (Internal Guide)** and **Mr. Vishal Sharma (External Guide)** in partial fulfillment of the requirements for the award of the degree of **Bachelor of Computer Applications**.

This project has been evaluated and approved as per the prescribed academic standards of the university."""

pdf.set_font('Times', '', 12)
pdf.multi_cell(0, 8, txt=cert_text, align='J', markdown=True)
pdf.ln(20)

pdf.set_font('Times', 'B', 12)
pdf.cell(0, 8, '**Project Guide**', align='L', markdown=True, new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Times', '', 12)
pdf.cell(0, 8, '(Signature)', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Name: Mr. Nirbhay (A.P.)', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Designation: Assistant Professor', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Department: Computer Applications', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

pdf.cell(0, 8, 'Head of Department (HOD)', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, '(Signature)', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Name: Mr. Navneet Gupta', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Department: Computer Applications', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Date:', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Place: Palampur', align='L', new_x="LMARGIN", new_y="NEXT")

# ================= PAGE 3: ACKNOWLEDGEMENT =================
pdf.add_page()
pdf.set_font('Times', 'B', 16)
pdf.cell(0, 10, 'ACKNOWLEDGEMENT', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

ack_text = """I would like to express my sincere gratitude to all those who have guided and supported me in the successful completion of my project.

First and foremost, I am highly thankful to **our respected Head of the Department**, Department of Computer Applications, for providing the necessary facilities and a conducive environment for completing this project.

I would like to express my deep sense of gratitude to my **Internal Guide, Mr. Nirbhay (A.P.)** , for their valuable guidance, constant encouragement, and support throughout the project work. Their insightful suggestions and timely feedback helped me in completing this project successfully.

I am also thankful to my **External Guide, Mr. Vishal Sharma** for their expert advice, continuous supervision, and for sharing their valuable knowledge during the course of this project.

I would also like to thank all the faculty members of the Department of Computer Applications for their support and cooperation. Last but not least, I am grateful to my family and friends for their encouragement, understanding, and moral support during the completion of this project."""

pdf.set_font('Times', '', 12)
pdf.multi_cell(0, 8, txt=ack_text, align='J', markdown=True)
pdf.ln(25)

pdf.cell(0, 8, 'RAHUL', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'Roll No.: 123011019', align='L', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, 'BCA (6TH Sem)', align='L', new_x="LMARGIN", new_y="NEXT")

# ================= PAGE 4: TABLE OF CONTENTS =================
pdf.add_page()
pdf.set_font('Times', 'B', 16)
pdf.cell(0, 10, 'TABLE OF CONTENTS', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

pdf.set_font('Times', 'B', 12)
pdf.cell(20, 10, 'S.NO', border=1, align='C')
pdf.cell(110, 10, 'TOPIC', border=1, align='C')
pdf.cell(30, 10, 'PAGE NO.', border=1, align='C', new_x="LMARGIN", new_y="NEXT")

toc_items = [
    ("1", "Abstract", "1"),
    ("2", "Introduction", "2"),
    ("3", "Problem Statement", "3"),
    ("4", "Objectives & Scope", "4"),
    ("5", "Literature Review", "5"),
    ("6", "Proposed System", "6"),
    ("7", "Feasibility Study", "7-8"),
    ("8", "System Analysis", "9"),
    ("9", "System Design", "10"),
    ("10", "Data Flow & Interaction", "11"),
    ("11", "Implementation", "12"),
    ("12", "Testing Methodologies", "13"),
    ("13", "References", "14")
]

pdf.set_font('Times', '', 12)
for row in toc_items:
    pdf.cell(20, 10, row[0], border=1, align='C')
    pdf.cell(110, 10, "  " + row[1], border=1, align='L')
    pdf.cell(30, 10, row[2], border=1, align='C', new_x="LMARGIN", new_y="NEXT")

# ================= CONTENT PAGES (Proper numbering starting here) =================

sections = [
    ("ABSTRACT", """The AI Message Assistant is an advanced, generative software project developed to provide automated messaging solutions by bridging traditional messaging platforms with modern artificial intelligence.

The core objective is to build an interactive, conversational system that replaces static manual typing with a dynamic AI interface. By integrating a specialized AI software layer utilizing Llama-3 models via Groq API, the project allows users to receive real-time, highly accurate reply suggestions to complex queries regarding their daily communications.

The implementation transitions from traditional hard-coded responses to a framework centered on Generative AI. Python is utilized to build the backend logic, while API-driven AI modules manage the generative logic. This architecture ensures the system can provide nuanced, context-aware responses rather than a fixed output.

The project's development emphasizes User Engagement and Conversational Accuracy. Unlike rigid ML workflows, this model prioritizes the seamless integration of LLMs to interpret user intent. By leveraging cloud APIs and offline voice processing via Vosk, the project provides a professional-grade application that makes digital communication faster, accessible, and tailored to the individual user's needs."""),

    ("INTRODUCTION", """In the contemporary era of rapid digital communication, managing substantial volumes of incoming messages efficiently, without compromising personalization and professional tone, represents a significant operational challenge. The AI Message Assistant is a generative artificial intelligence application developed to demonstrate the efficacy of an evolutionary software-development model within a modern data-science and AI workflow.

**OVERVIEW OF THE PROJECT**\n
This software project implements a compact, highly optimized, and production-oriented pipeline encompassing generative prompt orchestration, real-time message analysis, and a conversational AI interface. The underlying system leverages the Python programming language for backend data manipulation, the Vosk speech recognition toolkit for localized voice command execution, and advanced LLM APIs to generate dynamic, human-like responses.

Development adhered to an evolutionary approach, prioritizing incremental prompt refinement, modular code architecture, and efficient API utilization. This methodology ensures the final application is interactive, highly scalable, and fundamentally user-centric. The system is engineered to drastically minimize the cognitive load users typically face when formulating repetitive professional or casual correspondence."""),

    ("PROBLEM STATEMENT", """**PROBLEM STATEMENT**\n
The primary impediment in modern digital communication is the efficient management of high-frequency message environments. Users expend excessive temporal resources reading, analyzing, and manually typing repetitive responses. Existing automated reply features are predominantly algorithmic, often resulting in robotic, generalized responses that fail to capture the nuanced context or specific intent of an ongoing conversation. 

There exists a critical necessity for an intelligent system capable of scanning, interpreting, and drafting human-like responses instantaneously, whilst maintaining strict contextual adherence and user privacy. Current cloud-based solutions are often too slow or require expensive subscriptions, creating a barrier for average users.

The AI MESSAGE ASSISTANT addresses this by applying an evolutionary, iterative development process to generative AI: progressively refining prompt orchestration, mitigating response bias, and selecting LLM configurations that provide nuanced, user-centric guidance locally and efficiently."""),

    ("OBJECTIVES & SCOPE", """**PROJECT OBJECTIVES**\n
1. **Generative AI Integration:** To architect and deploy a conversational AI model that accurately interprets incoming text data and synthesizes personalized, real-time response suggestions utilizing the Llama-3 model.
2. **Advanced Prompt Engineering:** To systematically structure and refine system instructions (prompts) to enhance the artificial intelligence's interpretive accuracy, tone matching, and alignment with the specific intent of the user.
3. **Multimodal Input Processing:** To implement the Vosk library for highly accurate, offline speech-to-text processing, thereby enabling a robust, hands-free operational mode for dictating complex commands.
4. **Latency Optimization:** To utilize the Groq API infrastructure for near-instantaneous inference, guaranteeing that the integration of artificial intelligence does not introduce latency into the user's workflow.

**SCOPE OF THE PROJECT**\n
1. **Prompt Engineering & AI Logic:** Designing and refining system instructions to ensure the AI provides accurate, context-aware responses.
2. **Conversational AI Interface:** Building an interactive terminal or web module to handle natural language queries seamlessly.
3. **System Integration:** Connecting the backend to LLM APIs and ensuring smooth data flow between user inputs and AI-generated insights.
4. **Deployment & Persistence:** Configuring the final application for local deployment while managing API keys securely."""),

    ("LITERATURE REVIEW", """Existing systems dedicated to automated messaging and response generation typically rely upon static, rule-based algorithms, commonly manifesting as standard auto-responders or elementary chatbots. These systems operate on a rigid, predefined flow: the ingestion of a specific keyword triggers a query to a static database, which subsequently retrieves and displays pre-authored text.

While computationally inexpensive and straightforward, this single-pass approach is highly inflexible. It categorically fails to provide the personalized, conversational depth that modern users require. These legacy systems lack the intrinsic capability to process complex linguistic context, infer underlying emotional tone, or provide logical reasoning behind the suggested replies.

To transcend these limitations, this project adopts an evolutionary development workflow entirely centered on Generative Artificial Intelligence. Instead of a single-pass, rule-based setup, a dynamic prototype is constructed utilizing Large Language Models (LLMs) to genuinely comprehend the semantic meaning of the incoming message. This iterative cycle allows for the continuous enhancement of the "AI Software" component, ensuring the assistant remains contextually accurate and highly adaptable."""),

    ("PROPOSED SYSTEM", """The proposed system constitutes an iterative, AI-driven communication platform engineered to transition from traditional, hard-coded response paradigms to a dynamic, generative inference engine. It employs advanced natural language processing via the Groq API infrastructure and the Llama-3 model to deliver highly context-aware message suggestions.

**CORE FEATURES OF THE PROPOSED SYSTEM:**
1. **Contextual Message Scanning:** The system features automated reading and deep-semantic understanding of incoming messages to accurately capture the core intent and subtext.
2. **Prompt Engineering & Context Design:** The architecture relies on meticulously crafted system instructions that dictate the AI's operational tone, enforce safety guardrails, and maximize predictive accuracy.
3. **Ultra-Fast Inference Engine:** The integration of Llama-3 via the Groq Cloud API ensures near-instantaneous text generation, processing hundreds of tokens per second.
4. **Offline Voice Command Integration:** The incorporation of the Vosk library permits users to vocalize their messages and commands, which are subsequently processed into text entirely on local hardware, ensuring speed and privacy."""),

    ("FEASIBILITY STUDY", """**TECHNICAL FEASIBILITY**\n
The technical feasibility assessment evaluates the hardware and software resources required to develop, deploy, and operate the AI Message Assistant successfully. The system is designed to be highly accessible, shifting heavy computational tasks to the cloud.

**Hardware Requirements:**
1. **System / Processor:** A standard Intel Core i3 (8th Gen or above) or AMD Ryzen 3 processor is more than sufficient for seamless operation.
2. **Random Access Memory (RAM):** A minimum of 4 GB RAM is required, though 8 GB is highly recommended.
3. **Storage:** At least 2 GB of free disk space on a Solid State Drive (SSD) or Hard Disk Drive (HDD).
4. **Input/Output Peripherals:**
   - **Keyboard & Mouse:** A standard QWERTY keyboard and an optical mouse are required for manual text input and navigation.
   - **Microphone:** A functional internal or external microphone is strictly mandatory for the Vosk offline speech-to-text module.
   - **Display:** A standard monitor with a minimum resolution of 1366x768 pixels.

**Software Requirements:**
1. **Operating System:** Windows 10/11, macOS, or any standard Linux distribution.
2. **Programming Environment:** Python 3.10 or higher.
3. **Dependencies:** PyAudio (for microphone streams), Vosk, Requests, python-dotenv, and the Groq Client.

**ECONOMIC FEASIBILITY**\n
Within the scope of an academic project, the fiscal requirements are virtually non-existent. The core development relies entirely on open-source libraries. Furthermore, the Groq Cloud API currently provides a generous free tier for developers, eliminating the need for premium subscriptions.

**OPERATIONAL FEASIBILITY**\n
The operational deployment of the AI Message Assistant is highly practical and user-friendly. Users can seamlessly switch between typing queries and dictating messages hands-free via the microphone. The application initializes quickly without the need to load massive local AI models into RAM."""),

    ("SYSTEM ANALYSIS", """**SYSTEM OVERVIEW AND LOGICAL ARCHITECTURE**\n
The architectural framework of the AI Message Assistant is systematically partitioned into three distinct, interoperable layers. This modular separation ensures high maintainability, precise error tracking, and systemic scalability.

**LAYER 1: INPUT AND SENSORY ENGINE (THE LISTENER)**
1. **Service:** Vosk Offline Speech Recognition and Standard Text Input.
2. **Operational Task:** This layer is responsible for capturing the user's voice via a microphone stream and converting the audio data into highly accurate text strings locally. 

**LAYER 2: AI GATEWAY AND PROMPT ORCHESTRATION (THE BRAIN)**
1. **Logic:** Python-based prompt engineering module.
2. **Operational Task:** This intermediate layer acts as the logical bridge. It merges the parsed input text with predefined system instructions and transmits this optimized prompt payload to the cloud API.

**LAYER 3: SYNTHESIZER AND OUTPUT LAYER (THE VOICE)**
1. **Model:** Llama-3 accessed via Groq API.
2. **Operational Task:** This final layer processes the structured prompt at ultra-high speeds and returns a natural-language suggestion directly to the user interface."""),

    ("SYSTEM DESIGN", """**USER INTERFACE DESIGN**\n
The system's user interface is engineered to be highly interactive, intuitive, and computationally lightweight. Operating primarily through a responsive command-line interface or a graphical framework, it prioritizes user experience and minimal cognitive friction.

**1. Layout Management:**
   - A structured layout where the user provides input on one end, and the generated suggestions populate dynamically on the screen.
   - Real-time visual feedback indicating when the microphone is active (listening mode) and when the AI is processing the prompt.

**2. Database & Data Structures:**
   - While a traditional RDBMS is not heavily required for the core API pipeline, temporary session states are managed using JSON data structures.
   - The system securely holds the API key in environment variables to prevent accidental hardcoding in the source file.

**3. Error Handling Design:**
   - The design incorporates robust `try-except` blocks to handle scenarios like microphone failures, internet disconnections, or API rate-limiting gracefully."""),

    ("DATA FLOW & INTERACTION", """**INTERACTION FLOW AND DATA PIPELINE**\n
The interaction flow of the system is designed to minimize user friction while maximizing data processing efficiency.

1. **Input Selection:** The user selects between standard keyboard input or the microphone for a hands-free dictation experience.
2. **Transcription Phase:** If voice input is activated, the Vosk module instantaneously converts the audio stream to text offline. This local processing ensures that ambient background noise is filtered without consuming internet bandwidth.
3. **Contextual Processing:** The transcribed text is securely routed to the API handler. The underlying Python logic appends hidden systemic rules to the user's message, constraining the AI to act as a focused professional assistant rather than a generic chatbot.
4. **Output Generation:** The AI evaluates the query and generates distinct, intelligent reply options. The JSON payload is parsed, and the pure text string is displayed, empowering the user to select the optimal response."""),

    ("IMPLEMENTATION", """**ENVIRONMENT SETUP AND INTEGRATION**\n
1. **Security Configuration:** The project deployment commences with securely storing the Groq API authorization key within a hidden `.env` file, adhering to standard cybersecurity practices to prevent unauthorized access.
2. **Vosk Initialization:** The Vosk speech recognition model is initialized locally by loading a designated, lightweight acoustic language model directly into the Python execution script.

**THE VOICE LAYER IMPLEMENTATION (VOSK)**\n
Utilizing the `pyaudio` library, the system establishes a continuous microphone stream. The Vosk engine continuously analyzes the incoming audio frames in real-time. Upon the detection of a completed sentence, the engine outputs a structured JSON string containing the transcribed text.

**THE INTELLIGENCE LAYER IMPLEMENTATION (GROQ & LLAMA-3)**\n
The successfully transcribed text is programmatically passed to the Groq API endpoint. The project leverages the Llama-3 model due to its exceptional logical reasoning capabilities. Groq's proprietary LPU (Language Processing Unit) hardware architecture executes the model inference, consistently providing processing speeds exceeding 800 tokens per second."""),

    ("TESTING METHODOLOGIES", """**1. BLACK BOX TESTING**\n
Black box testing focuses entirely on the software's external attributes, functionality, and overall user behavior without inspecting the internal code structure. For the AI Message Assistant, this phase involved vocalizing inputs into the microphone, simulating various levels of ambient background noise, and verifying whether the software accurately transcribed the text and generated a logically sound, highly relevant smart reply.

**2. WHITE BOX TESTING**\n
White box testing involves evaluating the system from the developer's perspective, scrutinizing internal logic and data structures. In this project, this methodology required verifying the structural integrity of the JSON responses generated by Vosk, validating the audio sampling rates (strictly maintaining 16000 Hz), and meticulously inspecting the API payload structure dispatched to Groq.

**3. GRAY BOX TESTING**\n
Gray Box Testing represents a hybrid approach combining both Black Box and White Box techniques. This methodology was heavily utilized to optimize the prompt engineering parameters. The objective was to ensure the Llama-3 model did not merely return a valid string, but generated a string that strictly adhered to the Python context rules programmed by the developer."""),

    ("REFERENCES", """**1. Python Software Foundation**
   - Source: Official Python 3 Documentation (https://docs.python.org/3/)
   - Application: Utilized as the primary reference for standard library syntax, PyAudio implementation, and core programming structures.

**2. Groq Cloud API Documentation**
   - Source: Groq Developer Portal (https://console.groq.com/docs/quickstart)
   - Application: Referenced for understanding Language Processing Unit (LPU) inference mechanics, API authentication protocols, and JSON payload structuring.

**3. Vosk Offline Speech Recognition Toolkit**
   - Source: Alpha Cephei Documentation (https://alphacephei.com/vosk/)
   - Application: Essential guidelines for the integration and implementation of offline voice-to-text capabilities and acoustic model management.

**4. Meta Llama-3 Architecture**
   - Source: Llama Model Card (https://llama.meta.com/llama3/)
   - Application: Analyzed to understand the neural architecture, reasoning capabilities, and token limitation parameters of the underlying Large Language Model utilized in this project.""")
]

pdf.set_font('Times', '', 12)

# Write Content Pages
for title, content in sections:
    pdf.add_page()
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, 10, title, align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font('Times', '', 12)
    # Justified alignment, supports Markdown for bolding
    pdf.multi_cell(0, 8, txt=content, align='J', markdown=True)

filename = "Rahul_123011019_Final_Detailed.pdf"
pdf.output(filename)
print(f"Bhai, tumhari final PDF ready hai! Pages: {pdf.page_no()}")