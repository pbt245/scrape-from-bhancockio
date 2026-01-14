# config.py

# CV Scraping Sources Configuration
# We'll target Vietnamese job sites and GitHub profiles

CV_SOURCES = {
    "itviec": {
        "base_url": "https://itviec.com/it-jobs",
        "css_selector": "[class*='job-details'], [class*='candidate']",
        "enabled": True,
    },
    "topcv": {
        "base_url": "https://www.topcv.vn/viec-lam-it",
        "css_selector": "[class*='cv-item'], [class*='profile']",
        "enabled": False,  # Enable after testing
    },
    "github": {
        "base_url": "https://github.com/search?q=location:vietnam+type:user",
        "css_selector": "[class*='user-list-info']",
        "enabled": True,
    },
}

# Primary source to use for scraping
PRIMARY_SOURCE = "github"

# AI Configuration
AI_PROVIDER = "groq/deepseek-r1-distill-llama-70b"
AI_TEMPERATURE = 0.3  # Lower temperature for more consistent extraction

# Required fields for candidate validation
REQUIRED_CV_FIELDS = [
    "personal_info",
    "contact_info",
]

# Skills categories for classification
SKILL_CATEGORIES = [
    "programming_languages",
    "frameworks",
    "databases",
    "cloud_platforms",
    "tools",
    "soft_skills",
]

# Role classification options
ROLE_CLASSIFICATIONS = [
    "Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Data Engineer",
    "Data Scientist",
    "ML Engineer",
    "Mobile Developer",
    "QA Engineer",
    "Product Manager",
    "Technical Lead",
    "Architect",
    "Other",
]

# Seniority levels
SENIORITY_LEVELS = [
    "Intern",
    "Fresher",
    "Junior",
    "Mid-level",
    "Senior",
    "Lead",
    "Principal",
    "Staff",
]

# Output configuration
OUTPUT_CSV_FILE = "candidates_cv_data.csv"
OUTPUT_JSON_FILE = "candidates_cv_data.json"
