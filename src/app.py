import streamlit as st
import os
from assistente_financeiro import (
    carregar_dados,
    responder,
    analisar_gastos,
    gerar_insights
)

# =========================
# ⚙️ Configuração
# =========================
st.set_page_config(
    page_title="Assistente Financeiro Inteligente",
    page_icon="💰",
    layout="wide"
)

# =========================
# 🎨 Carregar CSS externo
# =========================
def carregar_css():
    caminho = os.path.join(os.path.dirname(__file__), "style.css")
    with open(caminho) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

carregar_css()

# =========================
# 🎨 Header
# =========================
st.markdown("""
<div style='
    text-align:center;
    padding:25px;
    background:white;
    border-radius:15px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.05);
    margin-bottom:20px;
'>
<h1>💰 Assistente Financeiro Inteligente</h1>
<p>Transformando dados em decisões financeiras inteligentes</p>
<p><b>Desenvolvido por Natália Baptista Pastre</b></p>
</div>
""", unsafe_allow_html=True)

# =========================
# 🧠 Dados
# =========================
transacoes, perfil = carregar_dados()

if transacoes is None or perfil is None:
    st.error("Erro ao carregar dados. Verifique a pasta 'data'.")
    st.stop()

total, por_categoria = analisar_gastos(transacoes)

# =========================
# 📊 CARDS
# =========================
col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class="card">
<h3>💸 Total gasto</h3>
<h2>R$ {total:.2f}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="card">
<h3>👤 Perfil</h3>
<h2>{perfil['perfil'].capitalize()}</h2>
</div>
""", unsafe_allow_html=True)

if len(por_categoria) > 0:
    maior_categoria = por_categoria.idxmax()
else:
    maior_categoria = "N/A"

col3.markdown(f"""
<div class="card">
<h3>📊 Maior gasto</h3>
<h2>{maior_categoria}</h2>
</div>
""", unsafe_allow_html=True)

# =========================
# 📈 GRÁFICO
# =========================
st.markdown("### 📊 Análise de gastos")
st.bar_chart(por_categoria)

# =========================
# 💡 INSIGHTS
# =========================
st.markdown("### 💡 Insights financeiros")

insights = gerar_insights(total, por_categoria)

for insight in insights:
    st.success(insight)

# =========================
# 💬 CHAT
# =========================
st.markdown("### 💬 Assistente IA")

if "chat" not in st.session_state:
    st.session_state.chat = []

col_chat, col_btn = st.columns([4,1])

with col_chat:
    pergunta = st.text_input("Digite sua pergunta:")

with col_btn:
    if st.button("🗑 Limpar"):
        st.session_state.chat = []

if pergunta:
    resposta = responder(pergunta, transacoes, perfil)

    st.session_state.chat.append(("user", pergunta))
    st.session_state.chat.append(("bot", resposta))

# =========================
# 🗨️ Histórico
# =========================
for autor, msg in st.session_state.chat:
    if autor == "user":
        st.markdown(f'<div class="chat-user">🧑 {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bot">🤖 {msg}</div>', unsafe_allow_html=True)

# =========================
# 🔻 Rodapé
# =========================
st.markdown("""
<hr>
<p style='text-align:center'>
Desenvolvido por Natália Baptista Pastre © 2026</b> 🚀
</p>
""", unsafe_allow_html=True)