# 4. Avaliação e Métricas

## Metodologia
Script `src/avaliar.py` com **16 perguntas** (12 dentro do escopo, 4 fora do escopo). Roda offline e mede a etapa de recuperação, que é a que decide se o assistente tem base para responder.

| Métrica | Como é medida |
|---|---|
| **Assertividade da recuperação** | O trecho correto está entre os 2 primeiros resultados |
| **Taxa de recusa segura** | Perguntas fora do escopo recebem "não tenho essa informação" (o LLM nem é chamado) |
| **Ausência de alucinação (manual)** | Com o LLM ligado, conferir se a resposta cita algo que não está no contexto |
| **Adequação de tom (manual)** | Simples, acolhedor, até 8 linhas e com um próximo passo |

## Resultado da execução (`python src/avaliar.py`)

| Métrica | Resultado |
|---|---|
| Assertividade da recuperação (dentro do escopo) | **12/12 (100%)** |
| Taxa de recusa segura (fora do escopo) | **4/4 (100%)** |

Após a redução de ruído na busca (2º trecho exige 70% da pontuação do 1º), o resultado se manteve em 12/12 e 4/4.

## Checagem manual com o LLM ligado (Ollama)
Foram feitas 12 interações (9 dentro do escopo e 3 fora). As respostas fora do escopo foram recusadas corretamente. Nas dentro do escopo, apareceram três falhas:

| Interação | Falha observada | Causa provável | Correção aplicada |
|---|---|---|---|
| 1. "Quero começar em tecnologia mas não sei por onde" | O modelo respondeu "Não tenho essa informação" mesmo com o FAQ recuperado | O prompt não deixava claro quando recusar | Regra 3: só recusar se o contexto estiver vazio ou irrelevante |
| 3. "O que preciso estudar para ser dev back-end com Python?" | Citou SQLAlchemy, Django ORM, segurança web e "regras de negócio em Python", que não estão na base | O modelo completou com conhecimento próprio | Regra 2: citar só o que está literalmente no contexto; temperatura 0 |
| 7. "Preciso ter faculdade?" | Afirmou "não é necessário", contradizendo o FAQ ("depende da vaga e da empresa") | O modelo simplificou o contexto | Regra 4: não contradizer o contexto nem transformar "depende" em sim/não |

Problemas menores: o modelo escreveu a linha "Fontes:" por conta própria (duplicando a do sistema) e passou de 8 linhas em várias respostas. Corrigido com a regra 7 e o limite explícito na regra 6. Trechos pouco relacionados nas fontes (ex.: Front-end junto de Back-end) foram reduzidos com o limite relativo de pontuação.

**Status:** as correções foram aplicadas, mas a nova checagem manual com o LLM ainda precisa ser refeita e registrada aqui por quem rodar o Ollama.

## Leitura crítica dos resultados
- O conjunto de teste foi escrito por mim, junto com a base, então **100% não significa que o assistente é perfeito**: ele mostra que o fluxo básico funciona.
- A busca é lexical: sinônimos e erros de digitação podem derrubar a recuperação.
- Alguns resultados trazem um segundo trecho pouco relacionado (ex.: FAQ "ingles" junto de "por onde começar"). Não prejudica a resposta principal, mas indica onde ajustar pesos.
- As checagens de alucinação e de tom com o LLM ligado são **manuais** e precisam ser registradas por quem rodar.

## Próximos passos
- Criar perguntas mais difíceis (com sinônimos e erros de digitação).
- Testar com pessoas reais e coletar feedback ("a resposta ajudou?").
- Trocar a busca por embeddings.
