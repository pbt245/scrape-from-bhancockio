import csv
import json
from typing import List
from models.candidate import Candidate


def flatten_candidate_for_csv(candidate: dict) -> dict:
    """
    Flatten nested candidate structure for CSV export.

    Args:
        candidate: Candidate dictionary with nested structure

    Returns:
        Flattened dictionary suitable for CSV
    """
    flat = {}

    # Personal Info
    personal = candidate.get("personal_info", {})
    flat["full_name"] = personal.get("full_name", "")
    flat["job_title"] = personal.get("job_title", "")
    flat["level"] = personal.get("level", "")
    flat["gender"] = personal.get("gender", "")
    flat["nationality"] = personal.get("nationality", "")
    flat["date_of_birth"] = personal.get("date_of_birth", "")
    flat["address"] = personal.get("address", "")
    flat["years_of_experience"] = personal.get("years_of_experience", "")
    flat["desired_work_locations"] = ", ".join(
        personal.get("desired_work_locations", [])
    )
    flat["job_rank"] = personal.get("job_rank", "")

    # Contact Info
    contact = candidate.get("contact_info", {})
    flat["phone_number"] = contact.get("phone_number", "")
    flat["email"] = contact.get("email", "")
    flat["website"] = contact.get("website", "")
    flat["linkedin"] = contact.get("linkedin", "")
    flat["github"] = contact.get("github", "")

    # Skills (as comma-separated list)
    skills = candidate.get("skills", [])
    flat["skills"] = ", ".join([s.get("name", "") for s in skills if s.get("name")])
    flat["skill_categories"] = ", ".join(
        list(set([s.get("category", "") for s in skills if s.get("category")]))
    )

    # Languages
    languages = candidate.get("languages", [])
    flat["languages"] = ", ".join(
        [f"{l.get('language', '')} ({l.get('proficiency', '')})" for l in languages]
    )

    # Education (first entry or summary)
    education = candidate.get("education", [])
    if education:
        edu = education[0]
        flat["education"] = (
            f"{edu.get('degree', '')} in {edu.get('major', '')} - {edu.get('institution_name', '')}"
        )
        flat["gpa"] = edu.get("gpa", "")
    else:
        flat["education"] = ""
        flat["gpa"] = ""

    # Projects count and summary
    projects = candidate.get("projects", [])
    flat["projects_count"] = len(projects)
    flat["projects_summary"] = " | ".join(
        [p.get("project_name", "") for p in projects[:3]]
    )

    # Achievements count
    achievements = candidate.get("achievements", [])
    flat["achievements_count"] = len(achievements)
    flat["achievements"] = " | ".join([a.get("title", "") for a in achievements[:3]])

    # HR Fields
    hr = candidate.get("hr_fields", {})
    flat["hiring_type"] = hr.get("hiring_type", "")
    flat["is_terminal"] = hr.get("is_terminal", "")
    flat["can_rehire"] = hr.get("can_rehire", "")
    flat["is_fsofter"] = hr.get("is_fsofter", "")
    flat["is_utilization"] = hr.get("is_utilization", "")

    # AI Analysis Fields
    flat["ai_matched_role"] = candidate.get("ai_matched_role", "")
    flat["ai_confidence_score"] = candidate.get("ai_confidence_score", "")
    flat["ai_jd_match_score"] = candidate.get("ai_jd_match_score", "")
    flat["ai_seniority"] = candidate.get("ai_seniority", "")
    flat["ai_recommendation"] = candidate.get("ai_recommendation", "")
    flat["ai_reasoning"] = candidate.get("ai_reasoning", "")

    return flat


def save_candidates_to_csv(candidates: List[dict], filename: str):
    """
    Save candidates to CSV file with flattened structure.

    Args:
        candidates: List of candidate dictionaries
        filename: Output CSV filename
    """
    if not candidates:
        print("No candidates to save.")
        return

    # Flatten all candidates
    flattened = [flatten_candidate_for_csv(c) for c in candidates]

    # Get all unique field names
    fieldnames = set()
    for candidate in flattened:
        fieldnames.update(candidate.keys())
    fieldnames = sorted(list(fieldnames))

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened)

    print(f"✓ Saved {len(candidates)} candidates to '{filename}'")


def save_candidates_to_json(candidates: List[dict], filename: str):
    """
    Save candidates to JSON file with full structure.

    Args:
        candidates: List of candidate dictionaries
        filename: Output JSON filename
    """
    if not candidates:
        print("No candidates to save.")
        return

    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(candidates, file, indent=2, ensure_ascii=False)

    print(f"✓ Saved {len(candidates)} candidates to '{filename}'")


def load_job_description(filename: str) -> str:
    """
    Load job description from a text file.

    Args:
        filename: Path to JD file

    Returns:
        Job description text
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Job description file '{filename}' not found.")
        return ""
