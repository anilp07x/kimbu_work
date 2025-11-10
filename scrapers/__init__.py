"""
Módulo de scrapers para sites de emprego
"""
from .base_scraper import BaseScraper
from .angoemprego_scraper import AngoEmpregoScraper
from .jobartis_scraper import JobArtisScraper

__all__ = ['BaseScraper', 'AngoEmpregoScraper', 'JobArtisScraper']
