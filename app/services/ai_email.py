from openai import OpenAI
import os

# usa variável de ambiente (mais seguro)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_email_com_ia(vaga, candidatos, nome_cliente):

    try:
        lista_candidatos = ""

        for c in candidatos:
            nome = getattr(c, "nome_arquivo", "não informado")
            score = getattr(c, "score", 0)
            resumo = getattr(c, "resumo", "") or getattr(c, "skills_extraidas", "")
            email = getattr(c, "email", "não informado")
            telefone = getattr(c, "telefone", "não informado")

            lista_candidatos += f"""
- {nome} ({round(score, 2)}%)
Experiência: {resumo}
Email: {email}
Telefone: {telefone}
"""

        prompt = f"""
Você é uma recrutadora sênior.

Crie um email profissional, direto e persuasivo para um cliente.

Cliente: {nome_cliente}
Vaga: {vaga.titulo if vaga else "não informada"}

Candidatos:
{lista_candidatos}

Regras:
- Linguagem profissional
- Destaque pontos fortes
- Seja objetivo
- Finalize pedindo aprovação
"""

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você escreve emails profissionais de recrutamento."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return resposta.choices[0].message.content.strip()

    except Exception as e:
        print("❌ ERRO IA EMAIL:", e)
        return ""