"""
Scraper para AngoEmprego.com
"""
from typing import List, Dict
from .base_scraper import BaseScraper


class AngoEmpregoScraper(BaseScraper):
    """Scraper para o site AngoEmprego"""
    
    def __init__(self):
        super().__init__('AngoEmprego', 'https://angoemprego.com')
    
    def scrape(self) -> List[Dict]:
        """
        Realiza o scraping do AngoEmprego
        Estrutura real identificada: usa classes 'job_listing' e 'type-job_listing'
        """
        jobs = []
        
        # Busca a página principal de vagas
        soup = self.fetch_page(self.base_url)
        if not soup:
            return jobs
        
        # Seletores REAIS do AngoEmprego
        # As vagas estão em <li class="job_listing type-job_listing ...">
        job_listings = soup.select('li.job_listing.type-job_listing')
        
        for job_elem in job_listings[:20]:  # Limitar a 20 vagas por scraping
            try:
                # Procurar o link principal da vaga
                link_elem = job_elem.select_one('a')
                if not link_elem:
                    continue
                
                job_url = link_elem.get('href', '')
                if not job_url.startswith('http'):
                    job_url = self.base_url.rstrip('/') + job_url
                
                # Título geralmente está dentro do link ou em h3
                title_elem = job_elem.select_one('h3') or job_elem.select_one('.job-title') or link_elem
                title = self.clean_text(title_elem.get_text()) if title_elem else 'Vaga disponível'
                
                # Empresa pode estar em diferentes locais
                company_elem = (
                    job_elem.select_one('.company') or 
                    job_elem.select_one('.job-company') or
                    job_elem.select_one('div.company strong')
                )
                company = self.clean_text(company_elem.get_text()) if company_elem else 'N/A'
                
                # Localização
                location_elem = (
                    job_elem.select_one('.location') or
                    job_elem.select_one('.job-location') or
                    job_elem.select_one('div.location')
                )
                location = self.clean_text(location_elem.get_text()) if location_elem else 'Angola'
                
                # Descrição curta se disponível
                description_elem = job_elem.select_one('.job-description') or job_elem.select_one('p')
                description = self.clean_text(description_elem.get_text())[:200] if description_elem else ''
                
                job = {
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description,
                    'url': job_url,
                    'source': self.name,
                    'posted_date': None
                }
                
                # Classificar e enriquecer com informações de TI
                job = self.classify_and_enrich_job(job)
                
                # Apenas adicionar se for vaga de TI
                if job.get('is_it_job'):
                    jobs.append(job)
                
            except Exception as e:
                print(f"Erro ao processar vaga no {self.name}: {e}")
                continue
        
        print(f"✓ {self.name}: {len(jobs)} vagas de TI encontradas")
        return jobs
