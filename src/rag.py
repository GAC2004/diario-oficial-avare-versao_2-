"""
rag.py - Busca semantica sobre o Diario Oficial de Avare.

Sem LLM externo. O sistema:
  1. Transforma a pergunta em embedding
  2. Busca os trechos mais relevantes no indice FAISS
  3. Permite filtrar por ano e/ou mes (periodo AAAA-MM)
  4. Retorna os trechos ordenados por relevancia
"""

import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import faiss
import pickle
import threading
from pathlib import Path
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DB_DIR = BASE_DIR / "vector_db"

INDEX_FILE = "index.faiss"
METADATA_PATH = VECTOR_DB_DIR / "metadata.pkl"
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 5


def faiss_load() -> faiss.Index:
    if not VECTOR_DB_DIR.exists():
        raise FileNotFoundError(
            f"Pasta vector_db não encontrada: {VECTOR_DB_DIR}"
        )

    index_path = VECTOR_DB_DIR / INDEX_FILE

    if not index_path.exists():
        raise FileNotFoundError(
            f"Arquivo index.faiss não encontrado: {index_path}"
        )

    return faiss.read_index(str(index_path))


class DiarioOficialRAG:

    def __init__(self):
        self.lock = threading.Lock()

        print(" Carregando indice e metadados...")
        self._load()

        print(" Carregando modelo de embeddings...")
        self.embed_model = SentenceTransformer(MODEL_NAME)

        print(" Sistema pronto!\n")

    def _load(self):
        self.index = faiss_load()

        if not METADATA_PATH.exists():
            raise FileNotFoundError(
                f"Arquivo metadata.pkl não encontrado: {METADATA_PATH}"
            )

        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def reload(self):
        """Recarrega indice e metadados apos uma atualizacao da base."""
        with self.lock:
            self._load()

        print(f" Indice recarregado: {self.index.ntotal} vetores.")

    def stats(self) -> dict:
        with self.lock:
            metadata = self.metadata
            total_vetores = self.index.ntotal

        datas = sorted(
            set(
                m["date"]
                for m in metadata
                if m["date"] != "sem-data"
            )
        )

        anos = sorted(
            set(d[:4] for d in datas),
            reverse=True
        )

        fontes = set(
            m["source"]
            for m in metadata
        )

        return {
            "total_chunks": len(metadata),
            "total_vetores": total_vetores,
            "total_docs": len(fontes),
            "periodo_inicio": datas[0] if datas else "-",
            "periodo_fim": datas[-1] if datas else "-",
            "anos": anos,
        }

    def search(
        self,
        query: str,
        top_k: int = TOP_K,
        ano: str = None,
        mes: str = None
    ) -> list[dict]:
        """
        Busca chunks relevantes. Se ano ou mes forem informados,
        filtra os resultados por periodo (mes no formato AAAA-MM).
        """

        with self.lock:
            index = self.index
            metadata = self.metadata

        emb = self.embed_model.encode(
            [query],
            convert_to_numpy=True
        )

        faiss.normalize_L2(emb)

        fetch_k = (
            top_k
            if not (ano or mes)
            else min(index.ntotal, max(top_k * 50, 200))
        )

        distances, indices = index.search(
            emb,
            fetch_k
        )

        results = []

        for dist, idx in zip(
            distances[0],
            indices[0]
        ):
            if idx == -1:
                continue

            chunk = metadata[idx]

            if mes and chunk["date"] != mes:
                continue

            if ano and not chunk["date"].startswith(ano):
                continue

            c = chunk.copy()
            c["score"] = round(float(dist), 4)

            results.append(c)

            if len(results) >= top_k:
                break

        return results

    def ask(
        self,
        question: str,
        top_k: int = TOP_K,
        ano: str = None,
        mes: str = None
    ) -> dict:

        chunks = self.search(
            question,
            top_k=top_k,
            ano=ano,
            mes=mes
        )

        if not chunks:
            return {
                "trechos": [],
                "sources": [],
                "resumo": "Nenhum trecho relevante encontrado para os filtros aplicados.",
            }

        sources = []

        for chunk in chunks:
            ref = f"{chunk['source']} — periodo {chunk['date']}"

            if ref not in sources:
                sources.append(ref)

        return {
            "trechos": chunks,
            "sources": sources,
            "resumo": f"{len(chunks)} trechos encontrados.",
        }


if __name__ == "__main__":
    rag = DiarioOficialRAG()

    print(rag.stats())

    for c in rag.ask(
        "decretos municipais",
        top_k=3,
        ano="2026"
    )["trechos"]:
        print(
            c["score"],
            c["source"],
            c["date"]
        )