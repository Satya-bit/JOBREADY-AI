# This is the Interview Agent class that handles the interview process, 
# including question generation

import json
import ast
from core.llm_service import generate_completion
from core.audio_io import speak_text, record_audio, transcribe_audio
from core.feedback_generator import generate_feedback_and_scores
from prompts.question_prompts import get_question_generation_prompt

class InterviewAgent:
    def __init__(self, resume_text: str, job_description: str):
        self.resume_text = resume_text,
        self.job_description = job_description
        self.interview_history = [] #
        self.current_round_info = None
        self.feedback = None

    def _generate_questions(self, round_name: str, num_questions: int) -> list[str]:
        """Generates questions for the specified round using LLM."""
        print(f"\nGenerating {num_questions} questions for the {round_name} round based on your resume...")
        prompt = get_question_generation_prompt(self.resume_text,self.job_description, round_name, num_questions)
        raw_response = generate_completion(prompt, max_tokens=300 * num_questions, temperature=0.8) # Allow more tokens

        # Trying to parse the response as a Python list
        try:
            # Cleaning potential markdown/fences
            raw_response = raw_response.strip().strip('```python').strip('```').strip() #To extract the list of questions from raw_text
            questions = ast.literal_eval(raw_response) # To convert string '[Q1,Q2,Q3]' to [Q1,Q2,Q3] Safer than eval
            if isinstance(questions, list) and all(isinstance(q, str) for q in questions):
                 # Ensure we have the correct number, truncate or pad if necessary (though LLM should follow instructions)
                if len(questions) > num_questions:
                    print(f"Warning: LLM generated {len(questions)} questions, expected {num_questions}. Using the first {num_questions}.")
                    questions = questions[:num_questions]
                elif len(questions) < num_questions:
                     print(f"Warning: LLM generated only {len(questions)} questions, expected {num_questions}.")
                     # Could try generating more, or just proceed
                
                print("Questions generated successfully.")
                return questions
            else:
                raise ValueError("Parsed result is not a list of strings.")
        except (SyntaxError, ValueError, TypeError) as e:
            print(f"Error parsing questions from LLM response: {e}")
            print(f"Raw response was: {raw_response}")
            # Fallback: Try splitting by newline if list parsing fails and response looks like lines of questions
            lines = [line.strip() for line in raw_response.split('\n') if line.strip()]
            if lines and len(lines) >= num_questions // 2: # Heuristic: if we got at least half the questions as lines
                print("Falling back to line splitting for questions.")
                return lines[:num_questions]
            else:
                print("Could not generate questions properly. Using generic questions.")
                # Generic fallback questions
                return [
                    f"Tell me about your experience relevant to the {round_name} role based on your resume.",
                    "What is your biggest strength related to this area?",
                    "Can you describe a challenge you faced and how you overcame it?",
                    "Where do you see yourself in 5 years?",
                    "Do you have any questions for me?" # Always good to include
                ][:num_questions]

