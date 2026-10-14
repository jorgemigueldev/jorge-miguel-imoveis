#!/usr/bin/env python3
"""
Servidor para o site Jorge Miguel Imóveis.
Serve os arquivos estáticos e permite atualização automática dos imóveis.

Uso:
  pip install flask
  python server.py

Acesse: http://localhost:5000
Para sincronizar manualmente: http://localhost:5000/sync
"""

from flask import Flask, send_from_directory, jsonify
import subprocess
import os
import threading

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/sync')
def sync():
    """Dispara a sincronização dos imóveis em background."""
    def run_scraper():
        try:
            result = subprocess.run(
                ["python3", "scraper.py"],
                capture_output=True,
                text=True,
                timeout=300
            )
            print("Scraper output:", result.stdout)
            if result.stderr:
                print("Scraper errors:", result.stderr)
        except Exception as e:
            print("Erro ao rodar scraper:", e)

    thread = threading.Thread(target=run_scraper, daemon=True)
    thread.start()
    return jsonify({
        "status": "sincronizacao_iniciada",
        "message": "A atualização dos imóveis foi iniciada em segundo plano. Recarregue a página em alguns minutos."
    })

@app.route('/api/properties')
def api_properties():
    """Endpoint alternativo que retorna o JSON atual."""
    try:
        with open("properties.json", "r", encoding="utf-8") as f:
            data = f.read()
        return data, 200, {"Content-Type": "application/json; charset=utf-8"}
    except FileNotFoundError:
        return jsonify({"error": "properties.json não encontrado"}), 404

if __name__ == "__main__":
    print("🚀 Servidor Jorge Miguel Imóveis rodando em http://localhost:5000")
    print("   Para sincronizar imóveis: http://localhost:5000/sync")
    app.run(host="0.0.0.0", port=5000, debug=True)
