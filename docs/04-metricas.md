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

## Leitura crítica dos resultados
- O conjunto de teste foi escrito por mim, junto com a base, então **100% não significa que o assistente é perfeito**: ele mostra que o fluxo básico funciona.
- A busca é lexical: sinônimos e erros de digitação podem derrubar a recuperação.
- Alguns resultados trazem um segundo trecho pouco relacionado (ex.: FAQ "ingles" junto de "por onde começar"). Não prejudica a resposta principal, mas indica onde ajustar pesos.
- As checagens de alucinação e de tom com o LLM ligado são **manuais** e precisam ser registradas por quem rodar.

## Próximos passos
- Criar perguntas mais difíceis (com sinônimos e erros de digitação).
- Testar com pessoas reais e coletar feedback ("a resposta ajudou?").
- Trocar a busca por embeddings.
