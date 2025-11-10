"""
Gerenciador de scrapers e agendamento
"""
from typing import List, Dict
from scrapers import AngoEmpregoScraper, JobArtisScraper
from database import Database
from config import Config


class ScraperManager:
    """Gerencia a execução dos scrapers"""
    
    def __init__(self):
        self.db = Database()
        self.scrapers = [
            AngoEmpregoScraper(),
            JobArtisScraper()
        ]
    
    def run_all_scrapers(self) -> Dict:
        """
        Executa todos os scrapers e salva as vagas na base de dados
        Returns: Estatísticas da execução
        """
        print("🔍 Iniciando scraping de vagas...")
        
        total_scraped = 0
        total_new = 0
        
        for scraper in self.scrapers:
            try:
                jobs = scraper.scrape()
                scraped_count = len(jobs)
                new_count = 0
                
                for job in jobs:
                    if self.db.add_job(job):
                        new_count += 1
                
                total_scraped += scraped_count
                total_new += new_count
                
                print(f"  {scraper.name}: {new_count} novas de {scraped_count} vagas")
                
            except Exception as e:
                print(f"❌ Erro no scraper {scraper.name}: {e}")
        
        stats = {
            'total_scraped': total_scraped,
            'total_new': total_new,
            'timestamp': None
        }
        
        print(f"✅ Scraping concluído: {total_new} novas vagas adicionadas")
        return stats
    
    def get_jobs(self, limit: int = 50, source: str = None) -> List[Dict]:
        """Obtém vagas da base de dados"""
        return self.db.get_jobs(limit=limit, source=source)
    
    def get_stats(self) -> Dict:
        """Obtém estatísticas das vagas"""
        return self.db.get_stats()
