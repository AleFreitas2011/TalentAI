import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resumo_cv_ia(texto):

    if not texto:
        return ""

    try:
        prompt = f"""
Você é um especialista em recrutamento tech.

Analise o CV abaixo e gere um resumo profissional curto (máx 3 linhas).

Inclua:
- tecnologia principal (SAP, Oracle, etc)
- nível (consultor, senior, lead)
- tipo de atuação (implementação, suporte, projetos)

CV:
{texto[:3000]}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um recrutador experiente."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        resumo = response.choices[0].message.content.strip()

        return resumo

    except Exception as e:
        print("❌ ERRO IA:", e)
        return ""