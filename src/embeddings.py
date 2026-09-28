"""Modelo de embeddings e carregamento do índice vetorial FAISS."""

from functools import lru_cache

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from . import config


@lru_cache(maxsize=1)
def get_embeddings():
    """Carrega o modelo de embeddings uma única vez por processo."""
    return HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


@lru_cache(maxsize=1)
def get_vectorstore():
    """Abre o índice FAISS já construído em vectorstore/."""
    if not config.INDEX_FAISS.exists() or not config.INDEX_PKL.exists():
        raise config.VectorstoreNaoEncontrado(
            f"Vectorstore não encontrado em {config.VECTORSTORE_DIR}. "
            f"Rode `python -m src.ingestion` primeiro."
        )

    return FAISS.load_local(
        str(config.VECTORSTORE_DIR),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )
