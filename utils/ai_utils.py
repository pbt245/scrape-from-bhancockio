"""
AI utilities for candidate analysis, role classification, and JD matching.
"""

import json
import os
from typing import Dict, Optional

from crawl4ai import LLMExtractionStrategy


async def classify_candidate_role(candidate_data: dict) -> dict:
    """
    Use AI to classify candidate's role based on their CV data.

    Args:
        candidate_data: The candidate's CV information

    Returns:
        Dictionary containing:
            - matched_role: classified role
            - confidence_score: confidence level (0-1)
            - seniority_level: determined seniority
            - reasoning: explanation of classification
            - key_skills: top relevant skills
    """
    from config import ROLE_CLASSIFICATIONS, SENIORITY_LEVELS, AI_PROVIDER

    # Prepare simplified data for analysis
    analysis_data = {
        "name": candidate_data.get("personal_info", {}).get("full_name", "Unknown"),
        "job_title": candidate_data.get("personal_info", {}).get("job_title"),
        "years_experience": candidate_data.get("personal_info", {}).get(
            "years_of_experience"
        ),
        "skills": [skill.get("name") for skill in candidate_data.get("skills", [])],
        "education": [edu.get("major") for edu in candidate_data.get("education", [])],
        "projects": [
            proj.get("project_name") for proj in candidate_data.get("projects", [])
        ],
    }

    roles_str = ", ".join(ROLE_CLASSIFICATIONS)
    levels_str = ", ".join(SENIORITY_LEVELS)

    prompt = f"""Analyze this candidate's profile and classify their role and seniority:

Candidate Data:
{json.dumps(analysis_data, indent=2)}

Available Roles: {roles_str}
Available Seniority Levels: {levels_str}

Return a JSON object with:
- matched_role: best matching role from the list
- confidence_score: float between 0-1
- seniority_level: most appropriate level
- reasoning: brief explanation (1-2 sentences)
- key_skills: array of top 5 most relevant skills

Respond ONLY with valid JSON."""

    try:
        # Use Groq API directly for classification
        import requests

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek-r1-distill-llama-70b",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert technical recruiter and HR analyst.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
                "response_format": {"type": "json_object"},
            },
        )

        if response.status_code == 200:
            result = response.json()
            classification = json.loads(result["choices"][0]["message"]["content"])
            return classification
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return {
                "matched_role": "Other",
                "confidence_score": 0.0,
                "seniority_level": "Unknown",
                "reasoning": "Classification failed",
                "key_skills": [],
            }

    except Exception as e:
        print(f"Error in role classification: {e}")
        return {
            "matched_role": "Other",
            "confidence_score": 0.0,
            "seniority_level": "Unknown",
            "reasoning": str(e),
            "key_skills": [],
        }


async def match_candidate_to_jd(candidate_data: dict, job_description: str) -> dict:
    """
    Match candidate CV against a job description using AI.

    Args:
        candidate_data: The candidate's CV data
        job_description: The job description text

    Returns:
        Dictionary containing:
            - match_score: overall match score (0-100)
            - matched_skills: skills that match JD requirements
            - missing_skills: required skills the candidate lacks
            - strengths: candidate's strengths for this role
            - concerns: potential concerns or gaps
            - recommendation: hire/interview/reject recommendation
    """
    from config import AI_PROVIDER

    # Prepare candidate summary
    candidate_summary = {
        "name": candidate_data.get("personal_info", {}).get("full_name"),
        "experience": candidate_data.get("personal_info", {}).get(
            "years_of_experience"
        ),
        "skills": [skill.get("name") for skill in candidate_data.get("skills", [])],
        "education": [
            f"{edu.get('degree')} in {edu.get('major')}"
            for edu in candidate_data.get("education", [])
        ],
        "projects": [
            proj.get("description") for proj in candidate_data.get("projects", [])
        ],
    }

    prompt = f"""Compare this candidate against the job description and provide a matching analysis:

Job Description:
{job_description}

Candidate Profile:
{json.dumps(candidate_summary, indent=2)}

Analyze and return a JSON object with:
- match_score: integer 0-100 indicating overall fit
- matched_skills: array of skills that match JD requirements
- missing_skills: array of required skills the candidate lacks
- strengths: array of 3-5 candidate strengths for this role
- concerns: array of 2-3 potential concerns or gaps
- recommendation: one of "strong_yes", "yes", "maybe", "no"
- reasoning: 2-3 sentences explaining the recommendation

Respond ONLY with valid JSON."""

    try:
        import requests

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek-r1-distill-llama-70b",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert technical recruiter analyzing candidate-job fit.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.3,
                "response_format": {"type": "json_object"},
            },
        )

        if response.status_code == 200:
            result = response.json()
            match_analysis = json.loads(result["choices"][0]["message"]["content"])
            return match_analysis
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return {
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "strengths": [],
                "concerns": ["Analysis failed"],
                "recommendation": "no",
                "reasoning": "Unable to perform analysis",
            }

    except Exception as e:
        print(f"Error in JD matching: {e}")
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "strengths": [],
            "concerns": [str(e)],
            "recommendation": "no",
            "reasoning": str(e),
        }


async def score_candidates(
    candidates: list, job_description: Optional[str] = None
) -> list:
    """
    Score and rank multiple candidates.

    Args:
        candidates: List of candidate dictionaries
        job_description: Optional JD to match against

    Returns:
        List of candidates with scores, sorted by relevance
    """
    scored_candidates = []

    for candidate in candidates:
        print(
            f"\nAnalyzing candidate: {candidate.get('personal_info', {}).get('full_name', 'Unknown')}"
        )

        # Classify role
        classification = await classify_candidate_role(candidate)
        candidate["ai_matched_role"] = classification.get("matched_role")
        candidate["ai_confidence_score"] = classification.get("confidence_score")
        candidate["ai_seniority"] = classification.get("seniority_level")
        candidate["ai_reasoning"] = classification.get("reasoning")
        candidate["ai_key_skills"] = classification.get("key_skills", [])

        # Match to JD if provided
        if job_description:
            jd_match = await match_candidate_to_jd(candidate, job_description)
            candidate["ai_jd_match_score"] = jd_match.get("match_score")
            candidate["ai_matched_skills"] = jd_match.get("matched_skills", [])
            candidate["ai_missing_skills"] = jd_match.get("missing_skills", [])
            candidate["ai_recommendation"] = jd_match.get("recommendation")
            candidate["ai_jd_reasoning"] = jd_match.get("reasoning")
        else:
            # Use role confidence as default score
            candidate["ai_jd_match_score"] = (
                classification.get("confidence_score", 0) * 100
            )

        scored_candidates.append(candidate)

    # Sort by match score (descending)
    scored_candidates.sort(key=lambda x: x.get("ai_jd_match_score", 0), reverse=True)

    return scored_candidates
