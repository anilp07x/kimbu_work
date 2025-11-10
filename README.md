# KimbuWork

**Plataforma Flask minimalista para monitorar vagas de emprego em Angola.**

<img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
<img src="https://img.shields.io/badge/Flask-3.0-green.svg" alt="Flask">
<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">

## 🚀 Funcionalidades

- ✅ **Web Scraping Automático**: Coleta vagas de AngoEmprego e JobArtis
- ✅ **Interface Responsiva**: Design minimalista com Tailwind CSS
- ✅ **Base de Dados SQLite**: Armazenamento leve e eficiente
- ✅ **Atualização Automática**: APScheduler para scraping periódico
- ✅ **API REST**: Endpoints para integração
- ✅ **Filtros por Fonte**: Organize vagas por portal
- ✅ **Indicador de Novas Vagas**: Veja rapidamente o que há de novo

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

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
cp .env.example .env
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
