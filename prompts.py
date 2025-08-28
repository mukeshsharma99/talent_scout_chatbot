# prompts.py
"""
Centralized prompt templates and prompt-generation helpers.
"""

from typing import List

SYSTEM_INSTRUCTION = (
    "You are TalentScout's Hiring Assistant — a professional, concise assistant that helps screen candidates. "
    "You should: 1) gather required candidate details, 2) ask follow-up clarifying questions if needed, "
    "3) generate 3-5 technical questions per declared technology in the candidate's tech stack, and "
    "4) always be respectful and maintain conversation context. "
    "Do not store or share candidate PII outside the designated backend. When the user types an exit keyword, respond with "
    "\"Thank you — your details were recorded. We'll get back to you.\""
)

EXIT_KEYWORDS = ["exit", "quit", "bye", "goodbye", "stop"]

GATHER_FIELDS = [
    ("full_name", "Full Name"),
    ("email", "Email Address"),
    ("phone", "Phone Number"),
    ("years_experience", "Years of Experience"),
    ("desired_positions", "Desired Position(s)"),
    ("location", "Current Location"),
    ("tech_stack", "Tech Stack (comma-separated)"),
]

def generate_question_prompt(tech_list: List[str], difficulty: str = "intermediate") -> str:
    """
    Builds the prompt to ask the LLM to generate 3-5 questions per technology.
    """
    techs_clean = [t.strip() for t in tech_list if t.strip()]
    if not techs_clean:
        techs_clean = ["general software engineering"]
    tech_lines = "\n".join(f"- {t}" for t in techs_clean)
    prompt = (
        f"You are an experienced technical interviewer. For each technology below, generate 3-5 clear, "
        f"targeted technical interview questions appropriate for a {difficulty} level candidate. "
        f"For each question include: (1) the question text, (2) a brief expected answer / key points (2-3 sentences), "
        f"and (3) a difficulty tag (easy/medium/hard). Present output as JSON with technology as the key. "
        f"Technologies:\n{tech_lines}\n"
        f"Keep answers compact and avoid asking the candidate to perform long coding — prefer concise conceptual or short code snippet questions."
    )
    return prompt

def generate_greeting(name: str = None) -> str:
    if name:
        return f"Hello {name}! I'm the TalentScout Hiring Assistant. I'll collect a few details and ask technical questions based on your tech stack."
    return "Hello! I'm the TalentScout Hiring Assistant. I'll collect a few details and ask technical questions based on your tech stack."
