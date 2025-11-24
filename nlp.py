import google.generativeai as genai
import os

# Load Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "models/gemini-2.5-flash"

# ------------------------ HELPERS ------------------------
def call_gemini(prompt):
    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    return response.text

# ------------------------ FEATURES ------------------------

def summarize_text(text):
    prompt = f"""
    Summarize the following text into clean, clear academic notes:

    {text}
    """
    return call_gemini(prompt)


def section_wise_summaries(text):
    prompt = f"""
    Read the following text and generate a research-paper-style summary.
    Divide it into the following sections:

    1. Short Summary (Abstract) – a concise overview of the whole text.
    2. Research Objective – what is the main purpose or question of this research.
    3. Methodology – methods, approaches, or procedures used.
    4. Key Findings – main results or discoveries.
    5. Conclusions – overall conclusions drawn from the research.
    6. Significance – importance, implications, or impact of the findings.

    Ensure each section is clear, concise, and written in a formal research style.

    Text:
    {text}
    """
    return call_gemini(prompt)



def create_question_bank(text):
    prompt = f"""
    Generate 25 high-quality MCQs from the following text.
    For each MCQ, include:
    - Question
    - 4 options (A/B/C/D)
    - Correct answer only

    Text:
    {text}
    """
    return call_gemini(prompt)


def create_written_answer_questions(text):
    prompt = f"""
    Using the text below, generate:
    - 10 very short answer questions
    - 10 short answer questions
    - 10 long answer / essay questions

    Text:
    {text}
    """
    return call_gemini(prompt)


def create_ppt_outline(text):
    prompt = f"""
    Create a clean structured PowerPoint outline.

    Format EXACTLY like this:

    Slide Title
    - Subtopic: one short sentence
    - Subtopic: one short sentence

    Slide Title 2
    - Subtopic: one short sentence
    - Subtopic: one short sentence

    Generate 10–12 slides based on this text:

    {text}
    """
    return call_gemini(prompt)


def generate_group_assignments(pdf_text):
    """
    Generates 3 unique assignments for 3 groups based on the PDF content.
    Each group has 3 questions worth 2.5 marks each (total 7.5 marks).
    """
    prompt = f"""
    Using the following PDF content, generate assignments for 3 groups:
    
    - Each group gets 3 unique, clear, academic questions directly related to the content.
    - Each question is worth 2.5 marks (total 7.5 marks per group).
    - Group 1: Roll ending 0,3,5,7
    - Group 2: Roll ending 1,6,8
    - Group 3: Roll ending 2,4,9
    - Format EXACTLY like:

    Group 1 (Roll ending 0,3,5,7):
    1. Question 1 (2.5 marks)
    2. Question 2 (2.5 marks)
    3. Question 3 (2.5 marks)

    Group 2 (Roll ending 1,6,8):
    1. Question 1 (2.5 marks)
    2. Question 2 (2.5 marks)
    3. Question 3 (2.5 marks)

    Group 3 (Roll ending 2,4,9):
    1. Question 1 (2.5 marks)
    2. Question 2 (2.5 marks)
    3. Question 3 (2.5 marks)

    PDF content:
    {pdf_text}
    """
    return call_gemini(prompt)

