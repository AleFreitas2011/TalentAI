from app.ai.client import client
import json


def analisar_cv_com_ia(texto_cv, descricao_vaga):

    prompt = f"""
Você é uma recrutadora sênior especialista em tecnologia.

Analise o CV e a vaga abaixo.

CV:
{texto_cv}

VAGA:
{descricao_vaga}

Responda APENAS em JSON válido com:

{{
  "score": número de 0 a 100,
  "resumo": "resumo profissional em até 4 linhas",
  "pontos_fortes": ["item1", "item2"],
  "pontos_atencao": ["item1", "item2"],
  "nivel": "Junior, Pleno ou Senior"
}}

REGRAS:
- Seja criteriosa
- Avalie experiência real (não só palavras-chave)
- Não invente informações
"""

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é uma recrutadora técnica experiente."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        conteudo = resposta.choices[0].message.content

        return json.loads(conteudo)

    except Exception as e:
        print("❌ Erro IA:", e)
        return None