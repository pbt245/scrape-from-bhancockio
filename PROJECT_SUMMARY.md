# CV Scraper Project Summary

## 🎯 Project Overview

Successfully built an AI-powered CV scraping system that:

- Scrapes candidate CVs from multiple sources (GitHub, job sites, custom URLs)
- Uses DeepSeek AI to intelligently extract and parse CV data
- Classifies candidates by role and seniority level
- Matches candidates against job descriptions with scoring
- Exports results in CSV and JSON formats

## 📁 Project Structure

```
deepseek-ai-web-crawler/
├── main.py                      # Main orchestration script
├── config.py                    # Configuration (sources, roles, settings)
├── requirements.txt             # Dependencies
├── README.md                    # Complete documentation
├── QUICKSTART.md               # Quick start guide
├── .env.example                # Environment template
├── job_description.txt.example # JD template
├── .gitignore                  # Git ignore rules
│
├── models/
│   └── candidate.py           # Pydantic CV data models
│
└── utils/
    ├── scraper_utils.py       # Web scraping utilities
    ├── ai_utils.py            # AI analysis & matching
    └── data_utils.py          # Data export utilities
```

## 🔑 Key Features Implemented

### 1. Comprehensive Data Model

Created `Candidate` model with all required fields:

- **Personal Info**: Name, title, level, gender, nationality, DOB, address, experience, locations, rank
- **Contact**: Phone, email, website, LinkedIn, GitHub
- **Skills**: Technical skills with categories and proficiency
- **Languages**: Spoken languages with proficiency levels
- **Education**: Institution, degree, major, GPA, duration
- **Projects**: Name, description, time period
- **Achievements**: Certifications and awards
- **HR Fields**: Hiring type, terminal status, rehire eligibility, Fsofter status, utilization

### 2. AI-Powered Extraction

- Uses DeepSeek R1 Distill Llama 70B via Groq API
- Intelligent parsing of unstructured CV content
- Structured output following Pydantic schema
- Configurable temperature for extraction consistency

### 3. Role Classification

Automatic classification into technical roles:

- Software Engineer, Frontend/Backend/Full Stack Developer
- DevOps Engineer, Data Engineer, Data Scientist
- ML Engineer, Mobile Developer, QA Engineer
- Product Manager, Technical Lead, Architect
- Confidence scoring for classifications

### 4. Job Description Matching

- Load JD from text file
- AI-powered matching analysis
- Match score (0-100)
- Identifies matched/missing skills
- Lists candidate strengths and concerns
- Provides hiring recommendation (strong_yes/yes/maybe/no)

### 5. Multi-Source Support

Configured sources:

- **GitHub**: Search for developer profiles by location
- **ITviec**: Vietnamese IT job site (ready to enable)
- **TopCV**: Vietnamese CV site (ready to enable)
- **Custom URLs**: Support for any website

### 6. Data Export

- **CSV**: Flattened structure for spreadsheet analysis
- **JSON**: Full nested structure for programmatic use
- Comprehensive field mapping
- UTF-8 encoding for international characters

## 🚀 Usage Patterns

### Basic Scraping

```bash
python main.py
```

- Scrapes GitHub profiles from Vietnam
- Extracts CV data using AI
- Classifies roles automatically
- Outputs ranked candidate list

### With Job Description

```bash
# Create job_description.txt with your JD
python main.py
```

- Performs all basic scraping
- Matches candidates against JD
- Calculates match scores
- Provides hiring recommendations

### Custom URL

```bash
python main.py --url "https://example.com/resumes" "[class='profile']"
```

- Scrapes specific URL
- Uses provided CSS selector
- Processes with AI

## 🤖 AI Pipeline

1. **CV Extraction**

   - Scrape web page
   - Extract content using CSS selector
   - Parse with AI using schema
   - Validate required fields

2. **Role Classification**

   - Analyze skills, experience, education
   - Match against role definitions
   - Assign confidence score
   - Determine seniority level

