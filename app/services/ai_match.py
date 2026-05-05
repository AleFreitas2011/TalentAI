import os
import json
import re
from openai import OpenAI

# 🔑 usa a chave do .env
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def analisar_cv_com_ia(texto_cv, descricao_vaga):
    try:
        # 🔥 segurança: evita texto gigante quebrar IA
        texto_cv = (texto_cv or "")[:1500]
        descricao_vaga = (descricao_vaga or "")[:1000]

        prompt = f"""
Você é um recrutador especialista.

Analise o CV com base na vaga e retorne:- Score de 0 a 100
- Resumo profissional curto

IMPORTANTE:
- Responda APENAS em JSON válido
- NÃO escreva nada antes ou depois

Formato obrigatório:
{{
    "score": 85,
    "resumo": "Profissional com forte experiência..."
}}

VAGA:
{descricao_vaga}

CV:
{texto_cv}
"""

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em recrutamento."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        conteudo = resposta.choices[0].message.content.strip()

        # 🔥 limpa qualquer texto extra da IA
        match = re.search(r"\{.*\}", conteudo, re.DOTALL)

        if match:
            json_str = match.group()
            resultado = json.loads(json_str)
        else:
            raise ValueError("Resposta da IA não contém JSON válido")

        return resultado

    except Exception as e:
        print("🔥 ERRO IA:", e)

        # 💎 fallback seguro (nunca quebra o sistema)
        return {
            "score": 0,
            "resumo": "Erro na análise com IA"
        }