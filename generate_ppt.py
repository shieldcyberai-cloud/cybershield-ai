from fpdf import FPDF

class ProjectSynopsis(FPDF):
    def __init__(self):
        super().__init__()
        # Proper 1 inch margin
        self.set_margins(25.4, 25.4, 25.4)
        
    def header(self):
        pass
        
    def footer(self):
        # Footer sirf 5th page (Abstract) se dikhega
        if self.page_no() >= 5:
            self.set_y(-15)
            # Simple font: No bold, No italic
            self.set_font('Arial', '', 10)
            
            # Center alignment for Department Name
            self.cell(0, 10, 'DEPARTMENT OF COMPUTER APPLICATIONS', 0, 0, 'C')
            
            # Page number on the right (Abstract is Page 1)
            actual_page_num = self.page_no() - 4
            self.set_x(-20)
            self.cell(0, 10, str(actual_page_num), 0, 0, 'R')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 14)
        # Heading Center (C)
        self.cell(0, 10, label, 0, 1, 'C')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        # Cleaning unicode dashes/quotes to avoid encoding errors
        body = body.replace('—', '-').replace('–', '-').replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        body = body.encode('latin-1', 'ignore').decode('latin-1')
        
        # Proper line spacing
        self.multi_cell(0, 8, body)
        self.ln()

# Create PDF
pdf = ProjectSynopsis()
pdf.set_auto_page_break(auto=True, margin=20)

# ================= PAGE 1: COVER PAGE =================
pdf.add_page()
pdf.set_font('Arial', 'B', 24)
pdf.cell(0, 20, 'SRI SAI UNIVERSITY', 0, 1, 'C') 
pdf.set_font('Arial', '', 14)
pdf.cell(0, 10, 'Transforming Dreams into Reality', 0, 1, 'C') 
pdf.ln(20)

pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'SYNOPSIS', 0, 1, 'C')
pdf.cell(0, 10, 'ON', 0, 1, 'C')
pdf.set_font('Arial', 'B', 18)
pdf.multi_cell(0, 10, 'PROJECT "AI MESSAGE ASSISTANT"', 0, 'C')
pdf.ln(15)

pdf.set_font('Arial', '', 14)
pdf.cell(0, 8, 'In Partial Fulfilment', 0, 1, 'C')
pdf.cell(0, 8, 'of', 0, 1, 'C')
pdf.cell(0, 8, 'Bachelor of Computer Applications (BCA)', 0, 1, 'C')
pdf.ln(30)

pdf.set_font('Arial', 'B', 12)
pdf.cell(100, 8, 'Submitted to:', 0, 0, 'L')
pdf.cell(0, 8, 'Submitted By:', 0, 1, 'R')
pdf.set_font('Arial', '', 12)
pdf.cell(100, 8, 'Mr. Nirbhay (A.P.)', 0, 0, 'L') 
pdf.cell(0, 8, 'Mr. Rahul', 0, 1, 'R')
pdf.cell(100, 8, '', 0, 0, 'L')
pdf.cell(0, 8, 'Roll No: 123011019', 0, 1, 'R')
pdf.cell(100, 8, '', 0, 0, 'L')
pdf.cell(0, 8, 'BCA (6TH Sem)', 0, 1, 'R')
pdf.ln(30)

pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 8, 'SRI SAI UNIVERSITY, PALAMPUR (H.P.)', 0, 1, 'C') 
pdf.cell(0, 8, 'DEPARTMENT OF COMPUTER APPLICATIONS', 0, 1, 'C') 
pdf.cell(0, 8, 'SESSION (2023-2026)', 0, 1, 'C') 

# ================= PAGE 2: CERTIFICATE =================
pdf.add_page()
pdf.chapter_title('CERTIFICATE')
cert_text = """This is to certify that the project entitled "AI MESSAGE ASSISTANT" is a bonafide work carried out by Mr. RAHUL, Roll No. 123011019, a student of Bachelor of Computer Applications (BCA), 6th Semester, during the academic session 2025-2026.

The work has been completed under the guidance of Mr. NIRBHAY (A.P.) (Internal Guide) in partial fulfillment of the requirements for the award of the degree of Bachelor of Computer Applications.

This project has been evaluated and approved as per the prescribed academic standards of the university."""
pdf.chapter_body(cert_text)
pdf.ln(30)

