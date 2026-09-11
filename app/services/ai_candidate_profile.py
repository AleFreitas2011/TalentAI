import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def gerar_perfil_profissional(texto_cv):

    if not texto_cv:
        return {}

    prompt = f"""
Você é um Head Recruiter internacional especialista em Tecnologia.

Sua missão é analisar EXCLUSIVAMENTE as informações presentes no currículo.

NUNCA invente informações.

Caso alguma informação não exista no currículo, retorne uma string vazia "".

Retorne APENAS um JSON válido.

Estrutura:

{{
"nome":"",
"titulo_profissional":"",
"anos_experiencia":"",
"localizacao":"",
"idiomas":"",
"setores":"",
"resumo":""
}}

Regras:

- titulo_profissional deve ser curto.

Exemplo:

Senior SAP MM Consultant

Oracle Cloud Financial Consultant

Microsoft 365 Engineer

Salesforce Developer

SAP SD Lead

- resumo deve possuir no máximo 5 linhas.

- idiomas deve conter somente idiomas encontrados.

- setores deve listar segmentos de atuação.

Currículo:

{texto_cv[:6000]}
"""

    try:

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            response_format={"type": "json_object"},

            temperature=0.2,

            messages=[

                {
                    "role": "system",
                    "content": "Você é um especialista em recrutamento."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ]

        )

        resposta = response.choices[0].message.content

        return json.loads(resposta)

    except Exception as erro:

        print("ERRO AI PROFILE")

        print(erro)

        return {}