"""Núcleo do assistente Guia Tech: busca na base de conhecimento + resposta.

Funciona em dois modos:
- Com LLM local (Ollama): a resposta é redigida pelo modelo, usando SOMENTE o contexto recuperado.
- Sem LLM (modo offline): a resposta é montada diretamente a partir da base.
"""
import json
import re
import unicodedata
from pathlib import Path

import requests

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LIMIAR_MINIMO = 3  # pontuação mínima para considerar que há informação suficiente

STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "de", "do", "da", "dos", "das", "em", "no", "na",
    "nos", "nas", "por", "para", "pra", "com", "sem", "e", "ou", "que", "qual", "quais",
    "como", "quero", "quer", "eu", "voce", "me", "meu", "minha", "se", "ser", "sao", "e",
    "tem", "ter", "preciso", "posso", "pode", "vale", "mais", "muito", "sobre", "ao",
    "onde", "quando", "aprender", "ajuda", "ajudar", "oi", "ola", "gostaria", "saber",
}

SYSTEM_PROMPT = """Você é o Guia Tech, um assistente que orienta pessoas iniciantes a escolherem e começarem uma trilha de estudos em tecnologia.

REGRAS:
1. Responda SOMENTE com base no CONTEXTO fornecido. Não invente trilhas, cursos, links, salários ou prazos.
2. Se o contexto não tiver a informação, diga claramente: "Não tenho essa informação na minha base" e sugira o que você pode ajudar (trilhas de estudo, primeiros passos, portfólio).
3. Use português do Brasil, linguagem simples, tom acolhedor e motivador, sem jargão desnecessário.
4. Respostas curtas (até 8 linhas). Termine sugerindo UM próximo passo concreto.
5. Não prometa emprego, salário ou resultados garantidos.
6. Não responda sobre assuntos fora de estudos e carreira iniciante em tecnologia."""

MSG_SEM_INFO = (
    "Não tenho essa informação na minha base. 😕\n\n"
    "Posso ajudar com: escolher uma trilha (Front-end, Back-end com Python, Análise de Dados, QA), "
    "primeiros passos, Git/GitHub e como montar um portfólio. Quer começar por alguma dessas?"
)

SAUDACOES = {"oi", "ola", "bom dia", "boa tarde", "boa noite", "e ai", "eai", "opa", "hello", "hi"}

MSG_SAUDACAO = (
    "Olá! 👋 Eu sou o Guia Tech e ajudo quem está começando em tecnologia.\n\n"
    "Me conta: o que você gosta de fazer? Ver resultado visual (Front-end), "
    "resolver problemas de lógica (Back-end), trabalhar com números (Dados) "
    "ou encontrar falhas (QA)? Também posso explicar por onde começar."
)

def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in texto if not unicodedata.combining(c))


def tokenizar(texto: str) -> set[str]:
    palavras = re.findall(r"[a-z0-9+#]+", normalizar(texto))
    return {p.rstrip("s") if len(p) > 3 else p for p in palavras if p not in STOPWORDS and len(p) > 1}


def carregar_base() -> list[dict]:
    """Transforma trilhas.json e faq.json em 'chunks' de texto pesquisáveis."""
    chunks = []
    for t in json.loads((DATA_DIR / "trilhas.json").read_text(encoding="utf-8")):
        texto = (
            f"Trilha: {t['nome']}. {t['descricao']} Indicada para: {t['para_quem']} "
            f"Habilidades: {', '.join(t['habilidades'])}. "
            f"Tempo estimado: {t['tempo_estimado_meses']} meses (varia conforme sua dedicação). "
            f"Primeiros passos: " + "; ".join(t["primeiros_passos"]) + ". "
            "Recursos gratuitos: " + "; ".join(f"{r['nome']} ({r['url']})" for r in t["recursos_gratuitos"]) + "."
        )
        chunks.append({"id": t["id"], "titulo": t["nome"], "texto": texto,
                       "keywords": tokenizar(" ".join(t["keywords"])), "corpo": tokenizar(texto)})
    for f in json.loads((DATA_DIR / "faq.json").read_text(encoding="utf-8")):
        texto = f"{f['pergunta']} {f['resposta']}"
        chunks.append({"id": f["id"], "titulo": f["pergunta"], "texto": f["resposta"],
                       "keywords": tokenizar(" ".join(f["keywords"])), "corpo": tokenizar(texto)})
    return chunks


def buscar(pergunta: str, base: list[dict], k: int = 2) -> list[tuple[int, dict]]:
    """Pontua cada chunk: 3 pontos por palavra-chave, 1 ponto por palavra no texto."""
    q = tokenizar(pergunta)
    resultados = []
    for c in base:
        pontos = sum(3 for w in q if w in c["keywords"]) + sum(1 for w in q if w in c["corpo"] and w not in c["keywords"])
        if pontos >= LIMIAR_MINIMO:
            resultados.append((pontos, c))
    return sorted(resultados, key=lambda x: -x[0])[:k]


def resposta_offline(encontrados: list[tuple[int, dict]]) -> str:
    if not encontrados:
        return MSG_SEM_INFO
    melhor = encontrados[0][1]
    return f"**{melhor['titulo']}**\n\n{melhor['texto']}\n\n👉 Próximo passo: escolha UM item da lista acima e dedique 1 hora hoje a ele."


def resposta_llm(pergunta: str, encontrados, modelo: str, url: str, historico=None) -> str:
    contexto = "\n\n".join(f"[{c['titulo']}]\n{c['texto']}" for _, c in encontrados)
    mensagens = [{"role": "system", "content": SYSTEM_PROMPT}]
    mensagens += (historico or [])[-6:]
    mensagens.append({"role": "user", "content": f"CONTEXTO:\n{contexto}\n\nPERGUNTA: {pergunta}"})
    r = requests.post(f"{url}/api/chat", json={"model": modelo, "messages": mensagens, "stream": False,
                                                 "options": {"temperature": 0.2}}, timeout=120)
    r.raise_for_status()
    return r.json()["message"]["content"]


def responder(pergunta: str, base: list[dict], usar_llm=False, modelo="llama3.2",
              url="http://localhost:11434", historico=None) -> dict:
    if normalizar(pergunta).strip(" !?.,") in SAUDACOES:
        return {"texto": MSG_SAUDACAO, "fontes": [], "modo": "saudacao"}
    encontrados = buscar(pergunta, base)
    if not encontrados:  # anti-alucinação: sem contexto, o LLM nem é chamado
        return {"texto": MSG_SEM_INFO, "fontes": [], "modo": "sem_info"}
    fontes = [c["titulo"] for _, c in encontrados]
    if usar_llm:
        try:
            return {"texto": resposta_llm(pergunta, encontrados, modelo, url, historico), "fontes": fontes, "modo": "llm"}
        except requests.RequestException:
            pass  # cai para o modo offline
    return {"texto": resposta_offline(encontrados), "fontes": fontes, "modo": "offline"}
