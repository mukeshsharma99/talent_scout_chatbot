# utils.py
import json
from typing import Dict, Any, List
from prompts import EXIT_KEYWORDS, GATHER_FIELDS
import streamlit as st

# Simple simulated storage (in-memory). Replace with DB/files for production.
_SIMULATED_DB: List[Dict[str, Any]] = []

def is_exit_message(text: str) -> bool:
    t = (text or "").strip().lower()
    return any(t == k for k in EXIT_KEYWORDS)

def save_candidate(candidate: Dict[str, Any]) -> None:
    """
    Simulated save. In production, encrypt and store in a secure DB.
    """
    _SIMULATED_DB.append(candidate)

def get_all_candidates() -> List[Dict[str, Any]]:
    return _SIMULATED_DB

def validate_candidate_data(data: Dict[str, Any]) -> Dict[str, str]:
    errors = {}
    if not data.get("full_name") or len(data["full_name"].strip()) < 2:
        errors["full_name"] = "Please provide a valid full name."
    if not data.get("email") or "@" not in data.get("email", ""):
        errors["email"] = "Please provide a valid email address."
    # phone is optional but lightly validated if provided
    ph = data.get("phone")
    if ph and len(ph.strip()) < 7:
        errors["phone"] = "Please provide a valid phone number."
    return errors

def pretty_print_questions_json(qjson: dict) -> str:
    return json.dumps(qjson, indent=2)
