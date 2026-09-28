"""Orquestração do pipeline RAG completo e estruturas de resultado.

Pergunta -> HyDE -> embedding -> FAISS -> contexto -> LLM -> resposta.
Usado pela CLI, pela interface web e pelos scripts de avaliação.
"""

from dataclasses import dataclass, field

from . import config, generation, retrieval


@dataclass
class UsoTokens:
    """Acumula os tokens das duas chamadas ao LLM (HyDE + resposta final)."""

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    def somar(self, usage_metadata):
        if not usage_metadata:
            return
        self.input_tokens += usage_metadata.get("input_tokens", 0) or 0
        self.output_tokens += usage_metadata.get("output_tokens", 0) or 0
        self.total_tokens += usage_metadata.get("total_tokens", 0) or 0

    def custo_usd(self):
        custo_input = (
            self.input_tokens / 1_000_000
        ) * config.PRECO_USD_POR_MILHAO_INPUT
        custo_output = (
            self.output_tokens / 1_000_000
        ) * config.PRECO_USD_POR_MILHAO_OUTPUT
        return custo_input + custo_output


@dataclass
class RespostaRAG:
    """Resultado de uma consulta, com as etapas intermediárias expostas
    para que a interface possa mostrar o que o pipeline fez."""

    pergunta: str
    hipotese_hyde: str
    documentos: list
    contexto: str
    resposta: str
    tempo_hyde: float
    tempo_recuperacao: float
    tempo_resposta: float
    uso: UsoTokens = field(default_factory=UsoTokens)

    @property
    def tempo_total(self):
        return self.tempo_hyde + self.tempo_recuperacao + self.tempo_resposta


def responder_pergunta(
    llm,
    vectorstore,
    pergunta,
    historico=None,
    k=5,
    versao_prompt_hyde=None,
    versao_prompt_answer=None,
):
    """Roda o pipeline de ponta a ponta para uma pergunta."""
    uso = UsoTokens()

    hipotese, usage_hyde, tempo_hyde = generation.gerar_hipotese_hyde(
        llm, pergunta, versao_prompt_hyde
    )
    uso.somar(usage_hyde)

    documentos, tempo_recuperacao = retrieval.buscar_documentos(
        vectorstore, hipotese, k=k
    )

    contexto = retrieval.formatar_contexto(documentos)
    historico_texto = generation.formatar_historico(historico)

    resposta, usage_resposta, tempo_resposta = generation.gerar_resposta_final(
        llm,
        pergunta,
        contexto,
        historico_texto,
        versao_prompt_answer,
    )
    uso.somar(usage_resposta)

    return RespostaRAG(
        pergunta=pergunta,
        hipotese_hyde=hipotese,
        documentos=documentos,
        contexto=contexto,
        resposta=resposta,
        tempo_hyde=tempo_hyde,
        tempo_recuperacao=tempo_recuperacao,
        tempo_resposta=tempo_resposta,
        uso=uso,
    )
