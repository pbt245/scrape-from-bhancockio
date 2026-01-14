import json
import os
from typing import List, Set, Tuple, Optional

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)

from models.candidate import Candidate


def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.

    Returns:
        BrowserConfig: The configuration settings for the browser.
    """
    return BrowserConfig(
        browser_type="chromium",
        headless=False,  # Set to True in production
        verbose=True,
    )


def get_cv_extraction_strategy() -> LLMExtractionStrategy:
    """
    Returns the configuration for CV extraction using LLM.

    Returns:
        LLMExtractionStrategy: The settings for extracting CV data using AI.
    """
    from config import AI_PROVIDER, AI_TEMPERATURE

    return LLMExtractionStrategy(
        provider=AI_PROVIDER,
        api_token=os.getenv("GROQ_API_KEY"),
        schema=Candidate.model_json_schema(),
        extraction_type="schema",
        instruction=(
            "Extract complete CV/resume information from the content. "
            "Parse the following data carefully:\n"
            "1. Personal Information: name, job title, level, gender, nationality, DOB, address, "
            "years of experience, desired locations, job rank\n"
            "2. Contact: phone, email, website, LinkedIn, GitHub\n"
            "3. Skills: technical skills with categories (programming languages, frameworks, tools, etc.)\n"
            "4. Languages: spoken languages with proficiency levels\n"
            "5. Education: institution, degree, major, GPA, duration\n"
            "6. Projects: project name, description, time period\n"
            "7. Achievements and certifications\n"
            "8. HR fields: hiring type, terminal status, rehire eligibility\n\n"
            "If information is not available, leave the field empty or null. "
            "Be thorough and extract all available information."
        ),
        input_format="markdown",
        temperature=AI_TEMPERATURE,
        verbose=True,
    )


def get_role_classification_strategy(candidate_data: dict) -> LLMExtractionStrategy:
    """
    Returns strategy for classifying candidate role based on CV data.

    Args:
        candidate_data: The candidate's CV data

    Returns:
        LLMExtractionStrategy: Strategy for role classification
    """
    from config import ROLE_CLASSIFICATIONS, SENIORITY_LEVELS, AI_PROVIDER

    roles_str = ", ".join(ROLE_CLASSIFICATIONS)
    levels_str = ", ".join(SENIORITY_LEVELS)

    return LLMExtractionStrategy(
        provider=AI_PROVIDER,
        api_token=os.getenv("GROQ_API_KEY"),
        extraction_type="custom",
        instruction=(
            f"Based on the candidate's CV data, classify their role and seniority level.\n\n"
            f"Available roles: {roles_str}\n"
            f"Available levels: {levels_str}\n\n"
            f"Candidate data:\n{json.dumps(candidate_data, indent=2)}\n\n"
            "Provide a JSON response with:\n"
            "- matched_role: the most suitable role from the list\n"
            "- confidence_score: 0-1 indicating confidence in the classification\n"
            "- seniority_level: the candidate's seniority level\n"
            "- reasoning: brief explanation of the classification\n"
            "- key_skills: top 5 most relevant skills for this role"
        ),
        verbose=True,
    )


async def check_page_exists(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
) -> bool:
    """
    Checks if a page exists and has content.

    Args:
        crawler: The web crawler instance
        url: The URL to check
        session_id: The session identifier

    Returns:
        bool: True if page exists with content, False otherwise
    """
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            session_id=session_id,
        ),
    )

    if result.success and result.cleaned_html:
        # Check for common "no results" indicators
        no_results_indicators = [
            "No Results Found",
            "No candidates found",
            "No profiles available",
            "0 results",
        ]
        return not any(
            indicator in result.cleaned_html for indicator in no_results_indicators
        )

    return False


async def fetch_cv_page(
    crawler: AsyncWebCrawler,
    url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
) -> Tuple[List[dict], bool]:
    """
    Fetches and processes a single page of CV data.

    Args:
        crawler: The web crawler instance
        url: The URL to fetch
        css_selector: The CSS selector to target CV content
        llm_strategy: The LLM extraction strategy
        session_id: The session identifier

    Returns:
        Tuple containing:
            - List of extracted candidate dictionaries
            - Boolean indicating if more pages exist
    """
    print(f"Fetching CVs from: {url}")

    # Check if page exists
    page_exists = await check_page_exists(crawler, url, session_id)
    if not page_exists:
        print("No more results found.")
        return [], False

    # Fetch page content with extraction strategy
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=llm_strategy,
            css_selector=css_selector,
            session_id=session_id,
        ),
    )

    if not (result.success and result.extracted_content):
        print(f"Error fetching page: {result.error_message}")
        return [], False

    # Parse extracted content
    try:
        extracted_data = json.loads(result.extracted_content)
        if not extracted_data:
            print("No CV data extracted from page.")
            return [], False

        print(f"Extracted {len(extracted_data)} candidate profiles")
        return extracted_data, True

    except json.JSONDecodeError as e:
        print(f"Error parsing extracted data: {e}")
        return [], False


def validate_candidate(candidate: dict, required_fields: List[str]) -> bool:
    """
    Validates if a candidate has the minimum required fields.

    Args:
        candidate: Candidate dictionary
        required_fields: List of required top-level fields

    Returns:
        bool: True if valid, False otherwise
    """
    for field in required_fields:
        if field not in candidate or not candidate[field]:
            return False

    # Additional validation: must have at least name or email
    has_identifier = False
    if "personal_info" in candidate:
        if candidate["personal_info"].get("full_name"):
            has_identifier = True
    if "contact_info" in candidate:
        if candidate["contact_info"].get("email"):
            has_identifier = True

    return has_identifier


def deduplicate_candidates(
    candidates: List[dict],
    seen_identifiers: Set[str],
) -> List[dict]:
    """
    Remove duplicate candidates based on email or name.

    Args:
        candidates: List of candidate dictionaries
        seen_identifiers: Set of already seen identifiers

    Returns:
        List of unique candidates
    """
    unique_candidates = []

    for candidate in candidates:
        # Create identifier from email or name
        identifier = None

        if "contact_info" in candidate and candidate["contact_info"].get("email"):
            identifier = candidate["contact_info"]["email"].lower()
        elif "personal_info" in candidate and candidate["personal_info"].get(
            "full_name"
        ):
            identifier = candidate["personal_info"]["full_name"].lower()

        if identifier and identifier not in seen_identifiers:
            seen_identifiers.add(identifier)
            unique_candidates.append(candidate)
        elif identifier:
            print(f"Duplicate candidate found: {identifier}")

    return unique_candidates
