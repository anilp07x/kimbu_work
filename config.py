"""
Configurações do KimbuWork
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuração base da aplicação"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'jobs.db')
    
    # Scraping
    SCRAPING_INTERVAL_HOURS = int(os.getenv('SCRAPING_INTERVAL_HOURS', 6))
    USER_AGENT = os.getenv(
        'USER_AGENT',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    
    # Notificações
    ENABLE_EMAIL_NOTIFICATIONS = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'False') == 'True'
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_EMAIL = os.getenv('SMTP_EMAIL', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    
    ENABLE_TELEGRAM_NOTIFICATIONS = os.getenv('ENABLE_TELEGRAM_NOTIFICATIONS', 'False') == 'True'
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # Sites de emprego
    JOB_SITES = [
        {
            'name': 'AngoEmprego',
            'url': 'https://angoemprego.com',
            'enabled': True
        },
        {
            'name': 'JobArtis',
            'url': 'https://www.jobartis.com',
            'enabled': True
        }
    ]
