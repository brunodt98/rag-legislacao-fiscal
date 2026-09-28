"""Interface web (Streamlit) do chatbot RAG (HyDE + FAISS + OpenRouter)."""

import os
import sys
from pathlib import Path

import streamlit as st

# Permite rodar direto (`streamlit run app/streamlit_app.py`) com a raiz do
# projeto no sys.path, para `import src`, e com app/ no sys.path, para `theme`.
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import src  # noqa: E402
import theme  # noqa: E402


st.set_page_config(
    page_title="Chatbot RAG + HyDE (ICMS/SP)",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

theme.aplicar()

ETAPAS = ["Pergunta", "HyDE", "Embedding", "FAISS", "Contexto", "Resposta"]


# ============================================================
# RECURSOS CACHEADOS (carregados uma vez por processo do servidor)
# ============================================================

@st.cache_resource(show_spinner="Carregando embeddings e vectorstore...")
def carregar_vectorstore():
    return src.get_vectorstore()


@st.cache_resource(show_spinner=False)
def carregar_llm(api_key, model, temperature):
    return src.build_llm(api_key, model=model, temperature=temperature)


# ============================================================
# SIDEBAR — CONFIGURAÇÃO
# ============================================================

with st.sidebar:
    theme.marca_lateral("Consulta ICMS", "Estado de São Paulo")

    st.markdown("<div class='side-rule'></div>", unsafe_allow_html=True)
    st.markdown("<div class='side-lbl'>Modelo</div>", unsafe_allow_html=True)

    api_key_input = st.text_input(
        "OPENROUTER_API_KEY",
        value=os.getenv("OPENROUTER_API_KEY", ""),
        type="password",
        help="Não é salva em disco. Também pode ser definida via .env.",
    )

    modelo = st.text_input("Modelo (OpenRouter)", value=src.DEFAULT_MODEL)

    temperatura = st.slider(
        "Temperatura", min_value=0.0, max_value=1.0,
        value=src.DEFAULT_TEMPERATURE, step=0.05,
    )

    st.markdown("<div class='side-rule'></div>", unsafe_allow_html=True)
    st.markdown("<div class='side-lbl'>Recuperação</div>", unsafe_allow_html=True)

    k_documentos = st.slider(
        "Documentos recuperados (k)", min_value=1, max_value=10, value=5,
    )

    mostrar_detalhes = st.checkbox(
        "Mostrar hipótese HyDE, trechos e métricas", value=True
    )

    st.markdown("<div class='side-rule'></div>", unsafe_allow_html=True)

    if st.button("Limpar conversa"):
        st.session_state["historico"] = []
        st.session_state["mensagens"] = []
        st.rerun()

    theme.rodape_lateral(
        "FT",
        "<b>Bruno Silva</b><br>Ciência de Dados · FATEC Cotia",
    )


# ============================================================
# CABEÇALHO
# ============================================================

theme.cabecalho(
    "RAG com HyDE",
    "Consulta à legislação de ICMS/SP",
    "Responde apenas com base nos documentos indexados. Cada pergunta é "
    "reescrita como hipótese documental antes da busca vetorial, e a resposta "
    "final é restrita aos trechos recuperados.",
)

theme.pipeline_visual(ETAPAS)
theme.regua()


# ============================================================
# CARREGAMENTO DO VECTORSTORE
# ============================================================

try:
    vectorstore = carregar_vectorstore()
except src.VectorstoreNaoEncontrado as e:
    st.error(str(e))
    st.stop()


# ============================================================
# ESTADO DA CONVERSA
# ============================================================

if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

if "historico" not in st.session_state:
    st.session_state["historico"] = []


def render_detalhes(detalhes):
    """Desenha o bloco de transparência do pipeline de uma resposta."""
    with st.expander("Como esta resposta foi construída"):
        st.markdown(
            f"<div class='hyde'><span class='tag'>Hipótese HyDE "
            f"— usada só como consulta de busca</span>"
            f"{detalhes['hipotese']}</div>",
            unsafe_allow_html=True,
        )

        theme.secao(
            "Métricas da consulta",
            "Tempo por etapa e tokens efetivamente cobrados pela API.",
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("HyDE", f"{detalhes['tempo_hyde']:.2f}s")
        c2.metric("Recuperação", f"{detalhes['tempo_recuperacao']:.2f}s")
        c3.metric("Resposta", f"{detalhes['tempo_resposta']:.2f}s")
        c4.metric("Total", f"{detalhes['tempo_total']:.2f}s")

        c1, c2, c3 = st.columns(3)
        c1.metric("Tokens de entrada", f"{detalhes['tokens_in']:,}".replace(",", "."))
        c2.metric("Tokens de saída", f"{detalhes['tokens_out']:,}".replace(",", "."))
        c3.metric("Custo estimado", f"US$ {detalhes['custo']:.6f}")

        theme.secao(
            f"Trechos recuperados ({len(detalhes['trechos'])})",
            "O que o FAISS devolveu e que serviu de base para a resposta.",
        )

        for i, trecho in enumerate(detalhes["trechos"], start=1):
            st.markdown(
                f"<div class='fonte'><h4>Trecho {i} — {trecho['fonte']}</h4>"
                f"<pre>{trecho['texto']}</pre></div>",
                unsafe_allow_html=True,
            )


for msg in st.session_state["mensagens"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("detalhes"):
            render_detalhes(msg["detalhes"])


pergunta = st.chat_input("Faça uma pergunta sobre a legislação indexada...")

if pergunta:
    if not api_key_input:
        st.error(
            "Informe uma OPENROUTER_API_KEY na barra lateral (ou defina no .env) "
            "antes de perguntar."
        )
        st.stop()

    st.session_state["mensagens"].append({"role": "user", "content": pergunta})

    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Gerando hipótese HyDE, buscando documentos e respondendo..."):
            try:
                llm = carregar_llm(api_key_input, modelo, temperatura)

                resultado = src.responder_pergunta(
                    llm,
                    vectorstore,
                    pergunta,
                    historico=st.session_state["historico"],
                    k=k_documentos,
                )

            except src.ChaveApiAusente as e:
                st.error(str(e))
                st.stop()

            except Exception as e:
                st.error(f"Ocorreu um erro ao consultar o modelo: {e}")
                st.stop()

        st.markdown(resultado.resposta)

        detalhes = None

        if mostrar_detalhes:
            detalhes = {
                "hipotese": resultado.hipotese_hyde,
                "tempo_hyde": resultado.tempo_hyde,
                "tempo_recuperacao": resultado.tempo_recuperacao,
                "tempo_resposta": resultado.tempo_resposta,
                "tempo_total": resultado.tempo_total,
                "tokens_in": resultado.uso.input_tokens,
                "tokens_out": resultado.uso.output_tokens,
                "custo": resultado.uso.custo_usd(),
                "trechos": [
                    {
                        "fonte": os.path.basename(
                            doc.metadata.get("source", "desconhecida")
                        ),
                        "texto": doc.page_content.strip()[:500],
                    }
                    for doc in resultado.documentos
                ],
            }

            render_detalhes(detalhes)

        st.session_state["historico"].append((pergunta, resultado.resposta))
        st.session_state["mensagens"].append({
            "role": "assistant",
            "content": resultado.resposta,
            "detalhes": detalhes,
        })
