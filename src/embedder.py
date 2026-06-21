#embedder.py
import json
import pickle
import gc
import os
from pathlib import Path

import faiss
import torch
from sentence_transformers import SentenceTransformer

# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"
VECTOR_DB_DIR = BASE_DIR / "vector_db"

# 🔥 GARANTE QUE A PASTA EXISTE (ESSENCIAL NO WINDOWS)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = VECTOR_DB_DIR / "index.faiss"
METADATA_PATH = VECTOR_DB_DIR / "metadata.pkl"

# =========================
# DEVICE (CPU/GPU AUTO)
# =========================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🔥 Usando device: {DEVICE}")

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2",
    device=DEVICE
)

# =========================
# CHUNKING
# =========================

def chunk_text(text, source, date, size=1500, overlap=200):
    text = text.strip()
    chunks = []

    i = 0
    while i < len(text):
        chunks.append({
            "source": source,
            "date": date,
            "text": text[i:i + size]
        })
        i += size - overlap

    return chunks


# =========================
# FAISS SAVE (WINDOWS SAFE)
# =========================

def save_index(index):
    try:
        gc.collect()

        # 🔥 SEM .tmp no Windows (evita erro de path)
        final_path = INDEX_PATH

        # salva direto em arquivo temporário simples
        temp_path = VECTOR_DB_DIR / "index_temp.faiss"

        faiss.write_index(index, str(temp_path))

        if final_path.exists():
            final_path.unlink()

        temp_path.replace(final_path)

        print("💾 Index salvo com segurança")

    except Exception as e:
        print(f"❌ Erro ao salvar index: {e}")


def load_index(dim):
    if INDEX_PATH.exists():
        return faiss.read_index(str(INDEX_PATH))
    return faiss.IndexHNSWFlat(dim, 32)


# =========================
# CARREGAR DOCS
# =========================

def load_all_documents():
    docs = []

    for file in PROCESSED_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                doc = json.load(f)

            if doc.get("full_text"):
                docs.append(doc)

        except Exception as e:
            print(f"⚠️ erro {file}: {e}")

    return docs


# =========================
# BUILD COMPLETO
# =========================

def build_index():
    print("\n🚀 Iniciando pipeline completo...")

    docs = load_all_documents()

    print(f"📄 Documentos: {len(docs)}")

    all_chunks = []

    for doc in docs:
        all_chunks.extend(
            chunk_text(
                doc["full_text"],
                doc["source"],
                doc["date"]
            )
        )

    print(f"📦 Chunks: {len(all_chunks)}")

    texts = [c["text"] for c in all_chunks]

    print("⚡ Gerando embeddings...")

    embeddings = model.encode(
        texts,
        batch_size=64 if DEVICE == "cuda" else 32,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]

    index = faiss.IndexHNSWFlat(dim, 32)
    index.add(embeddings)

    save_index(index)

    gc.collect()

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(all_chunks, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"✅ Index criado com {len(all_chunks)} vetores")


# =========================
# UPDATE INCREMENTAL
# =========================

def update_index():
    if not INDEX_PATH.exists():
        print("⚠️ Index não existe, criando do zero...")
        build_index()
        return

    print("\n📂 Carregando index...")

    index = faiss.read_index(str(INDEX_PATH))

    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    existing = {m["source"] for m in metadata}

    new_chunks = []

    for file in PROCESSED_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                doc = json.load(f)

            if doc["source"] in existing:
                continue

            if not doc.get("full_text"):
                continue

            new_chunks.extend(
                chunk_text(
                    doc["full_text"],
                    doc["source"],
                    doc["date"]
                )
            )

        except Exception as e:
            print(f"⚠️ erro {file}: {e}")

    if not new_chunks:
        print("⚠️ Nada novo")
        return

    print(f"📦 Novos chunks: {len(new_chunks)}")

    texts = [c["text"] for c in new_chunks]

    embeddings = model.encode(
        texts,
        batch_size=64 if DEVICE == "cuda" else 32,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    faiss.normalize_L2(embeddings)

    index.add(embeddings)

    metadata.extend(new_chunks)

    save_index(index)

    gc.collect()

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"🔥 Atualizado: {index.ntotal} vetores")


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    build_index()