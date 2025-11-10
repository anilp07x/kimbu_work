# KimbuWork - Copilot Instructions

## Project Overview
KimbuWork is a minimalist Flask-based job aggregator focused on employment opportunities in Angola. The application uses web scraping to collect job listings from AngoEmprego and JobArtis, storing them in SQLite with automatic updates.

## Tech Stack
- **Backend Framework**: Flask 3.0 (web framework)
- **Web Scraping**: BeautifulSoup4, Requests
- **Database**: SQLite3 (with custom ORM wrapper)
- **Job Scheduling**: APScheduler (automatic scraping)
- **Frontend**: HTML5, Tailwind CSS (via CDN), Vanilla JavaScript
- **Configuration**: python-dotenv for environment variables

## Development Environment

### Python Environment
- Uses virtual environment (`.venv/`)
- Python 3.13
- Windows-focused development (PowerShell)

### Activating Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### Installing Dependencies
```powershell
pip install -r requirements.txt
```

## Project Architecture

### Key Components
1. **Web Application** (`app.py`): Flask routes, templates, and API endpoints
2. **Database Layer** (`database.py`): SQLite wrapper with job storage and retrieval
3. **Scraper System**:
   - `scrapers/base_scraper.py`: Abstract base class for all scrapers
   - `scrapers/angoemprego_scraper.py`: AngoEmprego scraper implementation
   - `scrapers/jobartis_scraper.py`: JobArtis scraper implementation
4. **Scraper Manager** (`scraper_manager.py`): Orchestrates scraper execution
5. **Scheduler**: APScheduler runs scrapers every 6 hours (configurable)
6. **Configuration** (`config.py`): Centralized settings from `.env`

### Design Patterns
- **Template Method**: `BaseScraper` defines scraping workflow, subclasses implement site-specific parsing
- **Singleton Database Connection**: Context manager for SQLite connections
- **Background Scheduling**: APScheduler for periodic scraping without blocking Flask
- **Responsive Design**: Mobile-first with Tailwind CSS utility classes

## Development Workflows

### First-Time Setup
1. Copy environment template:
```powershell
Copy-Item .env.example .env
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

### Running the Application
Use the initialization script (recommended):
```powershell
python run.py
```

Or run Flask directly:
```powershell
python app.py
```

Access at: `http://localhost:5000`

### Manual Scraping
Trigger via web UI ("Atualizar Agora" button) or API:
```powershell
curl -X POST http://localhost:5000/api/scrape
```

### Database Management
SQLite database (`jobs.db`) is created automatically on first run.
Reset database: delete `jobs.db` and restart application.

## Coding Conventions

### Web Scraping
- **Inherit from `BaseScraper`**: All scrapers must extend the abstract base class
- **Use `fetch_page()`**: Built-in method handles requests with proper headers
- **Return List[Dict]**: Each scraper's `scrape()` must return job dictionaries with keys:
  - `title`, `company`, `location`, `description`, `url`, `source`, `posted_date`
- **CSS Selectors**: Scrapers use templates - adjust selectors by inspecting target sites
- **Error Handling**: Wrap parsing in try-except to skip malformed jobs gracefully
- **Limit Results**: Default to 20 jobs per scraping run to avoid overload

### Flask Routes
- **Templates**: Use Jinja2 in `templates/index.html`
- **API Prefix**: All API endpoints under `/api/*` return JSON
- **Error Responses**: Return JSON with `success: false` and HTTP error codes
- **Stats Calculation**: Use `Database.get_stats()` for aggregated data

### Database
- **No ORM**: Direct SQLite3 with `row_factory = sqlite3.Row` for dict-like access
- **Unique Constraint**: Job URLs are unique - `add_job()` returns `False` if duplicate
- **Boolean Fields**: Use `is_new` flag to track unseen jobs
- **Indexing**: Indexes on `source`, `posted_date`, and `is_new` for performance

