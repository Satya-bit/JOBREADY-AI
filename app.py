# I have used Streamlit to build prototype of frontend as I was having time constraints. 
# But we can later use REACT to make the frontend.

import streamlit as st
import os
import time
import traceback 
import re
# Importing the existing modules
from core.resume_parser import parse_resume
from agent.round_manager import AVAILABLE_ROUNDS
from agent.interview_agent import InterviewAgent
from core.audio_io import speak_text, transcribe_audio,record_audio 
from core.feedback_generator import generate_feedback_and_scores
from utils.config import TEMP_AUDIO_FILENAME 
from utils import config # checks if keys are loaded properly

# --- Streamlit App Configuration ---
st.set_page_config(page_title="PREPWISE AI", layout="wide")

# Inject robust CSS for background, fonts and controls (uses strong selectors and !important)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
:root { 
  /* Softer blue gradient (top → bottom) */
  --bg: #0f2b45;      /* lighter navy-blue top tone */
  --bg2: #163d5c;     /* deeper desaturated blue bottom */
  --card: #1c4666;    /* slightly lighter than main background for cards */
  --accent: #3b82f6;  /* keep the bright blue accent for buttons/links */
  --muted: #a8bed8;   /* softened text color */
}
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main, .block-container, .stApp {
  background: linear-gradient(180deg, var(--bg) 0%, var(--bg2) 100%) !important;
  color: #FFFFFF !important;
  font-family: 'Roboto', sans-serif !important;
}
[data-testid="stSidebar"] { background-color: rgba(10,18,30,0.95) !important; border-right: 1px solid rgba(255,255,255,0.04) !important; }
.block-container { max-width: 1100px; padding: 2rem !important; }
.stButton>button { background-color: var(--accent) !important; color: #04203a !important; border: none !important; padding: 8px 16px !important; border-radius: 8px !important; box-shadow: 0 2px 6px rgba(59,130,246,0.12) !important; display: inline-flex !important; width: auto !important; margin-right: 4px !important; }
.stButton>button:hover { background-color: #1e6ff6 !important; }
/* Make cards slightly lighter than background to keep contrast */
[data-testid="stAppViewContainer"] .css-1d391kg, .css-1outpf7, .css-1v3fvcr { background: rgba(255,255,255,0.02) !important; border: 1px solid rgba(255,255,255,0.03) !important; }

/* Camera input: ensure the "Take Photo" control text is black and fully opaque */
[data-testid="stCameraInput"] button, [data-testid="stCameraInput"] .stButton>button, [data-testid="stCameraInput"] button span {
    color: #000000 !important;
    opacity: 1 !important;
}

/* Also target potential nested classes for camera input used by some Streamlit versions */
div[data-testid="stCameraInput"] button[role="button"], div[data-testid="stCameraInput"] [role="button"] {
    color: #000000 !important;
    opacity: 1 !important;
}

h1, h2, h3, h4, p, label, .stText, .streamlit-expanderHeader { font-family: 'Roboto', sans-serif !important; color: #FFFFFF !important; }
/* Ensure inputs have readable backgrounds */
.stTextInput>div>div>input, .stTextArea>div>div>textarea { background: rgba(255,255,255,0.02) !important; color: #fff !important; border: 1px solid rgba(255,255,255,0.04) !important; }
/* Sidebar text contrast */
[data-testid="stSidebar"] * { color: #e6f0fb !important; }
/* Adjust link color */
a, a:visited { color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)


# --- Sidebar Info ---
st.sidebar.header("About")
st.sidebar.info(
"PREPWISE AI helps you practice interviews with AI-powered voice and text conversations."
"Built using OpenAI and ElevenLabs, it offers instant feedback and scoring to sharpen your skills and boost your confidence before the real interview."
)

UPLOAD_DIR = "data/uploads" # Saves resume Files
RECORDING_DIR = "data/recordings" #Saves Audio Recordings


# Funtion for uploading files
def save_uploaded_file(uploaded_file):
    """Saves uploaded file temporarily for parsing."""
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None

# Function for cleaning up temporary files
def cleanup_temp_file(file_path):
    """Removes a specific temporary file."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        st.warning(f"Could not remove temporary file {file_path}: {e}")


# --- Initializing Session State ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'job_description' # Initial stage
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'interview_agent' not in st.session_state:
    st.session_state.interview_agent = None
if 'selected_round_key' not in st.session_state:
    st.session_state.selected_round_key = None
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'interview_history' not in st.session_state:
    st.session_state.interview_history = [] # List of {'question': q, 'answer': a}
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'temp_resume_path' not in st.session_state:
     st.session_state.temp_resume_path = None # Store path for cleanup

# --- Checking API Keys ---
keys_loaded = bool(config.OPENAI_API_KEY and config.ELEVENLABS_API_KEY)
if not keys_loaded:
    st.error("API keys for OpenAI or ElevenLabs not found! Please check your .env file.")
    st.stop() 
# --- Main App Logic ---

st.title("🎯 PREPWISE AI")
st.markdown("Enter a job description and upload your resume, choose an interview round, and practice with an AI interviewer!")


if st.session_state.stage == 'job_description':
    # Override dark theme locally for the job description input so fonts are black on white
    st.markdown("""
    <style>
    /* Target Streamlit textarea and its label - applied only while this markdown is present */
    [data-testid="stTextArea"] textarea, .stTextArea>div>div>textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 1px solid rgba(0,0,0,0.12) !important;
    }
    /* Label and helper text */
    [data-testid="stTextArea"] label, .stTextArea label, .stTextArea .stMarkdown {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.header("1. Enter Job Description")
    job_description = st.text_area("Job Description", height=200)
    if st.button("Next", key="next_job_desc_btn"): # Button to proceed
        if job_description:
            st.session_state.job_description = job_description
            st.session_state.stage = 'upload'
            st.rerun()
        else:
            st.warning("Please enter a job description.")

# --- Stage 2: Upload Resume ---
if st.session_state.stage == 'upload':
    st.header("2. Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a resume file (PDF or DOCX)", type=['pdf', 'docx'])

    if uploaded_file is not None:
        # Save and parse
        st.session_state.temp_resume_path = save_uploaded_file(uploaded_file)
        if st.session_state.temp_resume_path:
            with st.spinner("Parsing resume..."):
                st.session_state.resume_text = parse_resume(st.session_state.temp_resume_path)

            if st.session_state.resume_text:
                st.success("Resume parsed successfully!")

                try:
                    st.session_state.interview_agent = InterviewAgent(st.session_state.resume_text,st.session_state.job_description)
                    st.session_state.stage = 'select_round'
                    st.rerun() # Rerun to move to the next stage UI immediately
                except Exception as e:
                    st.error(f"Failed to initialize interview agent: {e}")
                    st.session_state.resume_text = None # Reset on failure
                    st.session_state.interview_agent = None
                    cleanup_temp_file(st.session_state.temp_resume_path) # Clean up failed attempt's file
                    st.session_state.temp_resume_path = None
            else:
                st.error("Could not extract text from the resume. Please try a different file.")
                cleanup_temp_file(st.session_state.temp_resume_path) # Clean up failed attempt's file
                st.session_state.temp_resume_path = None


# --- Stage 3: Select Round ---
if st.session_state.stage == 'select_round':
    st.header("3. Select Interview Round")
    
    # Check if agent is initialized (should be if we are in this stage)
    if not st.session_state.interview_agent:
         st.error("Interview agent not initialized. Please upload a resume first.")
         st.session_state.stage = 'upload' # Go back to upload stage
         # Clean up just in case
         cleanup_temp_file(st.session_state.temp_resume_path)
         st.session_state.temp_resume_path = None
         st.rerun()

    round_options = {key: info['name'] for key, info in AVAILABLE_ROUNDS.items()}
    st.session_state.selected_round_key = st.selectbox(
        "Choose the type of interview round:",
        options=list(round_options.keys()),
        format_func=lambda key: round_options[key] # Show names in dropdown
    )

    if st.button("Start Interview Round", key="start_interview_btn"):
        if st.session_state.selected_round_key:
            selected_round_info = AVAILABLE_ROUNDS[st.session_state.selected_round_key]
            st.session_state.current_question_index = 0
            st.session_state.interview_history = []
            st.session_state.feedback = None
            
            # Generate questions for the round
            agent = st.session_state.interview_agent
            if agent:
                with st.spinner(f"Generating questions for the {selected_round_info['name']} round..."):
                    try:
                        # Access internal method carefully (or refactor agent for this)
                        st.session_state.questions = agent._generate_questions(
                            selected_round_info['name'],
                            selected_round_info['num_questions']
                        )
                    except Exception as e:
                         st.error(f"Error generating questions: {e}")
                         st.error(traceback.format_exc()) # Prints detailed error
                         st.session_state.questions = [] # Ensure it's empty on failure


                if st.session_state.questions:
                    st.session_state.stage = 'interviewing'
                    st.success(f"Questions generated. Starting the {selected_round_info['name']} round!")
                    time.sleep(1) # Gives user a moment to read the message
                    # Speaks welcome message for the round
                    try:
                        speak_text(f"Welcome to the {selected_round_info['name']} round. I will ask you {len(st.session_state.questions)} questions. Let's begin with the first question.")
                    except Exception as e:
                        st.warning(f"Could not play welcome audio: {e}. Starting interview.")
                    st.rerun()
                else:
                    st.error("Failed to generate questions for the round. Please try selecting the round again or check the logs/API keys.")
            else:
                 st.error("Interview agent not found. Please restart the process by uploading the resume again.")
                 st.session_state.stage = 'upload'
                 cleanup_temp_file(st.session_state.temp_resume_path)
                 st.session_state.temp_resume_path = None
                 st.rerun()
        else:
            st.warning("Please select a round first.")


# --- Stage 4: Interviewing ---
if st.session_state.stage == 'interviewing':
    st.header(f"🎙️ Interview in Progress: {AVAILABLE_ROUNDS[st.session_state.selected_round_key]['name']} Round")

    # Check if questions are loaded before interviewing
    if not st.session_state.questions:
        st.error("No questions loaded for this round. Please go back and select the round again.")
        if st.button("Go Back to Round Selection"):
            st.session_state.stage = 'select_round'
            st.rerun()
        st.stop()

    

    with st.sidebar:  
            st.camera_input("Camera Input", key="camera_input", 
                        width=600 # Set the width and height to make it smaller
                    ) 
    q_index = st.session_state.current_question_index

    if q_index < len(st.session_state.questions):
        current_question = st.session_state.questions[q_index]

        st.subheader(f"Question {q_index + 1}/{len(st.session_state.questions)}")
        st.markdown(f"**Interviewer:** {current_question}")
        if f"spoken_q{q_index}" not in st.session_state:
             try:
                 speak_text(current_question)
                 st.session_state[f"spoken_q{q_index}"] = True
             except Exception as e:
                 st.warning(f"Could not play question audio: {e}")
                 st.session_state[f"spoken_q{q_index}"] = True # Mark as 'spoken' anyway to avoid retry loop

        # --- Write/Record Audio Answer ---
        st.markdown("**Your Answer ( Write Text or Record Below):**")
        # Scoped CSS to make the answer textarea black-on-white so it's readable while keeping the rest of UI dark
        st.markdown('''
            <style>
            /* Stronger selectors: native textarea, Streamlit's stTextArea textarea, and contenteditable divs */
            textarea[placeholder="Type your answer..."], .stTextArea textarea[placeholder="Type your answer..."], .stTextArea textarea, .stTextArea div[role="textbox"] {
                color: #000000 !important;
                background-color: #ffffff !important;
                border: 1px solid rgba(0,0,0,0.12) !important;
                caret-color: #000000 !important;
                -webkit-text-fill-color: #000000 !important;
            }
            /* Placeholder color */
            textarea::placeholder, .stTextArea textarea::placeholder { color: rgba(0,0,0,0.45) !important; }
            /* Make the label and helper text for textareas in this block black for readability */
            .stTextArea label, .stTextArea .stMarkdown {
                color: #000000 !important;
            }
            </style>
        ''', unsafe_allow_html=True)
        
        user_answer = st.text_area("Enter your answer here:", key=f"answer_q{q_index}", height=150, placeholder="Type your answer...")

        # Place the Submit and Record buttons side-by-side (use tight columns so buttons stay close)
        spacer, btn_col1, btn_col2 = st.columns([6,1,1])

        with btn_col1:
            if st.button("Submit Answer", key=f"submit_q{q_index}"):
                if user_answer and user_answer.strip():
                    # Store the answer
                    st.session_state.interview_history.append({
                        "question": current_question,
                        "answer": user_answer.strip()
                    })

                    # Move to the next question
                    st.session_state.current_question_index += 1

                    # If there are more questions, speak the next one (or transition)
                    if st.session_state.current_question_index < len(st.session_state.questions):
                        next_q_index = st.session_state.current_question_index
                        next_question = st.session_state.questions[next_q_index]
                        try:
                            # Maybe just say "Next question." or similar to keep it shorter
                            speak_text("Okay, thank you. Next question.")
                            # Let Streamlit rerun handle displaying the next question text
                        except Exception as e:
                            st.warning(f"Audio notification error: {e}")

                    st.rerun() # Rerun to display the next question or move to feedback stage

                else:
                    st.warning("Please enter your answer before submitting.")

        with btn_col2:
            if st.button("Record Answer", key=f"record_q{q_index}"):
                with st.spinner("Recording in progress..."):
                    try:
                        # Call the record_audio function from audio_io.py
                        filename = record_audio()
                        if filename:
                            # Transcribe the recorded audio
                            user_answer = transcribe_audio(filename)
                            if user_answer:
                                # Store the answer
                                st.session_state.interview_history.append({
                                    "question": current_question,
                                    "answer": user_answer.strip()
                                })
                                st.success("Answer recorded and transcribed successfully!")
                            else:
                                st.session_state.warning_message = "Please record the answer clearly and again."
                                st.warning(st.session_state.warning_message)
                                time.sleep(5)
                                st.session_state.current_question_index=q_index
                                st.rerun()
                    except Exception as e:
                        st.error(f"Recording/transcription failed: {e}")

            
        
                    # Move to the next question
                st.session_state.current_question_index += 1

                    # If there are more questions, speak the next one (or transition)
                if st.session_state.current_question_index < len(st.session_state.questions):
                        next_q_index = st.session_state.current_question_index
                        next_question = st.session_state.questions[next_q_index]
                        try:
                            # Maybe just say "Next question." or similar to keep it shorter
                            speak_text("Okay, thank you. Next question.")
                            # Let Streamlit rerun handle displaying the next question text
                        except Exception as e:
                            st.warning(f"Audio notification error: {e}")

                st.rerun() # Rerun to display the next question or move to feedback stage


    else:
        # All questions answered, move to feedback stage
        st.success("All questions for this round are complete!")
        st.session_state.stage = 'feedback'
        try:
            speak_text("Thank you. That concludes the questions for this round. I will now prepare your feedback.")
        except Exception as e:
             st.warning(f"Audio notification error: {e}")
        st.rerun()


# --- Stage 5: Feedback ---
if st.session_state.stage == 'feedback':
    st.header("✅ Interview Complete - Feedback")

    agent = st.session_state.interview_agent
    round_name = AVAILABLE_ROUNDS[st.session_state.selected_round_key]['name']

    # Generate feedback only if it hasn't been generated yet for this round
    if not st.session_state.feedback and agent and st.session_state.interview_history:
        with st.spinner("Generating feedback... This may take a moment."):
            try:
                # Generate feedback using the agent's method (or directly call the function)
                # We need resume_text, job description, round_name, and history from session_state
                # Inside the 'feedback' stage in app.py
                st.session_state.feedback = generate_feedback_and_scores( # Call the imported function directly
                    resume_text=st.session_state.resume_text,
                    job_description=st.session_state.job_description, # Pass job description if needed
                    round_name=round_name,
                    qa_pairs=st.session_state.interview_history
                )
            except Exception as e:
                st.error(f"Failed to generate feedback: {e}")
                st.error(traceback.format_exc()) # Print detailed error


    # Display Feedback if available
    if st.session_state.feedback:
        feedback_data = st.session_state.feedback

        st.subheader("Overall Feedback")
        st.markdown(feedback_data.get("overall_feedback", "N/A"))

        st.subheader("Suggestions for Improvement")
        # Post-process suggestions string so metric labels appear on new lines for readability
        suggestions = feedback_data.get("suggestions", "N/A")
        if isinstance(suggestions, str):
            # Insert paragraph breaks before common metric labels
            suggestions = re.sub(r"\s*(Relevance:)", r"\n\n\1", suggestions)
            suggestions = re.sub(r"\s*(Clarity:)", r"\n\n\1", suggestions)
            suggestions = re.sub(r"\s*(Detail/Examples:)", r"\n\n\1", suggestions)
            suggestions = re.sub(r"\s*(Resume Alignment:)", r"\n\n\1", suggestions)
            # Ensure Qn and Overall Score appear on the same line: convert '\n\nQ1\n\nOverall Score:' -> 'Q1 Overall Score:'
            # First normalize possible 'Qn' followed later by 'Overall Score:' to ensure spacing
            suggestions = re.sub(r"Q(\d+)\s*\n\s*Overall Score:", r"Q\1 Overall Score:", suggestions)
            # Also handle cases where 'Qn' and 'Overall Score' are separated by our earlier inserts
            suggestions = re.sub(r"\n\n(Q\d+)\s*\n\n(Overall Score:)", r"\n\n\1 \2", suggestions)
            # Fallback: ensure any remaining 'Overall Score:' starts a new paragraph
            suggestions = re.sub(r"(Overall Score:)", r"\n\n\1", suggestions)
        st.markdown(suggestions)

        st.subheader("Scores per Question")
        scores = feedback_data.get("scores_per_question", [])
        total_score = feedback_data.get("total_score", 0)
        max_score = len(st.session_state.interview_history) * 10

        if scores and len(scores) == len(st.session_state.interview_history):
            for i, score in enumerate(scores):
                st.markdown(f"- **Q{i+1}:** {score}/10")
        elif scores:
             st.warning(f"Note: Number of scores ({len(scores)}) doesn't match number of questions ({len(st.session_state.interview_history)}). Displaying raw scores: {scores}")
        else:
             st.markdown("Scores could not be determined.")

        st.subheader("Total Score for Round")
        if max_score > 0:
            st.markdown(f"**{total_score} / {max_score}**")
        else:
             st.markdown("N/A (No questions answered)")

        # Optionally show raw feedback for debugging
        # with st.expander("Show Raw Feedback Data (for debugging)"):
        #      st.json(feedback_data)



    else:
        st.warning("Feedback is not available for this round.")


    # --- Option to Start New Round ---
    st.markdown("---")
    if st.button("Start Another Round"):
        # Reset state for a new round, keeping resume and agent
        st.session_state.stage = 'select_round'
        st.session_state.selected_round_key = None
        st.session_state.questions = []
        st.session_state.current_question_index = 0
        st.session_state.interview_history = []
        st.session_state.feedback = None
        # Clear spoken flags for questions
        keys_to_clear = [k for k in st.session_state if k.startswith('spoken_q')]
        for key in keys_to_clear:
             del st.session_state[key]
        st.rerun()


    # --- Option to Upload New Resume ---
    if st.button("Upload New Resume"):
         # Resets everything including resume and agent
        # Clean up the old resume file if present
        try:
            cleanup_temp_file(st.session_state.get('temp_resume_path'))
        except Exception:
            pass

        # Preserve a small set of keys we want to keep (e.g., job description)
        preserved = {}
        if 'job_description' in st.session_state:
            preserved['job_description'] = st.session_state.job_description

        # Clear only interview-related session keys to keep user-entered job description
        keys_to_remove = [k for k in list(st.session_state.keys()) if k not in preserved]
        for key in keys_to_remove:
            try:
                del st.session_state[key]
            except Exception:
                pass

        # Restore preserved values
        for k, v in preserved.items():
            st.session_state[k] = v

        # Reset to upload stage so user can upload a new resume
        st.session_state.stage = 'upload'
        st.rerun()







