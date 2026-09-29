# 2. Base de Conhecimento

## Arquivos

| Arquivo | Formato | Conteúdo | Uso no assistente |
|---|---|---|---|
| `data/trilhas.json` | JSON | 5 trilhas: descrição, para quem serve, habilidades, tempo estimado, primeiros passos, recursos gratuitos e palavras-chave | Responder "qual trilha?", "o que estudar?" e "quanto tempo?" |
| `data/faq.json` | JSON | 6 perguntas frequentes de iniciantes (por onde começar, faculdade, inglês, tempo de estudo, portfólio, como escolher) | Responder dúvidas gerais de carreira inicial |

## Estratégia de uso
1. Cada trilha e cada FAQ vira um **chunk** de texto.
2. A pergunta é normalizada (minúsculas, sem acentos, sem stopwords).
3. Pontuação: **3 pontos** por palavra-chave em comum + **1 ponto** por palavra em comum no texto.
4. Só entram como contexto os chunks com pontuação **≥ 3** (limiar mínimo), no máximo 2.
5. Sem chunk acima do limiar → o assistente diz que não tem a informação.

## Cuidados com os dados
- Os dados são **fictícios/gerais e sem informação pessoal**.
- Os links apontam apenas para documentações oficiais gratuitas.
- Não há salários nem promessas de mercado na base, de propósito, para evitar informação desatualizada.

## Como expandir
Adicionar uma nova trilha = incluir um objeto em `trilhas.json` com os mesmos campos. Não é preciso alterar o código.
