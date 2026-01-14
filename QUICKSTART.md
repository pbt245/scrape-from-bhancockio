# Quick Start Guide - CV Scraper

## 🚀 5-Minute Setup

### Step 1: Get Your API Key

1. Visit https://console.groq.com/
2. Sign up for a free account
3. Create an API key
4. Copy the key

### Step 2: Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and paste your API key
nano .env  # or use any text editor
```

Your `.env` should look like:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Your First Scrape

```bash
python main.py
```

This will scrape GitHub profiles and output:

- `candidates_cv_data.csv` - Spreadsheet format
- `candidates_cv_data.json` - Full structured data

## 📊 Understanding the Output

### Top Candidates Display

After scraping, you'll see:

```
============================================================
TOP CANDIDATES
============================================================

1. John Doe
   Role: Backend Developer (confidence: 0.92)
   JD Match Score: 85.0/100
   Recommendation: strong_yes
```

### CSV File

Open `candidates_cv_data.csv` in Excel/Google Sheets to:

- Filter by skills
- Sort by match score
- Export for ATS systems

### JSON File

`candidates_cv_data.json` contains full nested data for:

- Custom integrations
- Further AI processing
- Database import

## 🎯 Common Use Cases

### 1. Scrape with Job Description Matching

```bash
# Create a JD file
cp job_description.txt.example job_description.txt
# Edit it with your actual JD
nano job_description.txt

# Run scraper (automatically detects JD file)
python main.py
```

### 2. Scrape Custom Website

```bash
python main.py --url "https://mysite.com/resumes" "[class='profile']"
```

### 3. Scrape LinkedIn-style Profile Pages

Edit `config.py`:

```python
CV_SOURCES = {
    "mysite": {
        "base_url": "https://mysite.com/professionals",
        "css_selector": "[class*='profile-card']",
        "enabled": True,
    }
}
```

Then in `config.py`, set:

```python
PRIMARY_SOURCE = "mysite"
```

Run:

```bash
python main.py
```

## 🔧 Customization Tips

### Adjust Number of Pages

In `main.py`, find:

```python
candidates = await scrape_github_profiles(max_pages=3)
```

Change `max_pages=3` to your desired number.

### Change Role Classifications

In `config.py`, modify:

```python
ROLE_CLASSIFICATIONS = [
    "Data Scientist",
    "ML Engineer",
    "Backend Developer",
    # Add your custom roles
]
```

### Modify Extraction Temperature

For more creative AI extraction, edit `config.py`:

```python
AI_TEMPERATURE = 0.5  # 0.0 = very consistent, 1.0 = very creative
```

## 🐛 Troubleshooting

### Error: "No module named crawl4ai"

```bash
pip install -r requirements.txt
```

### Error: "Invalid API key"

- Check your `.env` file
- Ensure no spaces around the `=`
- Verify key at https://console.groq.com/

### No candidates extracted

- Website might have anti-scraping measures
- Try adjusting CSS selectors in `config.py`
- Enable verbose mode to see detailed logs

### Low quality data

- Adjust CSS selector to target specific content
- Increase AI temperature for more flexible parsing
- Check if website requires authentication

## 📈 Next Steps

1. **Scale Up**: Increase `max_pages` for larger datasets
2. **Filter Results**: Use Excel/Python to filter by skills/scores
3. **Integrate**: Import JSON into your ATS or database
4. **Automate**: Set up cron job for regular scraping
5. **Customize**: Add new sources or modify extraction logic

## 💡 Pro Tips

- **Start Small**: Test with 1-2 pages first
- **Respect Rate Limits**: Adjust sleep intervals if needed
- **Validate Data**: Always review AI extracted data
- **Monitor Costs**: Check Groq usage (free tier is generous)
- **Save Raw Data**: Keep JSON files for re-analysis

## 📞 Getting Help

- Check the main [README.md](README.md) for detailed docs
- Review error messages carefully
- Enable verbose mode for debugging
- Verify website structure hasn't changed

Happy scraping! 🎉