3. **JD Matching** (if JD provided)

   - Compare candidate profile to JD
   - Identify matched/missing skills
   - Score overall fit (0-100)
   - Generate recommendation

4. **Scoring & Ranking**
   - Sort by match score
   - Display top candidates
   - Export full results

## 📊 Output Format

### CSV Columns

```
full_name, job_title, level, gender, nationality, date_of_birth,
address, years_of_experience, desired_work_locations, job_rank,
phone_number, email, website, linkedin, github,
skills, skill_categories, languages, education, gpa,
projects_count, projects_summary, achievements_count, achievements,
hiring_type, is_terminal, can_rehire, is_fsofter, is_utilization,
ai_matched_role, ai_confidence_score, ai_jd_match_score,
ai_seniority, ai_recommendation, ai_reasoning
```

### JSON Structure

```json
{
  "personal_info": {...},
  "contact_info": {...},
  "skills": [...],
  "languages": [...],
  "education": [...],
  "projects": [...],
  "achievements": [...],
  "hr_fields": {...},
  "ai_matched_role": "...",
  "ai_confidence_score": 0.0-1.0,
  "ai_jd_match_score": 0-100,
  ...
}
```

## 🔧 Configuration Options

### In config.py:

- `CV_SOURCES`: Add/remove scraping sources
- `PRIMARY_SOURCE`: Set default source
- `AI_PROVIDER`: Change AI model
- `AI_TEMPERATURE`: Adjust extraction consistency
- `ROLE_CLASSIFICATIONS`: Customize role list
- `SENIORITY_LEVELS`: Define level hierarchy
- `SKILL_CATEGORIES`: Organize skill types

### In main.py:

- `max_pages`: Number of pages to scrape
- Sleep intervals: Rate limiting
- Source selection logic

## 🎓 Technical Stack

- **Web Scraping**: Crawl4AI (async web crawler)
- **AI/LLM**: DeepSeek R1 via Groq API
- **Data Models**: Pydantic
- **HTTP**: Requests library
- **Async**: asyncio
- **Data Export**: CSV, JSON (stdlib)

## ✅ Quality Features

- Duplicate detection (by email/name)
- Field validation
- Error handling
- Rate limiting
- Verbose logging
- UTF-8 support
- Clean code structure
- Comprehensive documentation

## 📝 Documentation

- **README.md**: Full documentation with examples
- **QUICKSTART.md**: 5-minute setup guide
- **Code comments**: Inline documentation
- **.env.example**: Environment template
- **job_description.txt.example**: JD template

## 🔒 Best Practices Implemented

- Environment variables for secrets
- .gitignore for sensitive files
- Modular code structure
- Type hints with Pydantic
- Async operations for performance
- Configurable rate limiting
- Comprehensive error handling

## 🎯 Use Cases

1. **Recruitment**: Screen candidates automatically
2. **Talent Sourcing**: Find candidates matching JD
3. **Market Research**: Analyze skill trends
4. **ATS Integration**: Export for applicant tracking
5. **Portfolio Analysis**: Evaluate developer profiles

## 🚀 Future Enhancement Ideas

- Database integration (PostgreSQL, MongoDB)
- Web UI dashboard
- Scheduled automated scraping
- Email notifications
- Advanced filtering/search
- Resume parsing from PDF/DOCX
- Multi-language support
- Batch JD matching
- API endpoint creation
- Integration with LinkedIn API

## 📈 Performance

- Async scraping for speed
- Configurable page limits
- Rate limiting for politeness
- Efficient data structures
- Minimal API calls

## ✨ Highlights

✅ All required CV fields supported
✅ AI-powered parsing and reasoning
✅ JD matching and scoring
✅ Role classification
✅ Multiple output formats
✅ Extensible architecture
✅ Production-ready code
✅ Comprehensive documentation
✅ Easy to customize
✅ Free AI tier (Groq)

---

**Project Status**: ✅ Complete and ready to use!
