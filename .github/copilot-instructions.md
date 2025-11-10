# KimbuWork - Copilot Instructions

## Project Overview
KimbuWork is a Python-based job aggregator with an Angolan focus. The application uses web scraping to collect and organize employment opportunities from various local portals, providing a centralized and user-friendly view.

## Tech Stack
- **Backend Framework**: Flask (web framework) + FastAPI (async endpoints)
- **Web Scraping**: BeautifulSoup4, html5lib
- **Data Processing**: pandas, numpy
- **UI Framework**: CustomTkinter (modern tkinter alternative)
- **Data Storage**: Redis (with aioredis for async)
- **Visualization**: matplotlib
- **Deployment**: PyInstaller (Windows executable generation)

## Development Environment

### Python Environment
- Uses virtual environment (`.venv/`)
- Python 3.13 (based on installed packages)
- Windows-focused development (PowerShell, pywin32-ctypes)

### Activating Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### Installing Dependencies
Currently no `requirements.txt` exists. To freeze current dependencies:
```powershell
python -m pip freeze > requirements.txt
```

## Project Architecture

### Key Components
1. **Web Scraping Layer**: BeautifulSoup4 for parsing HTML from job portals
2. **API Layer**: Dual framework approach
   - Flask: Traditional web routes and templates
   - FastAPI: Modern async API endpoints with Pydantic validation
3. **Desktop UI**: CustomTkinter for native Windows GUI
4. **Caching/Storage**: Redis for temporary data storage and job listings cache
5. **Data Analysis**: pandas for processing scraped job data

### Design Patterns
- **Async I/O**: Uses FastAPI with uvicorn for concurrent scraping operations
- **Data Validation**: Pydantic models for structured job posting data
- **Cross-Origin Requests**: flask-cors enabled for web API access

## Development Workflows

### Running the Application
For Flask web server:
```powershell
python -m flask run
```

For FastAPI server:
```powershell
python -m uvicorn main:app --reload
```

For desktop GUI (if main entry point exists):
```powershell
python main.py
```

### Building Executable
Uses PyInstaller for Windows distribution:
```powershell
pyinstaller --onefile --windowed your_main_file.py
```

### Testing Redis Connection
Ensure Redis is running locally or configure connection string:
```powershell
redis-server  # Start Redis (requires separate installation)
```

## Coding Conventions

### Web Scraping
- Use `requests` with proper headers to avoid blocking
- Parse with BeautifulSoup4: `BeautifulSoup(html, 'html5lib')`
- Handle chardet/charset-normalizer for encoding detection
- Implement rate limiting and respectful scraping delays

### API Development
- FastAPI endpoints: Use Pydantic models for request/response validation
- Flask routes: Follow RESTful conventions
- CORS: Already configured via flask-cors for cross-origin access

### GUI Development
- CustomTkinter widgets for modern Windows look
- tkinterdnd2 for drag-and-drop functionality
- Use plyer for desktop notifications

### Data Processing
- pandas DataFrames for job listings aggregation
- numpy for numerical operations
- matplotlib for job market visualizations

## File Organization (Expected)
```
kimbu_work/
├── .venv/              # Virtual environment (excluded from git)
├── scrapers/           # Web scraping modules per job portal
├── api/                # FastAPI/Flask routes
├── models/             # Pydantic data models
├── gui/                # CustomTkinter UI components
├── utils/              # Helper functions
├── static/             # Flask static assets
├── templates/          # Flask/Jinja2 templates
├── config.py           # Configuration management
└── main.py             # Application entry point
```

## External Dependencies
- **Redis**: Required for caching scraped jobs (install separately)
- **PyInstaller**: For creating standalone executables
- **Windows-specific**: Uses pywin32-ctypes for Windows integration

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
1. Create module in `scrapers/portal_name.py`
2. Implement BeautifulSoup4 parsing logic
3. Return standardized Pydantic model (JobPosting)
4. Add to scraper registry/scheduler

### Creating API Endpoints
FastAPI (preferred for new async endpoints):
```python
@app.get("/jobs", response_model=List[JobPosting])
async def get_jobs():
    # Async implementation
```

Flask (for traditional web pages):
```python
@app.route("/jobs")
def get_jobs():
    # Sync implementation
```

## Notes
- Currently in early development stage (minimal source code present)
- Virtual environment has comprehensive dependencies installed
- License: MIT (Copyright 2025 Anilson Da Silva Pedro)
- Repository: GitHub (anilp07x/kimbu_work)
