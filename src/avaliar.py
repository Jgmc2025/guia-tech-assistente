"""Avaliação automática da recuperação (funciona offline). Rodar: python src/avaliar.py"""
from assistente import buscar, carregar_base, responder, MSG_SEM_INFO

# (pergunta, id esperado entre os 2 primeiros resultados ou None se deve recusar)
CASOS = [
    ("Quero começar em tecnologia mas não sei por onde", "por_onde_comecar"),
    ("Gosto de deixar site bonito, qual trilha combina?", "frontend"),
    ("O que preciso estudar para ser dev back-end com Python?", "backend_python"),
    ("Gosto de números e planilhas, existe carreira pra mim?", "dados"),
    ("Como funciona a área de QA e testes?", "qa"),
    ("Como criar um repositório no GitHub?", "git_github"),
    ("Preciso ter faculdade?", "faculdade"),
    ("Tenho que saber inglês?", "ingles"),
    ("Quantas horas por dia devo estudar?", "tempo_estudo"),
    ("Como montar meu portfólio de projetos?", "portfolio"),
    ("Estou indeciso entre as trilhas, como escolher?", "escolher_trilha"),
    ("Quanto tempo leva para aprender front-end?", "frontend"),
    # fora do escopo: o assistente deve dizer que não tem informação
    ("Qual a melhor receita de bolo de cenoura?", None),
    ("Quem ganhou a Copa do Mundo de 2014?", None),
    ("Qual o salário garantido de um dev sênior no Google?", None),
    ("Me ajuda a investir em ações?", None),
]

base = carregar_base()
acertos_in = total_in = recusas = total_out = 0
print(f"{'Resultado':<10} Pergunta")
for pergunta, esperado in CASOS:
    ids = [c["id"] for _, c in buscar(pergunta, base)]
    if esperado:
        total_in += 1
        ok = esperado in ids
        acertos_in += ok
    else:
        total_out += 1
        ok = responder(pergunta, base)["texto"] == MSG_SEM_INFO
        recusas += ok
    print(f"{'OK' if ok else 'FALHOU':<10} {pergunta}  -> {ids}")

print(f"\nAssertividade da recuperação (dentro do escopo): {acertos_in}/{total_in} = {acertos_in/total_in:.0%}")
print(f"Taxa de recusa segura (fora do escopo):          {recusas}/{total_out} = {recusas/total_out:.0%}")
