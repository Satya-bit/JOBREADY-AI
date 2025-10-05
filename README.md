**JOBREADY AI- AI Powered Interview agent & ATS Tracker**

**=>DEMO LINK**

Demo Link- 


**=>What does this platform offer?**

-Role specific question generation. Different question generation for practice.

-Supports PDF(even scanned) & Word file for resume.

-Personalized interview sessions based on the candidate’s resume and job description.

-Voice-based interview agent.

-Front camera integration for a real interview feel.

-Real-time coaching/candidate feedback.

-ATS Friendly feedback and scores.
**=>USER INTERFACE**
<img width="1911" height="932" alt="image" src="https://github.com/user-attachments/assets/65443466-4159-4b31-ae87-e90de6a7652f" />

**1) Enter Job Description**   

<img width="1889" height="889" alt="image" src="https://github.com/user-attachments/assets/76c3bef4-a4ab-4166-b7e3-77a156d8b31b" />


**Job Description from LinkedIn which I entered**

<img width="1667" height="835" alt="image" src="https://github.com/user-attachments/assets/86ba200b-b1d4-4782-8f91-2bd4ac5ec954" />


**2) Upload the resume**

<img width="1737" height="771" alt="image" src="https://github.com/user-attachments/assets/fdf967a7-29cf-44d2-b14e-48e6ad3a44b6" />


**My Resume**

<img width="688" height="990" alt="image" src="https://github.com/user-attachments/assets/9de6d2f0-4784-4f4f-b8e2-3345934642fd" />


**3) Select round**

<img width="1746" height="752" alt="image" src="https://github.com/user-attachments/assets/4137552e-291b-42bd-a584-be8b7b673939" />


**4) The agent asks the question relvant to Job description and Resume(a voice is heard from the AI interview agent, this is done using Eleven Labs API, not possible to show this just by pictures). Just vague answer for this question- User can either record or submit text answers.**

<img width="1719" height="906" alt="image" src="https://github.com/user-attachments/assets/15352ad4-0799-4da7-a78a-74e020296705" />


**5) Relevant Answer**

<img width="1708" height="817" alt="image" src="https://github.com/user-attachments/assets/b5bfc620-000d-407a-8234-46cb226236b7" />


**6) You can see the questions are asked based on Job description and my Resume.**


**7) Feedback with scores. In the end the user can see the total scores**

<img width="1216" height="932" alt="image" src="https://github.com/user-attachments/assets/f7b19333-4b90-48ab-b2e2-5cee09334ad4" />

**8) An example of question being asked for HR Round.**

<img width="1706" height="643" alt="image" src="https://github.com/user-attachments/assets/21eb2f5d-84d8-4802-bf71-faacc317372e" />

**9) You can also see the ATS friendly feedback.**

<img width="1580" height="745" alt="image" src="https://github.com/user-attachments/assets/3998e876-6223-4523-ac1a-025f5b2d3abd" />

   **-Tell me about the Resume:** It will tell whether the candidate's profile aligns with the role. It will also tell about the strength and weakness of the candidate.
    <img width="1121" height="917" alt="image" src="https://github.com/user-attachments/assets/7e763a25-e353-4444-9cb9-e3f24afdbf1e" />

   **-What are the keywords that are missing:** It will display any keywords that are missing in the resume. 
    <img width="890" height="538" alt="image" src="https://github.com/user-attachments/assets/b0ecbf09-141b-4928-9a4c-a80755196bf2" />

   **-Percentage Match:** It tells about how much % the match is between job dscription and resume.
   <img width="832" height="282" alt="image" src="https://github.com/user-attachments/assets/a4e5a29a-92f7-4a43-bb43-e223d5ae28d9" />

**Note**-Only two questions are being asked in this demo. The number of questions can be increased as needed by the AI.

**=>System Architecture**

<img width="1321" height="560" alt="image" src="https://github.com/user-attachments/assets/5dba41f3-bff9-42ab-b932-399b212a23e9" />
<img width="1011" height="331" alt="image" src="https://github.com/user-attachments/assets/d528f91c-a23e-409b-9455-621df1444614" />



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

<img width="650" height="210" alt="image" src="https://github.com/user-attachments/assets/3fdf22f9-f46e-4a88-8d04-7a7c70b85f54" />

ElevenLabs(eleven_multilingual_v2)- For giving voice

<img width="309" height="186" alt="image" src="https://github.com/user-attachments/assets/eb1069ee-dc25-430e-bc5d-7f1ff417d996" />

Pytesseract/fitz/docx- For parsing a resume

<img width="259" height="181" alt="image" src="https://github.com/user-attachments/assets/3b317937-a6f2-4740-993c-f03a46171c72" />

Google Web Speech API- For transcription (when user selects to record answer.)

<img width="247" height="134" alt="image" src="https://github.com/user-attachments/assets/1737a685-8e43-4de2-9eaf-1e7d05f5c415" />
