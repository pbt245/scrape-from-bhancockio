# CV Scraper with AI-Powered Candidate Analysis

An intelligent web scraper that extracts candidate CV data from various sources and uses AI to classify roles, score candidates, and match them against job descriptions.

## Features

- 🤖 **AI-Powered Extraction**: Uses DeepSeek AI to intelligently parse CV data
- 📊 **Comprehensive Data Model**: Extracts 50+ fields including personal info, skills, education, projects
- 🎯 **Role Classification**: Automatically classifies candidates into technical roles
- 📈 **JD Matching**: Scores candidates against job descriptions
- 🔍 **Multi-Source Support**: GitHub, ITviec, TopCV, and custom URLs
- 💾 **Multiple Export Formats**: CSV and JSON output

## Data Fields Extracted

### Personal Information

- Full Name (with Job Title + Level)
- Gender, Nationality, Date of Birth
- Address, Years of Experience
- Desired Work Locations, Job Rank

### Contact Information

- Phone Number
- Email
- Website / LinkedIn
- GitHub

### Skills & Languages

- Technical Skills (categorized: programming languages, frameworks, tools, etc.)
- Spoken Languages with proficiency levels

### Education

- Institution Name
- Degree, Major
- GPA, Duration

### Projects

- Project Name
- Description
- Time Period

### Achievements & Certifications

- Title, Description, Date

### HR Extension Fields

- Hiring Type
- IsTerminal
- Can Rehire
- Is Fsofter
- Is Utilization

### AI Analysis Fields (Auto-generated)

- **ai_matched_role**: Classified role (e.g., "Backend Developer", "Data Engineer")
- **ai_confidence_score**: Confidence in role classification (0-1)
- **ai_jd_match_score**: Match score against job description (0-100)
- **ai_seniority**: Determined seniority level
- **ai_recommendation**: Hiring recommendation (strong_yes/yes/maybe/no)
- **ai_reasoning**: Explanation of AI analysis

## Installation

```bash
# Clone the repository
cd deepseek-ai-web-crawler

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

## Configuration

### API Keys

Get your free API key from [Groq](https://console.groq.com/) and add it to `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Configure Sources

Edit `config.py` to enable/disable CV sources:

```python
CV_SOURCES = {
    "github": {
        "base_url": "https://github.com/search?q=location:vietnam+type:user",
        "css_selector": "[class*='user-list-info']",
        "enabled": True,
    },
    # Add more sources...
}
```

## Usage

### Basic Usage (Scrape GitHub Profiles)

```bash
python main.py
```

This will:

1. Scrape GitHub profiles from Vietnam
2. Extract CV data using AI
3. Classify roles and assign seniority levels
4. Save results to `candidates_cv_data.csv` and `candidates_cv_data.json`

### Scrape Custom URL

```bash
python main.py --url "https://example.com/candidates" "[class*='profile']"
```

### With Job Description Matching

Create a `job_description.txt` file with your JD, then run:

```bash
python main.py
```

The scraper will automatically:

- Load the job description
- Match each candidate against the JD
- Calculate match scores
- Provide hiring recommendations

## Example Job Description (job_description.txt)

```
Senior Backend Engineer - Python/Go

Requirements:
- 5+ years of backend development experience
- Strong proficiency in Python and Go
- Experience with microservices architecture
- Knowledge of AWS/GCP
- Experience with Docker and Kubernetes
- Strong SQL and NoSQL database skills
- Experience with Redis, RabbitMQ, or Kafka

Nice to have:
- Experience with gRPC
- Knowledge of system design patterns
- Previous startup experience
```

## Output

### CSV Output (`candidates_cv_data.csv`)

Flattened structure with all fields in columns, suitable for Excel/Google Sheets analysis.

### JSON Output (`candidates_cv_data.json`)

Full nested structure preserving all data relationships:

```json
{
  "personal_info": {
    "full_name": "John Doe",
    "job_title": "Senior Backend Engineer",
    "years_of_experience": "5"
  },
  "skills": [
    {
      "name": "Python",
      "proficiency": "Expert",
      "category": "programming_languages"
    },
    { "name": "Docker", "proficiency": "Advanced", "category": "tools" }
  ],
  "ai_matched_role": "Backend Developer",
  "ai_confidence_score": 0.92,
  "ai_jd_match_score": 85,
  "ai_recommendation": "strong_yes"
}
```

## Project Structure

```
deepseek-ai-web-crawler/
├── main.py                      # Main orchestration script
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── models/
│   └── candidate.py            # Pydantic data models for CV structure
├── utils/
│   ├── scraper_utils.py        # Web scraping utilities
│   ├── ai_utils.py             # AI analysis and matching
│   └── data_utils.py           # Data processing and export
└── README.md                    # This file
```

## AI Analysis Pipeline

1. **CV Extraction**: AI parses unstructured web content into structured CV data
2. **Role Classification**: Analyzes skills, experience, and education to classify role
3. **Seniority Assessment**: Determines candidate level based on experience and projects
4. **JD Matching** (optional): Compares candidate profile against job requirements
5. **Scoring & Ranking**: Assigns scores and ranks candidates by relevance

## Customization

### Add New CV Sources

Edit `config.py` and add your source:

```python
CV_SOURCES = {
    "mysite": {
        "base_url": "https://mysite.com/resumes",
        "css_selector": "[class*='resume']",
        "enabled": True,
    }
}
```

### Modify Role Classifications

Update the role list in `config.py`:

```python
ROLE_CLASSIFICATIONS = [
    "Your Custom Role",
    # ... more roles
]
```

### Adjust AI Temperature

For more creative/diverse extraction, increase temperature in `config.py`:

```python
AI_TEMPERATURE = 0.5  # Higher = more creative, Lower = more consistent
```

## Best Practices

1. **Rate Limiting**: The scraper includes sleep intervals. Adjust in `main.py` if needed.
2. **API Costs**: Groq offers generous free tier. Monitor usage at console.groq.com.
3. **Data Privacy**: Ensure compliance with data privacy laws when scraping.
4. **Validation**: Always validate extracted data before use in production.

## Troubleshooting

### No candidates extracted

- Check if the website structure has changed
- Verify CSS selectors in `config.py`
- Enable verbose mode to see AI extraction details

### Low match scores

- Ensure job description is detailed and specific
- Check that required skills are clearly listed
- Verify candidate data quality

### API errors

- Verify GROQ_API_KEY in `.env`
- Check API rate limits
- Ensure internet connection

## License

MIT License - feel free to use and modify for your needs.

## Disclaimer

This tool is for educational and recruitment purposes. Always respect:

- Website terms of service
- robots.txt files
- Data privacy regulations (GDPR, CCPA, etc.)
- Rate limiting and bandwidth

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues and questions, please open a GitHub issue.
