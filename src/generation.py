"""Etapas que usam o LLM: hipótese HyDE e resposta final."""

import time
from functools import lru_cache

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from . import config, prompts


def build_llm(api_key, model=None, temperature=None, base_url=None):
    """Cria o cliente do LLM apontando para a OpenRouter (API compatível
    com a da OpenAI, o que permite reusar o ChatOpenAI)."""
    if not api_key:
        raise config.ChaveApiAusente(
            "Nenhuma OPENROUTER_API_KEY foi fornecida (.env ou UI)."
        )

    return ChatOpenAI(
        model=model or config.DEFAULT_MODEL,
        temperature=(
            config.DEFAULT_TEMPERATURE if temperature is None else temperature
        ),
        api_key=api_key,
        base_url=base_url or config.OPENROUTER_BASE_URL,
    )


@lru_cache(maxsize=8)
def _prompt_template(tipo, versao=None):
    _, template = prompts.carregar_prompt(tipo, versao)
    return ChatPromptTemplate.from_template(template)


def _invocar_llm(llm, prompt_template, variaveis):
    mensagens = prompt_template.format_messages(**variaveis)
    resposta = llm.invoke(mensagens)
    texto = (resposta.content or "").strip()
    usage = getattr(resposta, "usage_metadata", None)
    return texto, usage


def gerar_hipotese_hyde(llm, pergunta, versao_prompt=None):
    """HyDE: transforma a pergunta num trecho hipotético no estilo do
    documento, para ser usado como consulta na busca vetorial."""
    prompt_template = _prompt_template("hyde", versao_prompt)

    inicio = time.perf_counter()
    hipotese, usage = _invocar_llm(
        llm, prompt_template, {"user_input": pergunta}
    )
    tempo = time.perf_counter() - inicio

    if not hipotese:
        raise ValueError("O modelo não gerou uma hipótese HyDE.")

    return hipotese, usage, tempo


def gerar_resposta_final(
    llm, pergunta, contexto, historico_texto, versao_prompt=None
):
    """Gera a resposta ao usuário fundamentada apenas no contexto recuperado."""
    prompt_template = _prompt_template("answer", versao_prompt)

    inicio = time.perf_counter()
    resposta, usage = _invocar_llm(
        llm,
        prompt_template,
        {
            "user_input": pergunta,
            "context": contexto,
            "history": historico_texto,
        },
    )
    tempo = time.perf_counter() - inicio

    return resposta, usage, tempo


def formatar_historico(historico, max_turnos=5):
    """Serializa os últimos turnos da conversa para o prompt de resposta."""
    if not historico:
        return "Nenhuma conversa anterior."

    return "\n".join(
        f"Usuário: {pergunta}\nAssistente: {resposta}"
        for pergunta, resposta in historico[-max_turnos:]
    )
