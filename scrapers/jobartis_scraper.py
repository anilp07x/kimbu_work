"""
Scraper para JobArtis.com
"""
from typing import List, Dict
from .base_scraper import BaseScraper


class JobArtisScraper(BaseScraper):
    """Scraper para o site JobArtis"""
    
    def __init__(self):
        super().__init__('JobArtis', 'https://www.jobartis.com')
    
    def scrape(self) -> List[Dict]:
        """
        Realiza o scraping do JobArtis
        Estrutura real: vagas estão em 'panel panel-default' com links '/emprego-...'
        """
        jobs = []
        
        # JobArtis tem página específica de vagas
        vagas_url = self.base_url.rstrip('/') + '/vagas-emprego'
        soup = self.fetch_page(vagas_url)
        if not soup:
            # Tentar página inicial também
            soup = self.fetch_page(self.base_url)
            if not soup:
                return jobs
        
        # Seletores REAIS do JobArtis - containers são .panel.panel-default
        job_containers = soup.select('div.panel.panel-default')
        
        for job_elem in job_containers[:20]:  # Limitar a 20 vagas
            try:
                # Procurar link que contém 'emprego-' no href
                link_elem = None
                for a_tag in job_elem.find_all('a', href=True):
                    if 'emprego-' in a_tag.get('href', ''):
                        link_elem = a_tag
                        break
                
                if not link_elem:
                    continue
                
                job_url = link_elem.get('href', '')
                if not job_url.startswith('http'):
                    job_url = self.base_url.rstrip('/') + job_url
                
                # O texto do link geralmente contém: Cargo + Empresa + Localização
                full_text = self.clean_text(link_elem.get_text())
                
                # Tentar extrair título (geralmente é a primeira parte antes de "Empresa")
                title = full_text
                company = 'N/A'
                location = 'Angola'
                
                # Tentar encontrar padrões comuns
                # Formato típico: "CargoEmpresaNomeLocalizaçãoTipo..."
                if 'Empresa líder' in full_text:
                    parts = full_text.split('Empresa líder')
                    title = parts[0].strip()
                    if len(parts) > 1:
                        company = 'Empresa líder' + parts[1].split('.')[0]
                elif len(full_text) > 0:
                    # Usar primeiras palavras como título
                    words = full_text.split()
                    title = ' '.join(words[:5]) if len(words) > 5 else full_text
                
                # Procurar localização no texto
                for provincia in ['Luanda', 'Benguela', 'Huíla', 'Huambo', 'Cabinda', 'Namibe']:
                    if provincia in full_text:
                        location = provincia
                        break
                
                job = {
                    'title': title[:100],  # Limitar tamanho
                    'company': company,
                    'location': location,
                    'description': full_text[:200],  # Usar texto completo como descrição
                    'url': job_url,
                    'source': self.name,
                    'posted_date': None
                }
                
                # Classificar e enriquecer com informações de TI
                job = self.classify_and_enrich_job(job)
                
                # Validar que é uma vaga real de TI (não link de menu, etc)
                if len(title) > 3 and 'emprego-' in job_url and job.get('is_it_job'):
                    jobs.append(job)
                
            except Exception as e:
                print(f"Erro ao processar vaga no {self.name}: {e}")
                continue
        
        print(f"✓ {self.name}: {len(jobs)} vagas de TI encontradas")
        return jobs
