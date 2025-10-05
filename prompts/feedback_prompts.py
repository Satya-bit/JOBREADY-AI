# This function is responsible for generating feedback and scores based 
# on the interview questions and answers.

def get_feedback_prompt(resume_text: str,job_description: str, round_name: str, qa_pairs: list[dict], scoring_criteria: str = None) -> str:
    """Creates a prompt to generate feedback and scores."""

    if not scoring_criteria:
        scoring_criteria = """
        Score each answer out of 10 based on the following criteria:
        1. Relevance: How well does the answer address the question? (0-3 points)
        2. Clarity: How clear and concise is the answer? (0-2 points)
        3. Detail/Examples: Does the answer provide sufficient detail or examples (like STAR method where applicable)? (0-3 points)
        4. Resume Alignment: How well does the answer align with the candidate's resume? (0-2 points)
        """

    formatted_qa = "\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in qa_pairs])

    prompt = f"""
    You are an expert interviewer providing feedback on a mock interview.
    The interview was for the '{round_name}' round.
    Job description is provided below for context.
    The candidate's resume is provided below for context.
    Analyze the following question and answer pairs from the interview.


    Job Description:
    ---
    {job_description}
    ---     
    Resume Context:
    ---
    {resume_text}
    ---

    Interview Questions and Answers:
    ---
    {formatted_qa}
    ---

    Instructions:
    1. Provide overall constructive feedback for the candidate's performance in this round. Focus on strengths and areas for improvement. Give as Overall Feedback.
    2. Give specific suggestions for improvement based on their answers. Give as Suggestions. Donot provide summary of the feedback, just suggestions.
    3. Score each answer individually based on the provided criteria as Q1 Score: x/10, Q2 Score: y/10, etc. Follow this strictly and no other formats, everytime you generate answer. And then also give individual scores for each criteria mentioned above per question, like score for Relevance, Clarity, Detail/Examples, and Resume Alignment for individual question.
       For example, for Question 2, you might follow format like this:
       Q2- question asked by you to the candidate in the interview (Donot include this line in the answer, keep the original question you asked)
       Relevance: 0/3 (Answer “no idea” does not address the question)  
       Clarity: 1/2 (Clear but unhelpful)  
       Detail/Examples: 0/3 (No explanation or example)  
       Resume Alignment: 0/2 (No alignment shown) 
       Q2 Overall Score: 1/10 
       All of the above 6 should be in new line
    4. Calculate a total score for the round (sum of individual scores) as Total Score: x/10. Follow this format strictly and no other formats, everytime you generate answer.
       For example, you might follow format like this:
       Total Score: 4/10
    5. Format the output clearly, starting with Overall Feedback, then Suggestions, then a list of scores per question, and finally the Total Score.
   
    Scoring Criteria (per question, max 10 points):
    {scoring_criteria}
    
    Additionally, if there are any spelling or transcription errors in the candidate's answer, please ensure they are automatically corrected. Even if the candidate records the answer accurately, transcription inconsistencies can occur, so it's important that the final output reflects the correct and intended response.      
    Generate the feedback and scores now:
    """
    return prompt