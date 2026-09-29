"""Interface de chat (Streamlit) do Guia Tech.  Rodar: streamlit run src/app.py"""
import streamlit as st
from assistente import carregar_base, responder

st.set_page_config(page_title="Guia Tech", page_icon="🧭")
st.title("🧭 Guia Tech")
st.caption("Assistente para quem está começando em tecnologia. Respondo apenas com base na minha base de conhecimento.")

with st.sidebar:
    st.header("Configurações")
    usar_llm = st.toggle("Usar LLM local (Ollama)", value=False,
                         help="Desligado: respostas montadas direto da base. Ligado: o modelo redige a resposta usando só a base.")
    modelo = st.text_input("Modelo Ollama", "llama3.2")
    url = st.text_input("URL do Ollama", "http://localhost:11434")
    if st.button("Limpar conversa"):
        st.session_state.mensagens = []

@st.cache_data
def base():
    return carregar_base()

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for m in st.session_state.mensagens:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if pergunta := st.chat_input("Ex.: Quero começar em tecnologia, por onde vou?"):
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)
    hist = [{"role": m["role"], "content": m["content"]} for m in st.session_state.mensagens[:-1]]
    res = responder(pergunta, base(), usar_llm, modelo, url, hist)
    texto = res["texto"] + (f"\n\n_Fontes: {', '.join(res['fontes'])}_" if res["fontes"] else "")
    with st.chat_message("assistant"):
        st.markdown(texto)
    st.session_state.mensagens.append({"role": "assistant", "content": texto})
