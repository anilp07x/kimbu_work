"""
Aplicação Flask principal do KimbuWork
Plataforma especializada em Vagas de TI para Engenheiros Informáticos em Angola
"""
from flask import Flask, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit

from config import Config
from scraper_manager import ScraperManager
from database import Database
from it_classifier import ITJobClassifier

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar gerenciadores
scraper_manager = ScraperManager()
db = Database()

# Configurar agendamento automático
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=scraper_manager.run_all_scrapers,
    trigger="interval",
    hours=Config.SCRAPING_INTERVAL_HOURS,
    id='scrape_jobs',
    name='Scrape job listings',
    replace_existing=True
)
scheduler.start()

# Garantir que o scheduler para ao encerrar
atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def index():
    """Página principal"""
    stats = scraper_manager.get_stats()
    jobs = scraper_manager.get_jobs(limit=20)
    
    return render_template(
        'index.html',
        stats=stats,
        jobs=jobs,
        last_update=datetime.now().strftime('%d/%m/%Y %H:%M')
    )


@app.route('/api/jobs')
def api_jobs():
    """API endpoint para listar vagas com filtros avançados"""
    limit = request.args.get('limit', 50, type=int)
    source = request.args.get('source', None)
    category = request.args.get('category', None)
    experience_level = request.args.get('level', None)
    only_new = request.args.get('only_new', False, type=bool)
    
    jobs = db.get_jobs(
        limit=limit, 
        source=source, 
        category=category,
        experience_level=experience_level,
        only_new=only_new,
        only_it=True
    )
    return jsonify(jobs)


@app.route('/api/categories')
def api_categories():
    """API endpoint para listar todas as categorias"""
    from it_classifier import ITJobClassifier
    categories = ITJobClassifier.get_all_categories()
    return jsonify({'categories': categories})


@app.route('/api/stats')
def api_stats():
    """API endpoint para estatísticas detalhadas"""
    stats = scraper_manager.get_stats()
    return jsonify(stats)


@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    """API endpoint para forçar scraping manual"""
    try:
        stats = scraper_manager.run_all_scrapers()
        return jsonify({
            'success': True,
            'message': f'{stats["total_new"]} novas vagas adicionadas',
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/mark-seen', methods=['POST'])
def api_mark_seen():
    """Marcar todas as vagas como vistas"""
    db.mark_jobs_as_seen()
    return jsonify({'success': True})


@app.template_filter('timeago')
def timeago_filter(date_str):
    """Filtro para mostrar tempo relativo"""
    if not date_str:
        return 'Recente'
    # Implementar lógica de tempo relativo se necessário
    return date_str


if __name__ == '__main__':
    # Executar scraping inicial
    print("🚀 Iniciando KimbuWork...")
    scraper_manager.run_all_scrapers()
    
    # Iniciar servidor Flask
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
