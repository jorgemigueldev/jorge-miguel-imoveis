#!/usr/bin/env python3
"""
Scraper para atualizar automaticamente os imóveis do site Tolentino
para o catálogo da Jorge Miguel Imóveis.

Requisitos: pip install playwright && playwright install chromium
Uso: python scraper.py
"""

import asyncio
import json
import re
from playwright.async_api import async_playwright

OUTPUT_FILE = "properties.json"
BASE_URL = "https://tolentinoimoveissc.com.br/busca"


async def scrape():
    properties = []
    seen = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(BASE_URL, wait_until="networkidle")
        await page.wait_for_timeout(3000)

        # Coletar de todas as páginas (assumindo até 10 páginas)
        for page_num in range(1, 11):
            if page_num > 1:
                # Clicar no botão da página
                try:
                    btn = page.locator(f'button:text-is("{page_num}")')
                    if await btn.count() == 0:
                        break
                    await btn.click()
                    await page.wait_for_timeout(2500)
                except Exception:
                    break

            # Extrair cards
            cards = await page.evaluate("""
                () => Array.from(document.querySelectorAll('a[href*="/imovel/"]')).map(a => {
                    const img = a.querySelector('img');
                    return {
                        href: a.href,
                        text: a.innerText.replace(/\\s+/g, ' ').trim(),
                        img: img ? img.src : null
                    };
                })
            """)

            for card in cards:
                if card["href"] in seen:
                    continue
                seen.add(card["href"])

                text = card["text"]
                # Extrair tipo
                mtype = re.search(r'Comparar (Casa|Apartamento|Terreno|Empreendimento|Sobrado|Galpão|Casa Comercial)', text, re.I)
                tipo = mtype.group(1) if mtype else "Imóvel"

                # Preço
                price_m = re.search(r'R\$\s*[\d\.]+,\d{2}', text)
                preco = price_m.group(0) if price_m else "Sob consulta"

                # Local
                loc_m = re.search(r'([A-ZÁÉÍÓÚa-záéíóú\s]+),\s*([A-ZÁÉÍÓÚa-záéíóú\s]+)\s*-\s*SC', text)
                local = loc_m.group(0).strip() if loc_m else ""

                # Título
                after = text.split("Comparar", 1)[-1]
                after = re.sub(r'^(Casa|Apartamento|Terreno|Empreendimento|Sobrado|Galpão|Casa Comercial)\s*', '', after, flags=re.I)
                title_end = len(after)
                for marker in [local, preco]:
                    if marker and marker in after:
                        title_end = min(title_end, after.find(marker))
                titulo = after[:title_end].strip(" |,-")
                titulo = re.sub(r'\s+', ' ', titulo)[:140]
                for prefix in ["Casa ", "Apartamento ", "Terreno ", "Empreendimento "]:
                    if titulo.startswith(prefix):
                        titulo = titulo[len(prefix):]
                titulo = titulo.strip(" |,-") or f"{tipo} no Litoral Norte"

                codigo_m = re.search(r'Cód:\s*(\w+)', text)
                codigo = codigo_m.group(1) if codigo_m else ""

                properties.append({
                    "href": card["href"],
                    "titulo": titulo,
                    "tipo": tipo,
                    "preco": preco,
                    "local": local,
                    "img": card["img"],
                    "codigo": codigo
                })

            print(f"Página {page_num}: total acumulado {len(properties)}")

        await browser.close()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(properties, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Atualizado: {len(properties)} imóveis salvos em {OUTPUT_FILE}")
    return properties


if __name__ == "__main__":
    asyncio.run(scrape())
