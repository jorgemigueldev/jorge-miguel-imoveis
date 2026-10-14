# Jorge Miguel Imóveis — Site com atualização automática

Site catálogo de imóveis do Litoral Norte SC, com sincronização automática a partir do site Tolentino Imóveis.

## Estrutura

- `index.html` — página principal
- `style.css` — estilos
- `script.js` — lógica do front-end (carrega `properties.json`)
- `properties.json` — base de dados dos imóveis (atualizada pelo scraper)
- `scraper.py` — script que busca todos os imóveis atuais do site Tolentino
- `server.py` — servidor Flask (opcional, para rodar localmente com endpoint de sync)

## Como usar

### 1. Apenas estático (hospedagem simples)
Coloque a pasta em Netlify, Vercel, GitHub Pages ou qualquer host estático.
O site carrega os imóveis de `properties.json`.

### 2. Com atualização automática (recomendado)

#### Pré-requisitos
```bash
pip install flask playwright
playwright install chromium
```

#### Rodar o servidor
```bash
python server.py
```
Acesse http://localhost:5000

#### Sincronizar imóveis
- Manualmente: acesse http://localhost:5000/sync
- Ou rode direto: `python scraper.py`

#### Atualização periódica (cron)
Adicione no crontab para rodar a cada 6 horas, por exemplo:
```bash
0 */6 * * * cd /caminho/para/jorge-miguel-imoveis && python3 scraper.py
```

#### Deploy com sync automático
Opções:
1. **VPS / servidor próprio**: rode `server.py` + cron com `scraper.py`
2. **GitHub Actions**: crie um workflow que rode o scraper e faça commit do `properties.json` atualizado (depois o site estático pega a nova versão)
3. **Serverless** (Vercel/Netlify functions): adapte o scraper para uma function

## Notas
- Os detalhes completos e todas as fotos continuam no site original (links nos cards).
- O scraper extrai título, tipo, preço, localização, código e foto principal.
- CRECI 71144 SC · @jorgemiguelimoveis
- "Seu próximo capítulo começa perto do mar."

## Ajustes rápidos
- Número do WhatsApp: edite em `index.html`
- Cores/fontes: `style.css`
- Intervalo de sync: ajuste o cron ou o endpoint `/sync`
