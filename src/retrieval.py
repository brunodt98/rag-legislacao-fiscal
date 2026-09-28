"""Etapa de recuperação: busca semântica no FAISS e formatação do contexto."""

import time


def buscar_documentos(vectorstore, consulta, k=5):
    """Busca os k chunks mais similares à `consulta` e cronometra a busca."""
    inicio = time.perf_counter()
    documentos = vectorstore.similarity_search(consulta, k=k)
    tempo = time.perf_counter() - inicio
    return documentos, tempo


def buscar_documentos_por_texto(vectorstore, texto, k=5):
    """Recuperação direta (sem HyDE) — usada na avaliação de retrieval
    e como baseline de comparação, já que não depende do LLM."""
    return buscar_documentos(vectorstore, texto, k=k)


def formatar_contexto(documentos):
    """Monta o bloco de contexto enviado ao LLM, identificando a fonte
    de cada chunk para que a resposta possa ser rastreada."""
    partes = []

    for i, documento in enumerate(documentos, start=1):
        texto = documento.page_content.strip()
        fonte = documento.metadata.get("source", "Documento não identificado")

        partes.append(f"\nDOCUMENTO {i}\nFonte: {fonte}\n\n{texto}\n")

    return "\n".join(partes)
