# 🚀 Guia Rápido - KimbuWork

## Início Rápido (5 minutos)

### 1. Ativar ambiente virtual
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Criar arquivo de configuração
```powershell
Copy-Item .env.example .env
```

### 3. Executar aplicação
```powershell
python run.py
```

### 4. Acessar no navegador
Abra: **http://localhost:5000**

---

## ⚙️ Próximos Passos

### Ajustar Scrapers
Os scrapers não funcionarão corretamente até você ajustar os seletores CSS:

1. Abra o site no navegador (ex: https://angoemprego.com)
2. Pressione F12 (Developer Tools)
3. Inspecione elementos de vagas
4. Identifique classes CSS corretas
5. Atualize em `scrapers/angoemprego_scraper.py`:

```python
# Exemplo - ANTES (não funciona)
job_listings = soup.select('.job-listing')

# DEPOIS (com seletor correto)
job_listings = soup.select('div.vacancy-item')  # Ajuste conforme necessário
```

### Personalizar Configurações
Edite `.env`:

```ini
# Intervalo de atualização automática (em horas)
SCRAPING_INTERVAL_HOURS=6

# Chave secreta do Flask (mude em produção)
SECRET_KEY=sua-chave-secreta-aqui
```

---

## 📚 Comandos Úteis

### Ver logs do scraping
```powershell
python run.py
# Observe as mensagens no terminal
```

### Forçar atualização manual
- Clique em "Atualizar Agora" na interface web
- OU use curl:
```powershell
curl -X POST http://localhost:5000/api/scrape
```

### Listar vagas via API
```powershell
# Todas as vagas
curl http://localhost:5000/api/jobs

# Limitar a 10 vagas
curl http://localhost:5000/api/jobs?limit=10

# Filtrar por fonte
curl http://localhost:5000/api/jobs?source=AngoEmprego
```

### Ver estatísticas
```powershell
curl http://localhost:5000/api/stats
```

---

## 🐛 Solução de Problemas

### "No module named 'scrapers'"
Execute de dentro da pasta do projeto:
```powershell
cd c:\Users\anilp\Documents\kimbu_work
python run.py
```

### Scrapers não encontram vagas
1. Verifique se os sites estão acessíveis
2. Ajuste os seletores CSS (veja "Ajustar Scrapers" acima)
3. Verifique logs no terminal para erros

### Base de dados corrompida
Delete e recrie:
```powershell
Remove-Item jobs.db
python run.py  # Recria automaticamente
```

---

## 📖 Estrutura de Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | Aplicação Flask principal |
| `run.py` | Script de inicialização |
| `config.py` | Configurações do .env |
| `database.py` | Gerenciamento SQLite |
| `scraper_manager.py` | Orquestrador de scrapers |
| `scrapers/base_scraper.py` | Classe base para scrapers |
| `templates/index.html` | Interface web |
| `.env` | Variáveis de ambiente |
| `jobs.db` | Base de dados SQLite |

---

## 🎯 Checklist de Primeira Execução

- [ ] Ambiente virtual ativado
- [ ] Arquivo `.env` criado
- [ ] Dependências instaladas (`requirements.txt`)
- [ ] Aplicação rodando (`python run.py`)
- [ ] Interface acessível em http://localhost:5000
- [ ] Seletores CSS ajustados nos scrapers
- [ ] Primeira atualização manual executada
- [ ] Vagas aparecendo na interface

---

**Pronto! KimbuWork está funcionando! 🎉**

Para mais informações, consulte o [README.md](README.md) completo.
