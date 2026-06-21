"""
extractor.py - Extrai texto dos PDFs e salva como JSON estruturado.

Cada PDF gera um JSON em data/processed/ com:
{
  "source": "nome_do_arquivo.pdf",
  "date": "2026-05",
  "pages": [{"page": 1, "text": "..."}],
  "full_text": "texto completo concatenado"
}
"""

import json
import pdfplumber
from pathlib import Path
from tqdm import tqdm


BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = BASE_DIR / "data" / "pdfs"
OUTPUT_DIR = BASE_DIR / "data" / "processed"


def extract_text_from_pdf(pdf_path: Path) -> dict:
    """
    Extrai texto de todas as paginas de um PDF.
    Retorna dict estruturado com metadados e conteudo.
    """
    pages = []
    full_text_parts = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            pages.append({"page": i, "text": text})
            if text:
                full_text_parts.append(text)

    return {
        "source":    pdf_path.name,
        "date":      pdf_path.parent.name,
        "pages":     pages,
        "full_text": "\n\n".join(full_text_parts),
    }


def run_extractor():
    """Processa todos os PDFs ainda nao extraidos."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(PDF_DIR.rglob("*.pdf"))
    print(f"\n {len(pdf_files)} PDFs encontrados para processar.")
    print(f" Salvando JSONs em: {OUTPUT_DIR}\n")

    sucesso = 0
    falhas  = 0

    for pdf_path in tqdm(pdf_files, desc="Extraindo textos"):
        output_path = OUTPUT_DIR / (pdf_path.stem + ".json")

        if output_path.exists():
            continue  # Ja processado

        try:
            data = extract_text_from_pdf(pdf_path)

            # Valida se extraiu algum texto
            if not data["full_text"].strip():
                print(f"\n  AVISO: sem texto em {pdf_path.name} (pode ser PDF escaneado)")

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            sucesso += 1

        except Exception as e:
            print(f"\n  ERRO em {pdf_path.name}: {e}")
            falhas += 1

    print(f"\n Resultado: {sucesso} extraidos | {falhas} com falha")


def preview_pdf(pdf_path: Path, max_chars: int = 500):
    """
    Mostra preview do texto de um PDF.
    Util para validar se a extracao esta funcionando.
    """
    print(f"\n Preview: {pdf_path.name}")
    print("-" * 60)
    data = extract_text_from_pdf(pdf_path)
    print(f"Paginas: {len(data['pages'])}")
    print(f"Tamanho total: {len(data['full_text'])} caracteres")
    print(f"\nPrimeiros {max_chars} caracteres:")
    print(data["full_text"][:max_chars])
    print("-" * 60)


if __name__ == "__main__":
    # Primeiro faz preview de 1 PDF para validar
    pdfs = list(PDF_DIR.rglob("*.pdf"))
    if pdfs:
        preview_pdf(pdfs[0])

    # Depois extrai todos
    run_extractor()