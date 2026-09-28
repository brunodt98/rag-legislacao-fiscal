"""Identidade visual compartilhada entre os projetos de ICMS/SP.

Mesmos tokens e mesmo CSS do painel ICMS Educacional SP
(github.com/brunodt98/icms-educacional-sp), para que os dois projetos
sejam lidos como um conjunto.
"""

import streamlit as st


# ============================================================
# DESIGN TOKENS
# ============================================================
# Paleta institucional: azul-marinho e vermelho da bandeira paulista, com o
# vermelho conversando com a identidade do Centro Paula Souza (FATEC). O
# dourado marca apenas o estado ativo da navegacao.

SURFACE = "#ffffff"
PLANE = "#f4f3ef"
INK = "#14161a"
INK_2 = "#4a4f57"
MUTED = "#767c86"
GRID = "#e3e1da"

NAVY_DEEP = "#0b1f3d"   # barra lateral
NAVY = "#12305c"        # institucional
NAVY_LINE = "#1e3a63"   # divisorias sobre o navy
BLUE = "#2c6bb8"        # destaque / acento
GOLD = "#e8b33a"        # marcador de selecao
CRITICAL = "#b7202e"    # alerta

ON_NAVY = "#c6d4e6"     # texto secundario sobre a lateral
ON_NAVY_DIM = "#9fb2cc"

SANS = '"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif'
SERIF = '"Source Serif 4", Georgia, "Times New Roman", serif'


# A marca e' um sinal grafico proprio do projeto (faixas diagonais nas cores
# da bandeira paulista), NAO o brasao oficial do Estado: este e' um trabalho
# academico, nao uma publicacao do governo.
MARCA_SVG = f"""
<svg width="38" height="38" viewBox="0 0 38 38" aria-hidden="true" class="mark">
  <rect x="0" y="0" width="38" height="38" rx="7" fill="#ffffff"></rect>
  <path d="M0 26 L38 6 L38 13 L0 33 Z" fill="{CRITICAL}"></path>
  <path d="M0 15 L38 -5 L38 2 L0 22 Z" fill="{NAVY}"></path>
  <rect x="0" y="0" width="38" height="38" rx="7" fill="none"
        stroke="{NAVY}" stroke-width="1.5"></rect>
</svg>"""


