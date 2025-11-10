"""
Scraper base para sites de emprego
"""
from abc import ABC, abstractmethod
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from config import Config


class BaseScraper(ABC):
    """Classe base para todos os scrapers"""
    
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.headers = {
            'User-Agent': Config.USER_AGENT
        }
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Busca e retorna o conteúdo HTML de uma página"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Erro ao buscar {url}: {e}")
            return None
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Método abstrato para realizar o scraping
        Deve retornar lista de dicionários com as vagas
        """
        pass
    
    def clean_text(self, text: str) -> str:
        """Limpa e normaliza texto"""
        if not text:
            return ""
        return " ".join(text.strip().split())
