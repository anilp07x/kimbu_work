# KimbuWork 💼

**Plataforma especializada em Vagas de TI para Engenheiros Informáticos em Angola**

<img src="https://img.shields.io/badge/Python-3.13+-blue.svg" alt="Python">
<img src="https://img.shields.io/badge/Flask-3.0-green.svg" alt="Flask">
<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">

## 🎯 Sobre o Projeto

O KimbuWork é uma plataforma automatizada que agrega **exclusivamente vagas de Tecnologia da Informação** de múltiplos portais de emprego em Angola. Com classificação inteligente por categorias, níveis de experiência e tecnologias, facilita a busca de oportunidades para profissionais de TI.

## 🚀 Funcionalidades

### Core Features
- ✅ **Filtragem Inteligente de Vagas de TI**: Sistema de classificação automática usando palavras-chave específicas de tecnologia
- ✅ **Categorização Avançada**: 8 categorias especializadas (Programação, Redes, IT Support, Segurança, Data Science, DevOps, Cloud, Gestão TI)
- ✅ **Detecção de Nível de Experiência**: Identifica automaticamente vagas Júnior, Pleno e Sénior
- ✅ **Extração de Tecnologias**: Detecta linguagens, frameworks e ferramentas mencionadas nas vagas
- ✅ **Web Scraping Automático**: Coleta vagas de AngoEmprego e JobArtis a cada 6 horas
- ✅ **Interface Responsiva**: Design moderno focado em UX para profissionais de TI
- ✅ **Base de Dados SQLite**: Armazenamento eficiente com índices otimizados
- ✅ **API REST Completa**: Endpoints para filtros avançados (categoria, nível, tecnologia, portal)
- ✅ **Dashboard com Estatísticas**: Breakdown visual por categoria e nível de experiência

### Categorias Suportadas
1. 💻 **Programação** - Frontend, Backend, Full-stack, Mobile (Python, Java, JavaScript, PHP, C++, etc.)
2. 🌐 **Redes e Infraestrutura** - Cisco, Mikrotik, CCNA, CCNP, TCP/IP
3. 🛠️ **IT Support** - Help Desk, Service Desk, Technical Support
4. 🔒 **Segurança da Informação** - Cybersecurity, Pentesting, SOC, ISO 27001
5. 📊 **Data Science & BI** - Análise de Dados, Power BI, SQL, Machine Learning
6. ☁️ **DevOps & Cloud** - AWS, Azure, Docker, Kubernetes, CI/CD
7. 👔 **Gestão de TI** - Project Manager, Scrum Master, CTO, CIO
8. ⚙️ **Sistemas e Administração** - Linux, Windows Server, VMware, Virtualization

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (para clonar o repositório)

## 🔧 Instalação

1. **Clone o repositório**
```powershell
git clone https://github.com/anilp07x/kimbu_work.git
cd kimbu_work
```

2. **Crie e ative o ambiente virtual**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Instale as dependências**
```powershell
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```powershell
Copy-Item .env.example .env
# Edite o arquivo .env conforme necessário
```

## ▶️ Como Usar

### Executar a aplicação

```powershell
python run.py
```

Acesse: **http://localhost:5000**

### Forçar scraping manual

Clique no botão "Atualizar Agora" na interface ou use a API:

```powershell
curl -X POST http://localhost:5000/api/scrape
```

## 📁 Estrutura do Projeto

```
kimbu_work/
├── app.py                  # Aplicação Flask principal
├── run.py                  # Script de inicialização
├── config.py               # Configurações
├── database.py             # Gerenciamento SQLite
├── scraper_manager.py      # Orquestração de scrapers
├── scrapers/               # Módulos de scraping
│   ├── __init__.py
│   ├── base_scraper.py     # Classe base
│   ├── angoemprego_scraper.py
│   └── jobartis_scraper.py
├── templates/              # Templates HTML
│   └── index.html
├── requirements.txt        # Dependências Python
├── .env.example           # Exemplo de variáveis de ambiente
└── README.md
```

## 🛠️ Configuração de Scrapers

Os scrapers em `scrapers/` são **templates genéricos**. Você precisa ajustar os seletores CSS de acordo com a estrutura real dos sites:

1. Inspecione o site alvo (F12 no navegador)
2. Identifique os seletores CSS corretos
3. Atualize os seletores em `angoemprego_scraper.py` e `jobartis_scraper.py`

**Exemplo:**
```python
# Antes (template)
job_listings = soup.select('.job-listing')

# Depois (ajustado)
job_listings = soup.select('div.vacancy-card')
```

## 🌐 API Endpoints

### GET `/api/jobs`
Lista vagas
- **Parâmetros**: `limit` (int), `source` (string)
- **Resposta**: JSON com lista de vagas

### GET `/api/stats`
Estatísticas das vagas
- **Resposta**: JSON com total, novas vagas e distribuição por fonte

### POST `/api/scrape`
Força scraping manual
- **Resposta**: JSON com resultado da operação

## ⚙️ Configurações

Edite `.env` para personalizar:

- `SCRAPING_INTERVAL_HOURS`: Intervalo de atualização automática (padrão: 6h)
- `ENABLE_EMAIL_NOTIFICATIONS`: Ativar notificações por email
- `ENABLE_TELEGRAM_NOTIFICATIONS`: Ativar notificações pelo Telegram

## 📊 Tecnologias

- **Backend**: Flask 3.0
- **Scraping**: BeautifulSoup4, Requests
- **Database**: SQLite3
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Agendamento**: APScheduler
- **Tipografia**: Google Fonts (Inter)

## 🎨 Design

Interface minimalista com:
- Paleta neutra (branco, cinza, azul suave)
- Tipografia leve (Inter)
- Responsivo (mobile-first)
- Transições suaves

## 📝 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Anilson Da Silva Pedro**
- GitHub: [@anilp07x](https://github.com/anilp07x)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## ⚠️ Aviso Legal

Este projeto é para fins educacionais. Respeite os termos de serviço dos sites que você faz scraping e implemente delays apropriados para não sobrecarregar os servidores.

## 📞 Suporte

Encontrou um bug? Tem uma sugestão? Abra uma [issue](https://github.com/anilp07x/kimbu_work/issues)!

---

Feito com ❤️ em Angola 🇦🇴
