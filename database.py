"""
Gerenciamento da base de dados SQLite
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from config import Config


class Database:
    """Classe para gerenciar a base de dados SQLite"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.init_db()
    
    def get_connection(self):
        """Obtém conexão com a base de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Inicializa as tabelas da base de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de vagas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                description TEXT,
                url TEXT UNIQUE NOT NULL,
                source TEXT NOT NULL,
                posted_date TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_new BOOLEAN DEFAULT 1,
                categories TEXT,
                experience_level TEXT,
                technologies TEXT,
                is_it_job BOOLEAN DEFAULT 0
            )
        ''')
        
        # Índices para melhor performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON jobs(source)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_posted_date ON jobs(posted_date DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_is_new ON jobs(is_new)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_is_it_job ON jobs(is_it_job)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_experience_level ON jobs(experience_level)')
        
        conn.commit()
        conn.close()
    
    def add_job(self, job_data: Dict) -> bool:
        """
        Adiciona uma nova vaga à base de dados
        Returns: True se foi adicionada, False se já existia
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Converte listas para strings JSON se existirem
            categories = ','.join(job_data.get('categories', []))
            technologies = ','.join(job_data.get('technologies', []))
            
            cursor.execute('''
                INSERT INTO jobs (
                    title, company, location, description, url, source, posted_date,
                    categories, experience_level, technologies, is_it_job
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_data.get('title'),
                job_data.get('company'),
                job_data.get('location'),
                job_data.get('description'),
                job_data.get('url'),
                job_data.get('source'),
                job_data.get('posted_date'),
                categories,
                job_data.get('experience_level'),
                technologies,
                job_data.get('is_it_job', 0)
            ))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # URL já existe
            conn.close()
            return False
    
    def get_jobs(self, limit: int = 50, source: str = None, only_new: bool = False, 
                 category: str = None, experience_level: str = None, 
                 only_it: bool = True) -> List[Dict]:
        """Obtém lista de vagas com filtros avançados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM jobs WHERE 1=1'
        params = []
        
        if only_it:
            query += ' AND is_it_job = 1'
        
        if source:
            query += ' AND source = ?'
            params.append(source)
        
        if category:
            query += ' AND categories LIKE ?'
            params.append(f'%{category}%')
        
        if experience_level:
            query += ' AND experience_level = ?'
            params.append(experience_level)
        
        if only_new:
            query += ' AND is_new = 1'
        
        query += ' ORDER BY scraped_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        jobs = []
        for row in cursor.fetchall():
            job = dict(row)
            # Converte strings separadas por vírgula de volta para listas
            if job.get('categories'):
                job['categories'] = job['categories'].split(',')
            else:
                job['categories'] = []
            
            if job.get('technologies'):
                job['technologies'] = job['technologies'].split(',')
            else:
                job['technologies'] = []
            
            jobs.append(job)
        
        conn.close()
        return jobs
    
    def mark_jobs_as_seen(self):
        """Marca todas as vagas como vistas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE jobs SET is_new = 0 WHERE is_new = 1')
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """Obtém estatísticas das vagas com breakdown por categorias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM jobs WHERE is_it_job = 1')
        total = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as new FROM jobs WHERE is_new = 1 AND is_it_job = 1')
        new = cursor.fetchone()['new']
        
        cursor.execute('''
            SELECT source, COUNT(*) as count 
            FROM jobs 
            WHERE is_it_job = 1
            GROUP BY source
        ''')
        by_source = {row['source']: row['count'] for row in cursor.fetchall()}
        
        # Estatísticas por categoria
        cursor.execute('SELECT categories FROM jobs WHERE is_it_job = 1 AND categories IS NOT NULL AND categories != ""')
        all_categories = {}
        for row in cursor.fetchall():
            cats = row['categories'].split(',')
            for cat in cats:
                cat = cat.strip()
                if cat:
                    all_categories[cat] = all_categories.get(cat, 0) + 1
        
        # Estatísticas por nível de experiência
        cursor.execute('''
            SELECT experience_level, COUNT(*) as count 
            FROM jobs 
            WHERE is_it_job = 1 AND experience_level IS NOT NULL AND experience_level != ""
            GROUP BY experience_level
        ''')
        by_level = {row['experience_level']: row['count'] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total': total,
            'new': new,
            'by_source': by_source,
            'by_category': all_categories,
            'by_level': by_level
        }
