"""Pipeline RAG com HyDE sobre documentos de ICMS/SP.

Reexporta a API usada pelas interfaces (app/) e pelos scripts de avaliação
(eval/), para que elas não precisem conhecer a divisão interna dos módulos.
"""

from .config import (
    ChaveApiAusente,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    EMBEDDING_MODEL,
    VECTORSTORE_DIR,
    VectorstoreNaoEncontrado,
)
from .embeddings import get_embeddings, get_vectorstore
from .generation import build_llm
from .pipeline import RespostaRAG, UsoTokens, responder_pergunta
from .retrieval import buscar_documentos_por_texto

__all__ = [
    "ChaveApiAusente",
    "DEFAULT_MODEL",
    "DEFAULT_TEMPERATURE",
    "EMBEDDING_MODEL",
    "VECTORSTORE_DIR",
    "VectorstoreNaoEncontrado",
    "get_embeddings",
    "get_vectorstore",
    "build_llm",
    "RespostaRAG",
    "UsoTokens",
    "responder_pergunta",
    "buscar_documentos_por_texto",
]