pdf.set_font('Arial', 'B', 12)
pdf.cell(100, 8, 'Project Guide', 0, 0, 'L')
pdf.cell(0, 8, 'Head of Department (HOD)', 0, 1, 'R')
pdf.set_font('Arial', '', 12)
pdf.cell(100, 8, '(Signature)', 0, 0, 'L')
pdf.cell(0, 8, '(Signature)', 0, 1, 'R')
pdf.cell(100, 8, 'Name: Mr. Nirbhay (A.P.)', 0, 0, 'L')
pdf.cell(0, 8, 'Name: Mr. Navneet Gupta', 0, 1, 'R')
pdf.cell(100, 8, 'Dept: Computer Applications', 0, 0, 'L')
pdf.cell(0, 8, 'Dept: Computer Applications', 0, 1, 'R')
pdf.ln(20)
pdf.cell(0, 8, 'Date: ____________', 0, 1, 'L')
pdf.cell(0, 8, 'Place: Palampur', 0, 1, 'L')

# ================= PAGE 3: ACKNOWLEDGEMENT =================
pdf.add_page()
pdf.chapter_title('ACKNOWLEDGEMENT')
ack_text = """I would like to express my sincere gratitude to all those who have guided and supported me in the successful completion of my project.

First and foremost, I am highly thankful to our respected Head of the Department, Mr. Navneet Gupta, Department of Computer Applications, for providing the necessary facilities and a conducive environment for completing this project.

I would like to express my deep sense of gratitude to my Internal Guide, Mr. Nirbhay (A.P.) for their valuable guidance, constant encouragement, and support throughout the project work. Their insightful suggestions and timely feedback helped me in completing this project successfully.

I would also like to thank all the faculty members of the Department of Computer Applications for their support and cooperation.

Last but not least, I am grateful to my family and friends for their encouragement, understanding, and moral support during the completion of this project."""
pdf.chapter_body(ack_text)
pdf.ln(20)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'RAHUL', 0, 1, 'R')
pdf.set_font('Arial', '', 12)
pdf.cell(0, 8, 'Roll No: 123011019', 0, 1, 'R')
pdf.cell(0, 8, 'BCA (6TH Sem)', 0, 1, 'R')

# ================= PAGE 4: TABLE OF CONTENTS =================
pdf.add_page()
pdf.chapter_title('TABLE OF CONTENTS')
pdf.set_font('Arial', 'B', 12)
pdf.cell(20, 10, 'S.NO', border=1, align='C')
pdf.cell(100, 10, 'TOPIC', border=1, align='L')
pdf.cell(30, 10, 'PAGE NO.', border=1, align='C')
pdf.ln()

# 14 Content Pages Mapping
toc_items = [
    ("1", "Abstract", "1"),
    ("2", "Introduction", "2"),
    ("3", "Problem Statement & Objectives", "3"),
    ("4", "Literature Review", "4"),
    ("5", "Proposed System", "5"),
    ("6", "Technical Feasibility", "6"),
    ("7", "Economic & Op. Feasibility", "7"),
    ("8", "System Analysis", "8"),
    ("9", "System Design", "9"),
    ("10", "UI Flow & Interaction", "10"),
    ("11", "Implementation", "11"),
    ("12", "Model Description", "12"),
    ("13", "Testing", "13"),
    ("14", "References", "14")
]

pdf.set_font('Arial', '', 12)
for row in toc_items:
    pdf.cell(20, 10, row[0], border=1, align='C')
    pdf.cell(100, 10, "  " + row[1], border=1, align='L')
    pdf.cell(30, 10, row[2], border=1, align='C')
    pdf.ln()

