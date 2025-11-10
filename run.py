"""
Script de inicialização do KimbuWork
"""
import os
import sys

def main():
    """Inicializa a aplicação"""
    
    # Verificar se .env existe
    if not os.path.exists('.env'):
        print("⚠️  Arquivo .env não encontrado!")
        print("📝 Criando .env a partir de .env.example...")
        
        if os.path.exists('.env.example'):
            with open('.env.example', 'r', encoding='utf-8') as example:
                with open('.env', 'w', encoding='utf-8') as env:
                    env.write(example.read())
            print("✅ Arquivo .env criado com sucesso!")
        else:
            print("❌ .env.example não encontrado. Por favor, configure manualmente.")
            sys.exit(1)
    
    # Importar e executar aplicação
    from app import app, scraper_manager
    
    print("\n" + "="*50)
    print("🚀 KimbuWork - Vagas de Emprego em Angola")
    print("="*50 + "\n")
    
    # Executar scraping inicial
    print("🔍 Executando scraping inicial...")
    scraper_manager.run_all_scrapers()
    
    print("\n" + "="*50)
    print("✅ Servidor iniciado!")
    print("🌐 Acesse: http://localhost:5000")
    print("="*50 + "\n")
    
    # Iniciar servidor Flask
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
