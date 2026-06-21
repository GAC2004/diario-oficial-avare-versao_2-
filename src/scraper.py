"""
scraper.py - Coleta edicoes do Diario Oficial de Avare.

Estrategia descoberta por inspecao do site:
  - listaatos.php lista todos os atos com links para edicoes
  - Cada edicao tem ID no formato: dosp.com.br/exibe_do.php?i=XXXXXXXX
  - O endpoint retorna o PDF diretamente (application/pdf)
  - Salvamos os PDFs localmente organizados por ano-mes
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "data" / "pdfs"

BASE_URL = "https://imprensaoficialmunicipal.com.br"
PDF_BASE = "https://www.dosp.com.br/exibe_do.php"

SECOES = [
    "Leis",
    "Decretos",
    "Portarias",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def get_edicoes(secao: str) -> list[dict]:
    """
    Scrapa a pagina de listagem de atos de uma secao
    e retorna lista de edicoes unicas com metadados.
    """
    url = f"{BASE_URL}/listaatos.php?c=Avar%C3%A9&s={secao}"
    print(f"\n  Buscando secao: {secao}")

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  ERRO ao acessar {url}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    edicoes = {}

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "exibe_do.php" not in href:
            continue

        match = re.search(r"[?&]i=([A-Za-z0-9+=/]+)", href)
        if not match:
            continue

        edicao_id = match.group(1)
        if edicao_id in edicoes:
            continue

        tr = a.find_parent("tr")
        data_str = ""
        if tr:
            tds = tr.find_all("td")
            if len(tds) >= 2:
                data_str = tds[1].get_text(strip=True)

        edicoes[edicao_id] = {
            "id": edicao_id,
            "url": f"{PDF_BASE}?i={edicao_id}",
            "data_raw": data_str,
            "secao": secao,
        }

    print(f"  -> {len(edicoes)} edicoes unicas encontradas.")
    return list(edicoes.values())


def parse_data(data_str: str) -> str:
    """
    Converte data DD/MM/AAAA para AAAA-MM.
    Retorna 'sem-data' se nao conseguir parsear.
    """
    try:
        dt = datetime.strptime(data_str.strip(), "%d/%m/%Y")
        return dt.strftime("%Y-%m")
    except ValueError:
        return "sem-data"


def download_pdf(edicao: dict) -> bool:
    """
    Baixa o PDF de uma edicao e salva em:
    C:\...\data\pdfs\AAAA-MM\edicao_ID.pdf
    """
    mes_dir = PDF_DIR / parse_data(edicao["data_raw"])
    mes_dir.mkdir(parents=True, exist_ok=True)

    filename = f"edicao_{edicao['id'].replace('/', '_').replace('=', '')}.pdf"
    save_path = mes_dir / filename

    if save_path.exists():
        return True  # Ja existe, pula

    try:
        resp = requests.get(
            edicao["url"],
            headers=HEADERS,
            timeout=60,
            stream=True,
        )
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "")
        if "pdf" not in content_type.lower() and len(resp.content) < 1000:
            print(f"  AVISO: resposta inesperada para {edicao['id']}")
            return False

        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        return True

    except requests.RequestException as e:
        print(f"  ERRO ao baixar {edicao['id']}: {e}")
        return False


def run_scraper(secoes: list[str] = None, limite: int = None):
    """
    Ponto de entrada principal.

    Args:
        secoes: Lista de secoes para coletar. None = todas.
        limite: Limita quantas edicoes baixar (util para testes).
    """
    if secoes is None:
        secoes = SECOES

    PDF_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n Salvando PDFs em: {PDF_DIR}\n")

    todas_edicoes = []
    for secao in secoes:
        edicoes = get_edicoes(secao)
        todas_edicoes.extend(edicoes)

    # Remove duplicatas globais
    vistas = set()
    edicoes_unicas = []
    for e in todas_edicoes:
        if e["id"] not in vistas:
            vistas.add(e["id"])
            edicoes_unicas.append(e)

    print(f"\n Total de edicoes unicas: {len(edicoes_unicas)}")

    if limite:
        edicoes_unicas = edicoes_unicas[:limite]
        print(f" Limitando a {limite} edicoes para este teste.")

    baixados = 0
    falhas = 0

    for edicao in tqdm(edicoes_unicas, desc="Baixando PDFs"):
        if download_pdf(edicao):
            baixados += 1
        else:
            falhas += 1
        time.sleep(0.1)

    print(f"\n Resultado: {baixados} baixados | {falhas} com falha")
    print(f" Pasta: {PDF_DIR}")


if __name__ == "__main__":
    run_scraper()