## File Organization
```
kimbu_work/
├── .venv/                      # Virtual environment (git ignored)
├── .github/
│   └── copilot-instructions.md # AI agent instructions
├── scrapers/                   # Scraper modules
│   ├── __init__.py
│   ├── base_scraper.py         # Abstract base class
│   ├── angoemprego_scraper.py  # AngoEmprego implementation
│   └── jobartis_scraper.py     # JobArtis implementation
├── templates/
│   └── index.html              # Main web interface
├── app.py                      # Flask application + routes
├── run.py                      # Initialization script
├── config.py                   # Configuration from .env
├── database.py                 # SQLite wrapper
├── scraper_manager.py          # Scraper orchestration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .env                        # Environment variables (git ignored)
├── jobs.db                     # SQLite database (git ignored)
└── README.md                   # Documentation
```

## External Dependencies
- **No external services required**: Fully self-contained
- **SQLite**: Built-in with Python (no installation needed)
- **Tailwind CSS**: Loaded via CDN (no build step)

## Localization
- Target audience: Angola (Portuguese language context)
- Consider pt-PT or pt-AO locale for date formatting and UI text
- Use pytz for timezone handling (Africa/Luanda)

## Performance Considerations
- Use async scraping with FastAPI + aioredis for multiple portals simultaneously
- Cache parsed job listings in Redis with appropriate TTL
- Batch database operations with pandas for efficiency
- Use matplotlib's non-blocking mode for GUI integration

## Common Tasks

### Adding a New Job Portal Scraper
1. **Create new file**: `scrapers/new_portal_scraper.py`
2. **Inherit from BaseScraper**:
```python
from .base_scraper import BaseScraper

class NewPortalScraper(BaseScraper):
    def __init__(self):
        super().__init__('NewPortal', 'https://newportal.com')
    
    def scrape(self):
        jobs = []
        soup = self.fetch_page(self.base_url)
        # Implement parsing logic
        return jobs
```

3. **Register in `scrapers/__init__.py`**:
```python
from .new_portal_scraper import NewPortalScraper
__all__ = [..., 'NewPortalScraper']
```

4. **Add to ScraperManager** in `scraper_manager.py`:
```python
self.scrapers = [
    AngoEmpregoScraper(),
    JobArtisScraper(),
    NewPortalScraper()  # Add here
]
```

### Adjusting CSS Selectors
1. Open target website in browser (F12 developer tools)
2. Inspect job listing elements
3. Identify unique CSS selectors for: title, company, location, link
4. Update selectors in scraper's `scrape()` method:
```python
job_listings = soup.select('.actual-class-name')  # Replace with real selector
```

### Creating New API Endpoints
Add to `app.py` following RESTful conventions:
```python
@app.route('/api/your-endpoint')
def api_your_endpoint():
    # Logic here
    return jsonify({'data': result})
```

## Important Notes

### Scraper Templates
The included scrapers (`angoemprego_scraper.py`, `jobartis_scraper.py`) are **templates with placeholder selectors**. They will not work correctly until you:
1. Visit the actual websites
2. Inspect the HTML structure
3. Replace generic selectors (`.job-listing`, `.job-item`) with actual class names

### Scheduling Configuration
- Default: scraping runs every 6 hours
- Configure in `.env`: `SCRAPING_INTERVAL_HOURS=6`
- First scraping happens immediately on startup
- Manual scraping available via web UI or POST to `/api/scrape`

### Database Schema
Jobs table includes:
- `is_new` flag: Marks unseen jobs (set to `0` via `/api/mark-seen`)
- `scraped_at`: Timestamp of when job was added
- `url` UNIQUE constraint: Prevents duplicate entries

### Frontend Design
- **Tailwind CSS via CDN**: No build step required
- **Google Fonts (Inter)**: Loaded from CDN
- **Vanilla JavaScript**: No framework dependencies
- **Responsive**: Mobile-first design with breakpoints

## License & Repository
- **License**: MIT (Copyright 2025 Anilson Da Silva Pedro)
- **Repository**: [github.com/anilp07x/kimbu_work](https://github.com/anilp07x/kimbu_work)