# ================= CONTENT PAGES (14 Exact Pages) =================
sections = [
    ("ABSTRACT", """The AI Message Assistant is an advanced, generative software project developed to provide personalized and automated messaging solutions. By bridging traditional messaging platforms with modern artificial intelligence, it creates a seamless communication experience.

The core objective is to build an interactive, conversational system that replaces static manual typing with a dynamic AI interface. By integrating a specialized AI software layer using Llama-3 models via Groq API, the project allows users to receive real-time, highly accurate reply suggestions to complex messages. 

The implementation transitions from traditional hard-coded responses to a framework centered on Generative AI. Python is utilized to build the backend logic and API handling, enabling smooth data flow. The architecture ensures the system can provide nuanced, context-aware responses rather than fixed, robotic outputs.

The project's development emphasizes User Engagement, Speed, and Automation. Unlike rigid ML workflows, this model prioritizes the seamless integration of LLMs to interpret user intent efficiently. By leveraging cloud APIs and offline voice processing via Vosk, the project provides a professional-grade application that makes digital communication faster, accessible, and tailored to the individual user's needs."""), 

    ("INTRODUCTION", """In the era of rapid digital communication, managing high volumes of messages efficiently without losing the personal touch is a significant challenge. The AI MESSAGE ASSISTANT is a generative AI-based application developed to demonstrate the effectiveness of an evolutionary software-development model within a modern AI workflow.

OVERVIEW OF THE PROJECT:
This project implements a compact, production-oriented pipeline: generative prompt orchestration, real-time message scanning, and a conversational AI interface. The system leverages Python for backend data handling, Vosk for voice commands, and LLM APIs to provide dynamic responses. 

Development followed an evolutionary approach - incremental prompt refinement, modular code, and efficient API usage - ensuring the application is interactive, scalable, and user-centric. The system is designed to drastically reduce the time users spend typing repetitive professional and casual messages."""),

    ("PROBLEM STATEMENT & OBJECTIVES", """PROBLEM STATEMENT:
The primary challenge in digital communication is managing high volumes of messages efficiently. Users spend excessive time reading and typing repetitive responses. Existing auto-reply features are often too robotic or fail to understand the nuanced context of a conversation. The AI Message Assistant addresses this by applying an iterative development process to generative AI: orchestrating prompts to understand context and selecting LLM configurations that provide nuanced, user-centric replies instantly.

OBJECTIVES:
1. Generative AI Modeling: To develop and deploy a conversational AI model that interprets incoming messages and provides personalized, real-time response suggestions using Llama-3.
2. Data Processing & Prompt Engineering: To manage textual data and refine system prompts to improve the AI's interpretive accuracy, tone matching, and alignment with user intent.
3. Multimodal Integration: To implement the Vosk library for offline speech-to-text processing, allowing users to dictate commands seamlessly."""),

    ("LITERATURE REVIEW", """Existing systems for automated messaging typically rely on static, rule-based algorithms (like standard auto-responders or basic chatbots). They follow a rigid flow: input keyword -> query database -> retrieve pre-written text -> display.

While straightforward, this one-pass approach is rigid and fails to provide the personalized, conversational depth that modern users expect. These systems often lack the ability to handle complex context or provide reasoning behind the suggested replies.

To overcome these limits, this project adopts an evolutionary development workflow centered on Generative AI. Instead of a single-pass, rule-based setup, we build a dynamic prototype that uses Llama-3 to understand the actual meaning of the message. This cycle allows for the continuous improvement of the "AI Software" component, ensuring the assistant remains contextually accurate and highly engaging for professional use cases."""),

    ("PROPOSED SYSTEM", """The proposed system is an iterative AI-driven communication platform that transitions from traditional hard-coded replies to a dynamic, generative inference engine. It utilizes natural language processing via Groq's API and Llama-3 to provide context-aware message suggestions.

FEATURES OF THE PROPOSED SYSTEM:
* Contextual Message Scanning: Automated reading and understanding of incoming messages to capture the core intent.
* Prompt Engineering & Context Design: Crafting specialized system instructions to guide the AI's tone, safety guardrails, and accuracy.
* Ultra-Fast Inference Engine: Integration of Llama-3 via Groq Cloud API for near-instantaneous text generation.
* Offline Voice Commands: Integration of the Vosk library to allow users to speak their messages, which are processed into text locally.
* Response Validation & Refinement: Iterative testing of AI outputs to ensure conversational coherence and mitigate robotic advice."""),

    ("TECHNICAL FEASIBILITY", """TECHNICAL FEASIBILITY:
The AI Message Assistant is fully implementable using modern Python frameworks and Generative AI APIs. By shifting from local model training to API-driven inference via Groq, the technical complexity moves from hardware-heavy computation to efficient request handling.

Hardware Requirements:
* Development Hardware (Minimum): Dual-core CPU, 4 GB RAM, and a working microphone for Vosk testing. A stable internet connection is mandatory for Groq API communication.
* Development Hardware (Recommended): Quad-core CPU, 8 GB RAM, and an SSD for smooth development and faster local execution of the Vosk audio model.

Software Stack:
* Implementation Stack: Python 3.x, Groq API (Llama-3), Vosk Library, and environment management (dotenv).
* The application runs primarily on terminal or web frameworks like Streamlit, making it lightweight."""),

    ("ECONOMIC & OPERATIONAL FEASIBILITY", """ECONOMIC FEASIBILITY:
For a university project, the initial costs are virtually zero. The primary libraries (Python, Vosk, PyAudio) are entirely open-source and free to use. Furthermore, Groq Cloud currently provides generous free tiers for developers. This is more than sufficient for testing, demonstration, and generating ultra-fast LLM responses without paying for expensive GPU cloud instances.

OPERATIONAL FEASIBILITY:
The operation for demonstrating the AI Message Assistant is straightforward and designed for immediate accessibility. To launch the system, a developer simply needs to set up a Python virtual environment and execute the main python script.

Unlike heavy local AI models, there is no need to load a massive model file into RAM (except the lightweight Vosk language model for speech); instead, the app establishes a secure connection to the Groq API upon startup. The interface is intuitive, requiring minimal user training."""),

    ("SYSTEM ANALYSIS", """SYSTEM OVERVIEW:
The architecture of the AI Message Assistant is systematically divided into three distinct layers to ensure modularity and scalability: the Input/Voice Engine, the AI API Gateway, and the Synthesizer.

Layer 1: Input & Voice Engine (The "Listener")
Service: Vosk Offline Speech Recognition / Text Input.
Task: Captures user voice via microphone and converts it to highly accurate text locally.

Layer 2: AI Gateway & Prompt Management (The "Brain")
Database/Logic: Python prompt orchestration.
Task: Merges the parsed text with system instructions (defining tone, context, and rules) and sends the optimized prompt to the Groq Cloud API.

Layer 3: Synthesizer Layer (The "Voice")
Model: Llama-3 via Groq API.
Task: Processes the structured prompt at ultra-high speed and returns a natural-language response."""),

    ("SYSTEM DESIGN", """USER INTERFACE DESIGN:
The system's user interface is kept highly interactive yet lightweight. For PC deployment, it operates via a responsive command-line interface or a Streamlit web layout.

1. Layout Management:
* Dual-pane layout where the user provides input on one end, and the generated suggestions populate dynamically.
* Real-time visual feedback indicating when the microphone is active (listening mode) and when the AI is processing the prompt.

2. Data Flow Structure:
* Data flows sequentially from the PyAudio stream to the Vosk JSON parser.
* The extracted string is then encapsulated within a JSON payload and dispatched via HTTPS to the Groq Inference Engine.
* The response is parsed back to extract the AI's content block, which is then rendered on the screen."""),

    ("UI FLOW & INTERACTION", """INTERACTION FLOW:
The interaction flow of the system is designed to minimize user friction.

1. Input Selection: The user chooses between typing a message directly or utilizing the microphone for a hands-free experience.
2. Transcription: If voice is selected, Vosk instantly converts the audio stream to text without needing the internet. It actively filters background noise.
3. Processing Context: The text is sent via Groq API to Llama-3. Behind the scenes, the system appends hidden rules to the user's message, instructing the AI to act as a professional assistant.
4. Output Generation: The AI evaluates the query and generates 2-3 smart reply options, allowing the user to select the best fit.

This seamless loop ensures that communication remains fluid, fast, and highly contextual."""),

    ("IMPLEMENTATION", """SETUP & INTEGRATION:
1. Environment Setup: The project begins by securely storing the Groq API key in a hidden `.env` file to prevent unauthorized access.
2. Vosk Initialization: The Vosk model is initialized locally by loading a lightweight language model into the Python script.

THE VOICE LAYER (VOSK):
Using the pyaudio library, the system opens a microphone stream. Vosk continuously analyzes the audio frames. Once a sentence is completed, it outputs a JSON string containing the recognized text.

THE INTELLIGENCE LAYER (GROQ & LLAMA-3):
The transcribed text is passed to the Groq API. The project uses Llama-3 because of its exceptional reasoning capabilities. Groq's LPU (Language Processing Unit) architecture executes the model, providing inference speeds of over 800 tokens per second, making the response feel instantaneous."""),

    ("MODEL DESCRIPTION", """THE GENERATIVE PIPELINE:
The project uses a hybrid pipeline implemented via the Groq Llama-3 model and a local speech recognition engine. The model interprets contextual prompts derived from user inputs.

Unlike a standard machine learning classification model, this system uses an advanced Prompting Strategy. The user's input is injected into the LLM context for consistent, deterministic-style interpretation.

LIMITATIONS & FUTURE SCOPE:
As a generative model, it relies on internet connectivity for the Llama-3 component. While the Voice recognition (Vosk) works entirely offline, the core "brain" requires Groq's servers to function. 

A key future scope includes integrating smaller, fully offline LLMs (like Llama-3 8B quantized) directly onto the local machine if hardware permits, thereby making the entire AI Assistant 100% offline and hyper-secure."""),

    ("TESTING", """1. BLACK BOX TESTING:
Black box testing focuses on software's external attributes and behavior. For the AI Assistant, this involved speaking into the microphone, simulating background noise, and verifying if the correct text and a logical smart reply were generated on the screen without looking at the code.

2. WHITE BOX TESTING:
This testing works by looking at testing from the developer's point of view. In this project, it involved verifying the JSON responses from Vosk, checking the audio frame rates (16000 Hz), and inspecting the API payload structure being sent to Groq for authentication errors.

3. GRAY BOX TESTING:
Gray Box Testing is a combination of both techniques. This was heavily used to optimize the prompt engineering, ensuring the Llama-3 model didn't just return a valid string, but a string that strictly adhered to the Python context rules (e.g., returning exactly 2 options)."""),

    ("REFERENCES", """1. Python Official Documentation
* Official Docs: https://docs.python.org/3/
* Purpose: Standard library references and syntax logic.

2. Groq API Documentation
* Official Docs: https://console.groq.com/docs/quickstart
* API Reference: https://console.groq.com/docs/api-reference
* Purpose: Understanding LPU inference and API payload structuring.

3. Vosk Speech Recognition Toolkit
* Official Docs: https://alphacephei.com/vosk/
* Models & Integration: https://alphacephei.com/vosk/models
* Purpose: Implementation of offline voice-to-text capabilities.

4. Llama-3 Model Card (Meta AI)
* Documentation: https://llama.meta.com/llama3/
* Purpose: Understanding the architecture and reasoning capabilities of the underlying LLM.""")
]

# Write EXACTLY 14 pages (Total 18 pages)
for title, content in sections:
    pdf.add_page()
    pdf.chapter_title(title)
    pdf.chapter_body(content)

# Final Output
filename = "Rahul_123011019_Exact_18_Pages.pdf"
pdf.output(filename)
print(f"Bhai, tumhari {pdf.page_no()} pages ki PDF '{filename}' ready hai!")