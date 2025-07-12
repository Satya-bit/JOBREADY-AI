# This file is responsible for generating feedback and scores which is used by the 
# frontend(streamlit) to display the feedback and scores to the user.


from core.llm_service import generate_completion
from prompts.feedback_prompts import get_feedback_prompt
import re # For parsing score


def clean_markdown(text: str) -> str:
    # Removes **bold** or *italic* markdown formatting
    return re.sub(r'\*+', '', text).strip()

def generate_feedback_and_scores(resume_text: str,job_description: str, round_name: str, qa_pairs: list[dict]) -> dict:
    """Generates feedback, suggestions, and scores using the LLM."""
    print("\nGenerating feedback based on your interview...")
    prompt = get_feedback_prompt(resume_text,job_description, round_name, qa_pairs) #prompt to the LLM

    raw_feedback = generate_completion(prompt, max_tokens=1000, temperature=0.5) # More factual feedback from the LLM(Answer)

    # Basic parsing (can be improved with more robust methods)
    feedback_data = {
        "overall_feedback": "Could not parse feedback.",
        "suggestions": "Could not parse suggestions.",
        "scores_per_question": [],
        "total_score": 0,
        "raw_output": raw_feedback # Include raw output for debugging
    }
   
    try:
        # Extract Overall Feedback
        overall_match = re.search(r"Overall Feedback:(.*?)(Suggestions:|$)", raw_feedback, re.IGNORECASE | re.DOTALL) #Everything between Feedback and Suggestions
        if overall_match:
            feedback_data["overall_feedback"] = clean_markdown(overall_match.group(1).strip())

        # Extract Suggestions
        suggestions_match = re.search(r"Suggestions:(.*?)(Scores per Question:|Total Score:|$)", raw_feedback, re.IGNORECASE | re.DOTALL)

        if suggestions_match:
            feedback_data["suggestions"] = clean_markdown(suggestions_match.group(1).strip())

        # Extract Scores per Question (assuming format like "Q1 Score: 8/10")
        scores = []
        # Look for lines starting with Q followed by a number, then Score:, then number/10
        score_matches = re.findall(r"Q\d+ Overall Score:\s*(\d+)\s*/\s*10", raw_feedback, re.IGNORECASE)

        if score_matches:
            scores = [int(s) for s in score_matches]
            # Ensure number of scores matches number of questions
            if len(scores) == len(qa_pairs):
                 feedback_data["scores_per_question"] = scores
            else:
                print(f"Warning: Parsed {len(scores)} scores, but expected {len(qa_pairs)}. Storing raw scores.")
                # Store anyway, maybe user can interpret
                feedback_data["scores_per_question"] = scores # Or could set to []

        # Extract Total Score
        total_score_match = re.search(r"Total Score:\s*(\d+)", raw_feedback, re.IGNORECASE)

        if total_score_match:
             # Tries to parse total score directly
            feedback_data["total_score"] = int(total_score_match.group(1))
        elif feedback_data["scores_per_question"] and len(feedback_data["scores_per_question"]) == len(qa_pairs):
             # If parsing failed but individual scores look okay, calculate sum
            feedback_data["total_score"] = sum(feedback_data["scores_per_question"])
            print("Calculated total score from individual scores.")
        else:
            print("Warning: Could not parse total score from LLM output.")
            feedback_data["total_score"] = sum(feedback_data["scores_per_question"]) # Fallback


    except Exception as e:
        print(f"Error parsing feedback: {e}")
        print("Returning raw feedback in 'raw_output' field.")

    print("Feedback generated.")
    return feedback_data