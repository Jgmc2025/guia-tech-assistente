# 🧭 Guia Tech: assistente virtual com IA para quem está começando em tecnologia

Projeto do desafio **"Construa Seu Assistente Virtual Com Inteligência Artificial"** (DIO).
Baseado no [repositório do desafio](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro).

## O problema
Quem está começando em tecnologia se perde entre muitas áreas e opiniões. O **Guia Tech** conversa com a pessoa, entende o que ela gosta de fazer e responde com trilhas de estudo, primeiros passos e recursos gratuitos, **sempre com base em uma base de conhecimento** e dizendo quando **não tem a informação** (sem inventar).

## Como o desafio foi cumprido

| # | Passo | Onde está |
|---|---|---|
| 1 | Documentação do agente | [`docs/01-documentacao-agente.md`](docs/01-documentacao-agente.md) |
| 2 | Base de conhecimento | [`data/`](data/) e [`docs/02-base-conhecimento.md`](docs/02-base-conhecimento.md) |
| 3 | Prompts | [`docs/03-prompts.md`](docs/03-prompts.md) |
| 4 | Aplicação funcional | [`src/app.py`](src/app.py) e [`src/assistente.py`](src/assistente.py) |
| 5 | Avaliação e métricas | [`docs/04-metricas.md`](docs/04-metricas.md) e [`src/avaliar.py`](src/avaliar.py) |
| 6 | Pitch | [`docs/05-pitch.md`](docs/05-pitch.md) |

## Como funciona
1. A pergunta é comparada com a base (`data/trilhas.json` e `data/faq.json`).
2. Se nada relevante for encontrado, o assistente responde que não tem a informação.
3. Se houver contexto, a resposta vem de um LLM local (Ollama) restrito a esse contexto, ou direto da base (modo offline).
4. A resposta mostra as fontes usadas.

## Como rodar

```bash
git clone https://github.com/Jgmc2025/guia-tech-assistente.git
cd guia-tech-assistente
pip install -r requirements.txt
streamlit run src/app.py
```

- **Modo offline (padrão):** funciona sem chave de API e sem internet.
- **Modo LLM (opcional):** instale o [Ollama](https://ollama.ai/), rode `ollama pull llama3.2` e ligue a opção "Usar LLM local" na barra lateral.

Para rodar a avaliação: `python src/avaliar.py`

## Exemplos de perguntas
- "Quero começar em tecnologia, por onde vou?"
- "Gosto de deixar site bonito, qual trilha combina?"
- "Preciso ter faculdade?"
- "Como monto um portfólio?"
- "Qual a receita de bolo?" → o assistente recusa, pois está fora da base.

## Resultados da avaliação
Em 16 perguntas de teste: **12/12** acertos na recuperação e **4/4** recusas corretas fora do escopo. Detalhes e limitações em [`docs/04-metricas.md`](docs/04-metricas.md).

## Estrutura
```
guia-tech-assistente/
├── README.md
├── requirements.txt
├── data/      # trilhas.json, faq.json
├── docs/      # os 5 documentos do desafio
└── src/       # app.py, assistente.py, avaliar.py
```

## Próximos passos
Ampliar a base, usar embeddings na busca, registrar feedback das pessoas usuárias e gravar o pitch.

## Tecnologias
Python · Streamlit · Ollama (opcional) · JSON · Mermaid
