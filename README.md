**AI MOCK INTERVIEW AGENT (voice based)**

**=>DEMO LINK**

Demo Link- 


**=>What does this platform offer?**

-Role-specific question generation. Different question generation for practice.

-Supports PDF(even scanned) & Word file for resume.

-Personalized interview sessions based on the candidate’s resume and job description.

-Voice-based interview agent.

-Front camera integration for a real interview feel.

-Real-time coaching/candidate feedback.

-ATS Friendly feedback and scores.
**=>USER INTERFACE**

**1) Enter Job Description**   


**Job Description from LinkedIn which I entered**



**2) Upload the resume**



**My Resume**



**3) Select round**




**4) The agent asks the question(voice is heard, this is done using Eleven Labs API, not possible to show this just by pictures). Just vague answers- User can either record or submit text answers.**




**5) Relevant Answer**




**6) You can see the questions are asked based on Job description and my Resume.**



**7) Feedback with scores. In the end the user can see the total scores**


**8) You can also see the ATS friendly feedback.**


**=>System Architecture**

<img width="1321" height="560" alt="image" src="https://github.com/user-attachments/assets/5dba41f3-bff9-42ab-b932-399b212a23e9" />



**=>Steps for AI MOCK INTERVIEW:**

1. The user enters a job description.

2. User uploads their resume (PDF or DOCX). It is parsed using pytesseract OCR/fitz for PDF & DOCX for Word files. The system parses the resume using OCR or file reading tools

3. The user selects the interview round.

4. Based on the Resume, Job description & round selected, the agent generates question.

5. The AI agent generates personalized questions using the job description, resume & the round selected (using the OpenAI API).

6. The AI agent asks questions using voice (Eleven Labs API).

7. User answers the questions (by typing or recording).

8. If recorded, the answer is transcribed using Google Web Speech API.

9. The AI agent generates feedback and scores using the OpenAI API.

10. Feedback and scores are displayed.

**=>Steps for ATS friendly feedback and scores:**

1. Upload Job Description & Resume.

2. Select any one of the below options:

  - Tell me about the resume
  - What are the keywords that are missing
  - Percentage Match

So this way, the user gets a personalized experience based on the resume and job description. 


**=>Techstacks and libraries used**
Python- For Backend

<img width="316" height="233" alt="image" src="https://github.com/user-attachments/assets/ff9af491-de40-4d2c-8a66-c4e658088298" />

Streamlit- For Frontend

<img width="320" height="166" alt="image" src="https://github.com/user-attachments/assets/95084bb4-79e7-458f-bc6f-a093a7fe7113" />

GEMINI API (gemini-2.0-Flash & gemini-2.5-Pro)- For LLM Service

<img width="274" height="106" alt="image" src="https://github.com/user-attachments/assets/899ad2c6-bdd8-45e8-8aff-abf7420b2217" />

ElevenLabs(eleven_multilingual_v2)- For giving voice

<img width="309" height="186" alt="image" src="https://github.com/user-attachments/assets/eb1069ee-dc25-430e-bc5d-7f1ff417d996" />

Pytesseract/fitz/docx- For parsing a resume

<img width="259" height="181" alt="image" src="https://github.com/user-attachments/assets/3b317937-a6f2-4740-993c-f03a46171c72" />

Google Web Speech API- For transcription (when user selects to record answer.)

<img width="247" height="134" alt="image" src="https://github.com/user-attachments/assets/1737a685-8e43-4de2-9eaf-1e7d05f5c415" />
