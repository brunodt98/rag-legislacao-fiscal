"""Ingestão: carrega os .docx, divide em chunks e constrói o índice FAISS.

Uso:
    python -m src.ingestion
"""

import sys

from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from . import config
from .embeddings import get_embeddings


def listar_documentos():
    """Lista os .docx disponíveis em data/documentos/."""
    arquivos = sorted(config.DOCUMENTOS_DIR.glob("*.docx"))

    if not arquivos:
        raise SystemExit(
            f"Nenhum arquivo .docx encontrado em:\n{config.DOCUMENTOS_DIR}"
        )

    return arquivos


def carregar_documentos(arquivos):
    """Extrai o texto de cada .docx (um Document por arquivo)."""
    documentos = []

    for arquivo in arquivos:
        print(f"Carregando: {arquivo.name}")
        documentos.extend(Docx2txtLoader(str(arquivo)).load())

    return documentos


def dividir_em_chunks(documentos):
    """Quebra os documentos em trechos menores que o limite de contexto.

    O overlap evita que uma informação partida entre dois chunks fique
    incompleta nos dois — relevante em texto legal, com frases longas.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )

    return splitter.split_documents(documentos)


def construir_indice(chunks):
    """Gera os embeddings dos chunks e grava o índice FAISS em disco."""
    print("\nCarregando modelo de embeddings...")
    embeddings = get_embeddings()

    print("Criando banco vetorial FAISS...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    config.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(config.VECTORSTORE_DIR))

    return vectorstore


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    arquivos = listar_documentos()

    print("Documentos encontrados:")
    for arquivo in arquivos:
        print(f"  - {arquivo.name}")
    print()

    documentos = carregar_documentos(arquivos)
    print(f"\nDocumentos carregados: {len(documentos)}")

    chunks = dividir_em_chunks(documentos)
    print(
        f"Chunks gerados: {len(chunks)} "
        f"(chunk_size={config.CHUNK_SIZE}, overlap={config.CHUNK_OVERLAP})"
    )

    construir_indice(chunks)

    print(f"\nIndice criado em: {config.VECTORSTORE_DIR}")
    print(f"  - {config.INDEX_FAISS.name}")
    print(f"  - {config.INDEX_PKL.name}")


if __name__ == "__main__":
    main()
