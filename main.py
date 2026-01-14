"""
CV Scraper with AI-powered candidate analysis
Scrapes candidate CV data and uses AI to classify roles and match against JD
"""

import asyncio
import sys

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import (
    CV_SOURCES,
    PRIMARY_SOURCE,
    REQUIRED_CV_FIELDS,
    OUTPUT_CSV_FILE,
    OUTPUT_JSON_FILE,
)
from utils.data_utils import (
    save_candidates_to_csv,
    save_candidates_to_json,
    load_job_description,
)
from utils.scraper_utils import (
    fetch_cv_page,
    get_browser_config,
    get_cv_extraction_strategy,
    validate_candidate,
    deduplicate_candidates,
)
from utils.ai_utils import score_candidates

load_dotenv()


async def scrape_github_profiles(max_pages: int = 5) -> list:
    """
    Scrape GitHub profiles for CV data.

    Args:
        max_pages: Maximum number of pages to scrape

    Returns:
        List of candidate dictionaries
    """
    print("\n=== Scraping GitHub Profiles ===\n")

    browser_config = get_browser_config()
    llm_strategy = get_cv_extraction_strategy()
    session_id = "cv_scraper_session"

    all_candidates = []
    seen_identifiers = set()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for page_num in range(1, max_pages + 1):
            # GitHub search pagination
            url = f"https://github.com/search?q=location:vietnam+type:user&p={page_num}"

            candidates, has_more = await fetch_cv_page(
                crawler,
                url,
                CV_SOURCES["github"]["css_selector"],
                llm_strategy,
                session_id,
            )

            if not has_more or not candidates:
                print(f"No more results on page {page_num}")
                break

            # Validate and deduplicate
            valid_candidates = [
                c for c in candidates if validate_candidate(c, REQUIRED_CV_FIELDS)
            ]

            unique_candidates = deduplicate_candidates(
                valid_candidates, seen_identifiers
            )
            all_candidates.extend(unique_candidates)

            print(f"Page {page_num}: Found {len(unique_candidates)} unique candidates")

            # Be respectful with rate limiting
            await asyncio.sleep(3)

    return all_candidates


async def scrape_custom_url(url: str, css_selector: str = None) -> list:
    """
    Scrape a custom URL for CV data.

    Args:
        url: The URL to scrape
        css_selector: Optional CSS selector for targeting content

    Returns:
        List of candidate dictionaries
    """
    print(f"\n=== Scraping Custom URL: {url} ===\n")

    browser_config = get_browser_config()
    llm_strategy = get_cv_extraction_strategy()
    session_id = "cv_custom_session"

    if not css_selector:
        css_selector = "body"  # Default to entire page

    async with AsyncWebCrawler(config=browser_config) as crawler:
        candidates, _ = await fetch_cv_page(
            crawler,
            url,
            css_selector,
            llm_strategy,
            session_id,
        )

        # Validate candidates
        valid_candidates = [
            c for c in candidates if validate_candidate(c, REQUIRED_CV_FIELDS)
        ]

        print(f"Found {len(valid_candidates)} valid candidates")
        return valid_candidates


async def main():
    """
    Main entry point for CV scraper
    """
    print("=" * 60)
    print("CV SCRAPER WITH AI ANALYSIS")
    print("=" * 60)

    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--url" and len(sys.argv) > 2:
            # Scrape custom URL
            custom_url = sys.argv[2]
            css_selector = sys.argv[3] if len(sys.argv) > 3 else None
            candidates = await scrape_custom_url(custom_url, css_selector)
        else:
            print("Usage: python main.py [--url <url> [css_selector]]")
            return
    else:
        # Default: scrape GitHub profiles
        candidates = await scrape_github_profiles(max_pages=3)

    if not candidates:
        print("\n❌ No candidates found during scraping.")
        return

    print(f"\n✓ Scraped {len(candidates)} candidates")

    # Optional: Load job description for matching
    jd_text = None
    try:
        jd_text = load_job_description("job_description.txt")
        if jd_text:
            print("✓ Loaded job description for matching")
    except:
        print("ℹ No job description file found. Skipping JD matching.")

    # AI Analysis: Score and classify candidates
    print("\n=== AI Analysis: Scoring and Classifying Candidates ===\n")
    scored_candidates = await score_candidates(candidates, jd_text)

    # Display top candidates
    print("\n" + "=" * 60)
    print("TOP CANDIDATES")
    print("=" * 60)
    for idx, candidate in enumerate(scored_candidates[:5], 1):
        name = candidate.get("personal_info", {}).get("full_name", "Unknown")
        role = candidate.get("ai_matched_role", "Unknown")
        score = candidate.get("ai_jd_match_score", 0)
        confidence = candidate.get("ai_confidence_score", 0)

        print(f"\n{idx}. {name}")
        print(f"   Role: {role} (confidence: {confidence:.2f})")
        print(f"   JD Match Score: {score:.1f}/100")
        if candidate.get("ai_recommendation"):
            print(f"   Recommendation: {candidate.get('ai_recommendation')}")

    # Save results
    print("\n=== Saving Results ===\n")
    save_candidates_to_csv(scored_candidates, OUTPUT_CSV_FILE)
    save_candidates_to_json(scored_candidates, OUTPUT_JSON_FILE)

    print("\n" + "=" * 60)
    print(f"✅ COMPLETE! Processed {len(scored_candidates)} candidates")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
