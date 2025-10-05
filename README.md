**AI MOCK INTERVIEW AGENT (voice based)**

**=>DEMO LINK**

Demo Link- https://drive.google.com/file/d/17-T8bA7h-7s3fD9Me5yYYSFDmRtUC4dL/view 

**=>REPORT LINK**

Report Link- https://drive.google.com/file/d/1O7i19UQc-kBeo5w8_z8NonKHHXgECiW0/view?usp=sharing

**=>What does this platform offer?**

-Role-specific question generation. Different question generation for practice.

-Supports PDF(even scanned) & Word file for resume.

-Personalized interview sessions based on the candidate’s resume and job description.

-Voice-based interview agent.

-Front camera integration for a real interview feel.

-Real-time coaching/candidate feedback.


**=>USER INTERFACE**

**1) Enter Job Description**   

<img width="1903" height="921" alt="image" src="https://github.com/user-attachments/assets/84a53172-4f05-4e8f-a021-86bc8331624f" />

**Job Description from LinkedIn which I entered**

<img width="662" height="662" alt="image" src="https://github.com/user-attachments/assets/cfe71d73-2d64-4ecd-a3d3-89a6ebb8e622" />


**2) Upload the resume**


<img width="1875" height="887" alt="image" src="https://github.com/user-attachments/assets/6162e623-27e2-48f0-ac36-d8a6ab059e0b" />

**My Resume**

<img width="836" height="811" alt="image" src="https://github.com/user-attachments/assets/53971ff8-8775-4819-80f8-4ce2df86b6f2" />


**3) Select round**


<img width="1879" height="842" alt="image" src="https://github.com/user-attachments/assets/f8b5479b-05dc-47ec-87f0-3c228d2c5dea" />


**4) The agent asks the question(voice is heard, this is done using Eleven Labs API, not possible to show this just by pictures, will upload a demo of this soon). Just vague answers- User can either record or submit text answers.**


<img width="1884" height="906" alt="image" src="https://github.com/user-attachments/assets/847ca6a4-80e8-4351-b637-ddba68e0d4dc" />


**5) Relevant Answer**


<img width="1889" height="897" alt="image" src="https://github.com/user-attachments/assets/17b22393-d00c-4e96-87e2-cab30f88fa42" />


**6) You can see the questions are asked based on Job description and my Resume.**


<img width="1902" height="892" alt="image" src="https://github.com/user-attachments/assets/8e1ff798-0b89-4a11-b48e-a65506cce6e5" />


**7) Feedback with scores. I just answered Q3 with relevant answer so I get highest marks for this question. Rest I got zero marks for all questions with a feedback. In teh end teh user can see the total scores**


<img width="1878" height="837" alt="image" src="https://github.com/user-attachments/assets/b454d536-2250-4170-9734-d93d4a7fd37b" />

<img width="1846" height="951" alt="image" src="https://github.com/user-attachments/assets/20355709-9129-4972-8a06-61c0494944b6" />

<img width="1907" height="942" alt="image" src="https://github.com/user-attachments/assets/b26d49fc-0182-4402-a1bf-95dcec4d44f9" />

**=>System Architecture**

<img width="1321" height="560" alt="image" src="https://github.com/user-attachments/assets/5dba41f3-bff9-42ab-b932-399b212a23e9" />



**=>Steps:**

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

So this way, the user gets a personalized experience based on the resume and job description. This also answers the questions: input needed, AI functionalities in the architecture, and outcomes.



**=>Techstacks and libraries used**
Python- For Backend

<img width="316" height="233" alt="image" src="https://github.com/user-attachments/assets/ff9af491-de40-4d2c-8a66-c4e658088298" />

Streamlit- For Frontend

<img width="320" height="166" alt="image" src="https://github.com/user-attachments/assets/95084bb4-79e7-458f-bc6f-a093a7fe7113" />

OPENAI API (gpt-4.1-mini)- For LLM Service

<img width="274" height="106" alt="image" src="https://github.com/user-attachments/assets/899ad2c6-bdd8-45e8-8aff-abf7420b2217" />

ElevenLabs(eleven_multilingual_v2)- For giving voice

<img width="309" height="186" alt="image" src="https://github.com/user-attachments/assets/eb1069ee-dc25-430e-bc5d-7f1ff417d996" />

Pytesseract/fitz/docx- For parsing a resume

<img width="259" height="181" alt="image" src="https://github.com/user-attachments/assets/3b317937-a6f2-4740-993c-f03a46171c72" />

Google Web Speech API- For transcription (when user selects to record answer.)

<img width="247" height="134" alt="image" src="https://github.com/user-attachments/assets/1737a685-8e43-4de2-9eaf-1e7d05f5c415" />