CSS = f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap');

  .stApp {{ background: {PLANE}; }}
  [data-testid="stHeader"] {{ background: transparent; }}
  [data-testid="stMainBlockContainer"] {{
      padding: 1.9rem 2.4rem 5rem; max-width: 1100px;
  }}
  html, body, [class*="st-"] {{ font-family: {SANS}; }}

  /* Os icones do Streamlit sao ligaduras de uma fonte propria. A regra
     de font-family acima alcanca esses spans e faz o NOME do icone
     aparecer como texto (ex.: 'arrow_down'), entao restauramos a fonte. */
  [data-testid="stIconMaterial"],
  span[class*="material-symbols"] {{
      font-family: "Material Symbols Rounded" !important;
  }}

  /* ---------- barra lateral ---------- */
  [data-testid="stSidebar"] {{ background: {NAVY_DEEP}; border-right: 0; }}
  [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
      padding: 1.5rem 1.15rem 1.2rem;
  }}
  [data-testid="stSidebar"] * {{ color: #ffffff; }}
  [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
      font-size: .76rem !important; color: {ON_NAVY_DIM}; font-weight: 500;
  }}
  .side-lbl {{
      font-size: .66rem; letter-spacing: .1em; text-transform: uppercase;
      color: #7e93b3; margin: .1rem 0 .55rem;
  }}
  .side-rule {{ height: 1px; background: {NAVY_LINE}; margin: 1.15rem 0; }}
  .side-brand {{ display: flex; align-items: center; gap: .72rem; }}
  .side-brand .mark {{ flex: 0 0 auto; }}
  .side-brand .nm {{
      font-family: {SERIF}; font-size: 1.02rem; font-weight: 600;
      letter-spacing: -.01em; line-height: 1.15; color: #fff;
  }}
  .side-brand .uf {{
      font-size: .68rem; letter-spacing: .05em; text-transform: uppercase;
      color: {ON_NAVY_DIM}; margin-top: .12rem;
  }}
  .side-foot {{
      display: flex; align-items: center; gap: .65rem;
      padding-top: .95rem; border-top: 1px solid {NAVY_LINE}; margin-top: .6rem;
  }}
  .side-foot .sigla {{
      width: 30px; height: 30px; border-radius: 6px; background: {CRITICAL};
      display: flex; align-items: center; justify-content: center;
      font-size: .66rem; font-weight: 600; color: #fff; flex: 0 0 auto;
  }}
  .side-foot .txt {{ font-size: .68rem; color: {ON_NAVY_DIM}; line-height: 1.4; }}
  .side-foot .txt b {{ color: #fff; font-weight: 500; }}

  /* campos na lateral */
  [data-testid="stSidebar"] [data-baseweb="select"] > div,
  [data-testid="stSidebar"] [data-testid="stTextInput"] input {{
      background: #112b52; border-color: #2a4b7c; color: #fff;
      border-radius: 7px; font-size: .82rem;
  }}
  [data-testid="stSidebar"] [data-baseweb="radio"] svg {{ fill: {GOLD}; }}
  [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {{
      background: {GOLD};
  }}
  [data-testid="stSidebar"] [data-testid="stButton"] button {{
      background: transparent; border: 1px solid #2a4b7c; color: {ON_NAVY};
      font-size: .82rem; border-radius: 7px; width: 100%;
  }}
  [data-testid="stSidebar"] [data-testid="stButton"] button:hover {{
      border-color: {GOLD}; color: #fff;
  }}

  /* ajuda fixa na lateral: como obter a chave */
  .side-help {{
      background: #112b52; border: 1px solid #2a4b7c; border-radius: 8px;
      padding: .7rem .8rem; margin-top: .55rem;
  }}
  .side-help .tit {{
      font-size: .72rem; font-weight: 600; color: #fff; margin-bottom: .35rem;
  }}
  .side-help ol {{ margin: 0; padding-left: 1.05rem; }}
  .side-help li {{
      font-size: .72rem; color: {ON_NAVY}; line-height: 1.5; margin-bottom: .22rem;
  }}
  .side-help a {{ color: {GOLD}; text-decoration: underline; font-weight: 500; }}
  .side-help code {{
      background: #0b1f3d; color: #fff; font-size: .68rem;
      padding: .04rem .26rem; border-radius: 3px;
  }}
  .side-help .nota {{
      font-size: .68rem; color: {ON_NAVY_DIM}; line-height: 1.45;
      margin: .45rem 0 0; padding-top: .45rem; border-top: 1px solid #2a4b7c;
  }}

  /* ---------- cabecalho ---------- */
  .eyebrow {{
      font-size: .7rem; font-weight: 600; letter-spacing: .09em;
      text-transform: uppercase; color: {MUTED}; margin-bottom: .45rem;
  }}
  h1.hero {{
      font-family: {SERIF}; font-size: 2.05rem; font-weight: 600;
      letter-spacing: -.022em; color: {INK}; margin: 0 0 .45rem; line-height: 1.1;
  }}
  .lede {{
      font-size: .93rem; color: {INK_2}; max-width: 74ch;
      line-height: 1.55; margin-bottom: .9rem;
  }}
  .rule {{ height: 1px; background: {GRID}; margin: 1.35rem 0 1.2rem; border: 0; }}

  /* fluxo do pipeline, no cabecalho */
  .pipe {{ display: flex; flex-wrap: wrap; align-items: center; gap: .4rem; }}
  .pipe span {{
      font-size: .74rem; color: {INK_2}; background: {SURFACE};
      border: 1px solid {GRID}; border-radius: 999px; padding: .26rem .7rem;
  }}
  .pipe span.on {{
      background: {NAVY}; border-color: {NAVY}; color: #fff; font-weight: 500;
  }}
  .pipe i {{ color: {MUTED}; font-style: normal; font-size: .74rem; }}

  /* ---------- titulos de secao ---------- */
  .sec {{ margin: 1.9rem 0 .85rem; }}
  .sec h2 {{
      font-size: 1.02rem; font-weight: 640; color: {INK};
      margin: 0 0 .2rem; letter-spacing: -.01em;
  }}
  .sec p {{ font-size: .82rem; color: {MUTED}; margin: 0; line-height: 1.5; }}

  /* ---------- stat tiles ---------- */
  [data-testid="stMetric"] {{
      background: {SURFACE}; border: 1px solid {GRID};
      border-top: 3px solid {NAVY}; border-radius: 10px; padding: .8rem .95rem;
  }}
  [data-testid="stMetricLabel"] p {{
      font-size: .74rem !important; font-weight: 550; color: {MUTED};
      letter-spacing: .01em; line-height: 1.3;
  }}
  [data-testid="stMetricValue"] {{
      font-family: {SERIF}; font-size: 1.45rem !important; font-weight: 600;
      color: {INK}; letter-spacing: -.02em;
      font-variant-numeric: proportional-nums;
  }}

  /* ---------- chat ---------- */
  [data-testid="stChatMessage"] {{
      background: {SURFACE}; border: 1px solid {GRID}; border-radius: 10px;
      padding: .95rem 1.1rem; margin-bottom: .6rem;
  }}
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
      background: {PLANE}; border-style: dashed;
  }}
  [data-testid="stChatMessage"] p {{ color: {INK_2}; line-height: 1.6; }}
  [data-testid="stChatInput"] {{
      border-color: {GRID}; border-radius: 10px; background: {SURFACE};
  }}

  /* hipotese HyDE: citacao, para nao ser confundida com a resposta */
  .hyde {{
      background: {SURFACE}; border: 1px solid {GRID};
      border-left: 3px solid {GOLD}; border-radius: 8px;
      padding: .8rem 1rem; font-size: .86rem; color: {INK_2}; line-height: 1.6;
  }}
  .hyde .tag {{
      display: block; font-size: .68rem; letter-spacing: .08em;
      text-transform: uppercase; color: {MUTED}; margin-bottom: .35rem;
  }}

  /* trecho recuperado */
  .fonte {{
      background: {SURFACE}; border: 1px solid {GRID};
      border-left: 3px solid {BLUE}; border-radius: 8px;
      padding: .75rem .95rem; margin-bottom: .55rem;
  }}
  .fonte h4 {{
      font-size: .8rem; font-weight: 620; color: {INK}; margin: 0 0 .3rem;
  }}
  .fonte pre {{
      font-size: .76rem; color: {INK_2}; line-height: 1.55; margin: 0;
      white-space: pre-wrap; font-family: {SANS};
  }}

  [data-testid="stElementToolbar"] {{ display: none; }}
</style>
"""


def aplicar():
    """Injeta a folha de estilo. Chamar uma vez, logo após set_page_config."""
    st.markdown(CSS, unsafe_allow_html=True)


def ajuda_chave():
    """Passo a passo para obter a chave da OpenRouter, fixo na lateral."""
    st.markdown(
        "<div class='side-help'>"
        "<div class='tit'>Não tem chave?</div>"
        "<ol>"
        "<li>Crie uma conta em <a href='https://openrouter.ai'"
        " target='_blank'>openrouter.ai</a> (Google ou GitHub).</li>"
        "<li>Abra <a href='https://openrouter.ai/keys'"
        " target='_blank'>openrouter.ai/keys</a> e clique em "
        "<b>Create Key</b>.</li>"
        "<li>Copie a chave (começa com <code>sk-or-</code> e aparece uma vez "
        "só) e cole no campo acima.</li>"
        "</ol>"
        "<p class='nota'>Modelos pagos exigem crédito na conta. "
        "Para testar sem crédito, use um modelo terminado em "
        "<code>:free</code>.</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def cabecalho(eyebrow, titulo, lede):
    st.markdown(
        f"<div class='eyebrow'>{eyebrow}</div>"
        f"<h1 class='hero'>{titulo}</h1>"
        f"<p class='lede'>{lede}</p>",
        unsafe_allow_html=True,
    )


def pipeline_visual(etapas, ativa=None):
    """Mostra as etapas do pipeline como trilha, destacando a etapa `ativa`."""
    partes = []

    for i, etapa in enumerate(etapas):
        classe = "on" if etapa == ativa else ""
        partes.append(f"<span class='{classe}'>{etapa}</span>")
        if i < len(etapas) - 1:
            partes.append("<i>&rsaquo;</i>")

    st.markdown(
        f"<div class='pipe'>{''.join(partes)}</div>", unsafe_allow_html=True
    )


def secao(titulo, sub=""):
    st.markdown(
        f"<div class='sec'><h2>{titulo}</h2>"
        f"{f'<p>{sub}</p>' if sub else ''}</div>",
        unsafe_allow_html=True,
    )


def marca_lateral(nome, subtitulo):
    st.markdown(
        f"<div class='side-brand'>{MARCA_SVG}"
        f"<div><div class='nm'>{nome}</div>"
        f"<div class='uf'>{subtitulo}</div></div></div>",
        unsafe_allow_html=True,
    )


def rodape_lateral(sigla, texto):
    st.markdown(
        f"<div class='side-foot'><div class='sigla'>{sigla}</div>"
        f"<div class='txt'>{texto}</div></div>",
        unsafe_allow_html=True,
    )


def regua():
    st.markdown("<hr class='rule'>", unsafe_allow_html=True)
