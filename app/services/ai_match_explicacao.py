from app.ai.client import client

def gerar_match_explicacao(resumo, descricao_vaga):

    prompt = f"""
Você é uma recrutadora sênior especialista em tecnologia.

Analise o FIT entre um candidato e uma vaga.

Candidato:
{resumo}

Vaga:
{descricao_vaga}

Regras:

- Resposta em português
- Máximo 3 linhas
- Linguagem profissional e consultiva
- Seja objetiva
- Estrutura:
  - pontos fortes
  - aderência à vaga
  - possível gap (se houver)

Não invente informações.
"""

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return resposta.choices[0].message.content.strip()