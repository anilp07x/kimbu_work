"""
Classificador de Vagas de TI
Identifica e categoriza vagas específicas para Engenharia Informática
"""

class ITJobClassifier:
    """Classifica vagas de emprego em categorias de TI"""
    
    # Palavras que DESQUALIFICAM uma vaga de ser TI (filtro negativo)
    NEGATIVE_KEYWORDS = [
        'professor', 'professora', 'docente', 'ensino', 'educação',
        'vendedor', 'vendedora', 'comercial', 'vendas',
        'motorista', 'condutor', 'transporte',
        'limpeza', 'cozinha', 'segurança física', 'vigilante',
        'construção civil', 'pedreiro', 'eletricista', 'canalizador',
        'agricultura', 'pecuária', 'agropecuária',
        'medicina', 'enfermeiro', 'médico', 'saúde',
        'direito', 'advogado', 'jurídico',
        'contabilidade', 'contador', 'financeiro', 'tesouraria',
        'recursos humanos', 'rh ', 'recrutamento',
        'marketing tradicional', 'publicidade',
        'gestão empresarial', 'administração empresarial',
        'logística', 'armazém', 'stock',
        'atendimento ao cliente', 'receção', 'secretária'
    ]
    
    # Categorias principais de TI - MUITO MAIS ESPECÍFICAS
    CATEGORIES = {
        'Programação': {
            'keywords': [
                'programador', 'developer', 'desenvolvedor', 'software engineer',
                'frontend developer', 'backend developer', 'full stack', 'fullstack',
                'web developer', 'mobile developer', 'app developer',
                'python developer', 'java developer', 'javascript developer',
                '.net developer', 'php developer', 'c++ developer', 'c# developer',
                'react developer', 'angular developer', 'vue developer',
                'node.js', 'django', 'flask', 'laravel', 'spring',
                'android developer', 'ios developer', 'swift', 'kotlin',
                'flutter developer', 'react native'
            ],
            'color': 'blue'
        },
        'Redes e Infraestrutura': {
            'keywords': [
                'network engineer', 'engenheiro de redes', 'administrador de redes',
                'técnico de redes', 'infraestrutura de ti', 'infrastructure engineer',
                'cisco', 'mikrotik', 'ccna', 'ccnp', 'ccent',
                'router', 'switch', 'firewall configuration',
                'vpn', 'wan', 'lan', 'tcp/ip', 'dns', 'dhcp',
                'network administrator', 'network technician'
            ],
            'color': 'green'
        },
        'IT Support': {
            'keywords': [
                'suporte técnico', 'technical support', 'it support',
                'help desk', 'helpdesk', 'service desk',
                'suporte de ti', 'suporte informático',
                'técnico de informática', 'técnico de ti', 'it technician',
                'desktop support', 'field technician',
                'assistência técnica informática',
                'troubleshooting de ti', 'manutenção de computadores'
            ],
            'color': 'yellow'
        },
        'Segurança da Informação': {
            'keywords': [
                'segurança da informação', 'information security', 'cybersecurity',
                'cibersegurança', 'security analyst', 'analista de segurança',
                'pentester', 'penetration tester', 'ethical hacker',
                'security engineer', 'engenheiro de segurança',
                'soc analyst', 'security operations',
                'iso 27001', 'iso 27002', 'compliance de ti',
                'vulnerability assessment', 'threat analysis'
            ],
            'color': 'red'
        },
        'Data Science & BI': {
            'keywords': [
                'data scientist', 'cientista de dados',
                'data analyst', 'analista de dados',
                'data engineer', 'engenheiro de dados',
                'business intelligence', 'bi analyst', 'analista bi',
                'power bi', 'tableau', 'qlik',
                'big data', 'data mining',
                'machine learning engineer', 'ml engineer',
                'artificial intelligence', 'ai engineer',
                'data warehouse', 'etl developer',
                'database administrator', 'dba'
            ],
            'color': 'purple'
        },
        'DevOps & Cloud': {
            'keywords': [
                'devops engineer', 'engenheiro devops',
                'cloud engineer', 'cloud architect', 'arquiteto cloud',
                'aws engineer', 'azure engineer', 'gcp engineer',
                'docker', 'kubernetes', 'container',
                'jenkins', 'ci/cd', 'pipeline',
                'terraform', 'ansible', 'chef', 'puppet',
                'gitlab', 'github actions', 'bitbucket',
                'sre', 'site reliability engineer',
                'infrastructure as code', 'iac'
            ],
            'color': 'indigo'
        },
        'Gestão de TI': {
            'keywords': [
                'gestor de ti', 'it manager', 'gerente de ti',
                'diretor de ti', 'cto', 'cio',
                'project manager ti', 'project manager it',
                'scrum master', 'product owner', 'agile coach',
                'tech lead', 'technical lead', 'líder técnico',
                'coordenador de ti', 'coordenador it',
                'service manager it', 'it service manager',
                'itil', 'cobit', 'pmp'
            ],
            'color': 'gray'
        },
        'Sistemas e Administração': {
            'keywords': [
                'system administrator', 'sysadmin', 'administrador de sistemas',
                'linux administrator', 'windows server administrator',
                'unix administrator', 'administrador unix',
                'active directory', 'ad administrator',
                'exchange administrator', 'office 365 administrator',
                'vmware', 'hyper-v', 'virtualização', 'virtualization',
                'backup administrator', 'storage administrator'
            ],
            'color': 'teal'
        }
    }
    
    # Níveis de experiência
    EXPERIENCE_LEVELS = {
        'Júnior': ['junior', 'júnior', 'trainee', 'estagiário', 'entry level', 'graduate'],
        'Pleno': ['pleno', 'mid level', 'mid-level', 'intermediate', 'semi-senior', 'semi-sénior'],
        'Sénior': ['senior', 'sénior', 'sr', 'lead', 'principal', 'expert', 'architect']
    }
    
    @classmethod
    def is_it_job(cls, title: str, description: str = '') -> bool:
        """
        Verifica se uma vaga é relacionada com TI - VERSÃO RESTRITIVA
        
        Args:
            title: Título da vaga
            description: Descrição da vaga (opcional)
            
        Returns:
            True se for vaga de TI, False caso contrário
        """
        text = f"{title} {description}".lower()
        
        # PRIMEIRO: Verificar palavras negativas (descarta a vaga)
        for negative in cls.NEGATIVE_KEYWORDS:
            if negative in text:
                return False
        
        # SEGUNDO: Deve ter pelo menos UMA palavra-chave específica de TI
        it_match_found = False
        for category_data in cls.CATEGORIES.values():
            for keyword in category_data['keywords']:
                if keyword.lower() in text:
                    it_match_found = True
                    break
            if it_match_found:
                break
        
        # Se encontrou match específico, é vaga de TI
        if it_match_found:
            return True
        
        # Palavras genéricas de TI - APENAS se o título for muito específico
        title_lower = title.lower()
        specific_it_titles = [
            'ti', 'it ', 'informática', 'tecnologia da informação',
            'engenheiro de software', 'técnico de informática'
        ]
        
        for keyword in specific_it_titles:
            if keyword in title_lower:
                return True
                
        return False
    
    @classmethod
    def classify_job(cls, title: str, description: str = '') -> list:
        """
        Classifica uma vaga em uma ou mais categorias de TI
        
        Args:
            title: Título da vaga
            description: Descrição da vaga (opcional)
            
        Returns:
            Lista de categorias identificadas
        """
        text = f"{title} {description}".lower()
        categories = []
        
        for category, data in cls.CATEGORIES.items():
            for keyword in data['keywords']:
                if keyword.lower() in text:
                    if category not in categories:
                        categories.append(category)
                    break
        
        # Se não encontrar categoria específica mas for vaga de TI
        if not categories and cls.is_it_job(title, description):
            categories.append('TI - Geral')
            
        return categories
    
    @classmethod
    def detect_experience_level(cls, title: str, description: str = '') -> str:
        """
        Detecta o nível de experiência da vaga
        
        Args:
            title: Título da vaga
            description: Descrição da vaga (opcional)
            
        Returns:
            Nível de experiência ('Júnior', 'Pleno', 'Sénior', ou 'Não especificado')
        """
        text = f"{title} {description}".lower()
        
        for level, keywords in cls.EXPERIENCE_LEVELS.items():
            for keyword in keywords:
                if keyword in text:
                    return level
        
        return 'Não especificado'
    
    @classmethod
    def extract_technologies(cls, title: str, description: str = '') -> list:
        """
        Extrai tecnologias mencionadas na vaga
        
        Args:
            title: Título da vaga
            description: Descrição da vaga (opcional)
            
        Returns:
            Lista de tecnologias identificadas
        """
        text = f"{title} {description}".lower()
        technologies = []
        
        # Lista de tecnologias comuns
        tech_list = [
            'Python', 'Java', 'JavaScript', 'PHP', 'C++', 'C#', '.NET',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask',
            'Laravel', 'Spring', 'Flutter', 'React Native',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'Redis',
            'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes',
            'Linux', 'Windows Server', 'Ubuntu', 'CentOS',
            'Cisco', 'Mikrotik', 'Fortinet', 'Palo Alto',
            'Git', 'GitHub', 'GitLab', 'Jenkins', 'Terraform',
            'Power BI', 'Tableau', 'Excel', 'SAP', 'Salesforce'
        ]
        
        for tech in tech_list:
            if tech.lower() in text:
                technologies.append(tech)
        
        return technologies
    
    @classmethod
    def get_category_color(cls, category: str) -> str:
        """
        Retorna a cor associada a uma categoria
        
        Args:
            category: Nome da categoria
            
        Returns:
            Nome da cor (para uso em CSS/Tailwind)
        """
        if category in cls.CATEGORIES:
            return cls.CATEGORIES[category]['color']
        return 'gray'
    
    @classmethod
    def get_all_categories(cls) -> list:
        """Retorna lista de todas as categorias disponíveis"""
        return list(cls.CATEGORIES.keys()) + ['TI - Geral']
