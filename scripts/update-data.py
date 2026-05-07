#!/usr/bin/env python3
"""
Actualiza data.json para Astara Growth Radar usando fuentes públicas.
No necesita API keys. Corre bien en GitHub Actions.
"""
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data.json"
PERU_TZ = timezone(timedelta(hours=-5))

SEARCHES = [
    "mercado automotriz Peru AAP",
    "vehiculos electrificados Peru AAP SUNARP",
    "Astara Peru Kia Chery MG Mitsubishi GAC",
    "Toyota Peru hibridos lanzamiento",
    "Jetour Peru SUV",
    "BAIC Magna Peru",
    "GWM Haval Changan Geely Peru automotriz"
]

DEFAULT_SOURCES = [
    { "name": "Astara corporativo", "url": "https://astara.com/es" },
    { "name": "Astara Retail Perú", "url": "https://www.astararetail.pe/" },
    { "name": "AAP Perú", "url": "https://aap.org.pe/" }
]


def fetch_url(url: str, timeout: int = 20) -> bytes:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 AstaraGrowthRadar/1.0"})
    with urlopen(req, timeout=timeout) as response:
        return response.read()


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    text = text.replace("&amp;", "&").replace("&#39;", "'").replace("&quot;", '"')
    return re.sub(r"\s+", " ", text).strip()


def google_news(query: str, limit: int = 3):
    url = f"https://news.google.com/rss/search?q={quote(query)}&hl=es-419&gl=PE&ceid=PE:es-419"
    try:
        xml_bytes = fetch_url(url)
        root = ET.fromstring(xml_bytes)
        items = []
        for item in root.findall(".//item")[:limit]:
            title = strip_html(item.findtext("title", ""))
            link = item.findtext("link", "#")
            pub_date = item.findtext("pubDate", "Reciente")
            source = item.findtext("source", "Google News")
            if title:
                items.append({
                    "title": title,
                    "url": link,
                    "source": source,
                    "date": pub_date
                })
        return items
    except Exception as exc:
        print(f"No se pudo leer Google News para {query}: {exc}", file=sys.stderr)
        return []


def dedupe_news(items, max_items=8):
    seen = set()
    result = []
    for item in items:
        key = re.sub(r"\W+", "", item.get("title", "").lower())[:80]
        if key and key not in seen:
            seen.add(key)
            result.append(item)
        if len(result) >= max_items:
            break
    return result


def build_competition_bullets(news):
    text = " ".join(n.get("title", "") for n in news).lower()
    bullets = []
    if "toyota" in text or "híbr" in text or "hibr" in text:
        bullets.append("Toyota: liderazgo y conversación activa en híbridos.")
    else:
        bullets.append("Toyota: referente de confianza e híbridos; monitoreo permanente.")

    if "jetour" in text:
        bullets.append("Jetour: señales activas en SUVs, aventura y expansión comercial.")
    else:
        bullets.append("Jetour: crecimiento acelerado en SUVs y presencia regional.")

    if "baic" in text or "magna" in text:
        bullets.append("BAIC/Magna: nuevo movimiento competitivo en SUV y off-road.")
    else:
        bullets.append("BAIC: nuevo entrante con foco en SUV y off-road.")
    return bullets


def main():
    if DATA_PATH.exists():
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    else:
        data = {}

    all_news = []
    for query in SEARCHES:
        all_news.extend(google_news(query, limit=2))

    news = dedupe_news(all_news, max_items=8)
    now = datetime.now(PERU_TZ)
    data["lastUpdated"] = now.strftime("%d/%m/%Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.")
    data["news"] = news
    data["competitionBullets"] = build_competition_bullets(news)
    data["sources"] = DEFAULT_SOURCES + [
        {"name": "Google News: mercado automotriz Perú", "url": "https://news.google.com/search?q=mercado%20automotriz%20Peru"}
    ]

    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Actualizado {DATA_PATH} con {len(news)} noticias.")


if __name__ == "__main__":
    main()
