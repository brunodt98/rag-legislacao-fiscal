"""Configuração central do projeto: caminhos, modelos e variáveis de ambiente."""

import os
from pathlib import Path

from dotenv import load_dotenv


# Raiz do projeto (um nível acima de src/)
ROOT_DIR = Path(__file__).resolve().parents[1]

load_dotenv(ROOT_DIR / ".env")


# ============================================================
# CAMINHOS
# ============================================================

DOCUMENTOS_DIR = ROOT_DIR / "data" / "documentos"

VECTORSTORE_DIR = ROOT_DIR / "vectorstore"
INDEX_FAISS = VECTORSTORE_DIR / "index.faiss"
INDEX_PKL = VECTORSTORE_DIR / "index.pkl"

PROMPTS_FILE = Path(__file__).parent / "prompts.yaml"


# ============================================================
# MODELOS
# ============================================================

# Embeddings rodam localmente em CPU, sem custo de API. Trocar este modelo
# exige reconstruir o índice FAISS (as dimensões/vetores mudam).
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1",
)

DEFAULT_MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

DEFAULT_TEMPERATURE = float(os.getenv("TEMPERATURE", "0.5"))


# ============================================================
# CHUNKING
# ============================================================

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))


# ============================================================
# PREÇO DE REFERÊNCIA (apenas para estimar custo nos relatórios)
# ============================================================

PRECO_USD_POR_MILHAO_INPUT = float(
    os.getenv("PRECO_USD_POR_MILHAO_INPUT", "0.02")
)
PRECO_USD_POR_MILHAO_OUTPUT = float(
    os.getenv("PRECO_USD_POR_MILHAO_OUTPUT", "0.10")
)


# ============================================================
# ERROS
# ============================================================

class VectorstoreNaoEncontrado(RuntimeError):
    pass


class ChaveApiAusente(RuntimeError):
    pass
