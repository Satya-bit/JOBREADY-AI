# This function is responsible for generating interview questions based 
# on the resume and job description user enters.
def get_question_generation_prompt(resume_text: str,job_description: str, round_name: str, num_questions: int = 5) -> str:
    """Creates a prompt to generate interview questions."""
    # Round-specific instructions (which can be expanded)
    round_instructions = {
        "HR": "Focus on behavioral questions, cultural fit, salary expectations (ask indirectly), and general background.",
        "Technical": "Focus on specific technical skills, technologies, and project experiences mentioned in the resume., Also ask technical questions related to the job description's mentioned skills and technologies, never forget this part. So this round should be mixture of questions asked from both resume and job description. Include questions from both resume and job description",
        "Managerial": "Focus on leadership potential, team collaboration, conflict resolution, project management approaches, and career goals.",
        "General": "Ask a mix of behavioral, situational, resume-based and job description questions."
    }
    instructions = round_instructions.get(round_name, round_instructions["General"])

    prompt = f"""
    Based on the following resume text and Job Description, generate {num_questions} relevant interview questions for a '{round_name}' round.
    {instructions}
    Ensure the questions are open-ended and encourage detailed answers. Do not ask questions that can be answered with a simple 'yes' or 'no'.
    Format the output as a Python list of strings, like this:
    ["Question 1?", "Question 2?", "Question 3?"]

    Job Description:
    ---
    {job_description}
    ---
    
    Resume Text:
    ---
    {resume_text}
    ---

    Generate the list of questions now:
    """
    return prompt