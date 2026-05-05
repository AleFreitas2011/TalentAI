import os
from openai import OpenAI
from dotenv import load_dotenv

# 🔥 CARREGA .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def gerar_email_com_ia(nome_cliente, nome_vaga, candidatos):

    try:
        lista = ""

        for c in candidatos:

            # 🔥 SUPORTE PARA dict OU objeto
            nome = getattr(c, "nome_arquivo", None) or c.get("nome", "Sem nome")
            score = getattr(c, "score", None) if hasattr(c, "score") else c.get("score", 0)
            resumo = getattr(c, "resumo", None) or c.get("resumo", "Não informado")
            email = getattr(c, "email", None) or c.get("email", "")
            telefone = getattr(c, "telefone", None) or c.get("telefone", "")

            lista += f"""
- {nome} ({round(score or 0, 2)}%)
Resumo: {resumo}
Email: {email}
Telefone: {telefone}
"""

        # 💎 PROMPT ESTRATÉGICO (SEM GAPS)
        prompt = f"""
Você é uma headhunter sênior especialista em recrutamento consultivo.

Seu objetivo é apresentar candidatos ao cliente de forma estratégica, clara e segura, como uma consultora experiente.

CONTEXTO:
Cliente: {nome_cliente}
Vaga: {nome_vaga}

Candidatos:
{lista}

INSTRUÇÕES:

- Comece com uma introdução contextualizada sobre a vaga
- Demonstre entendimento do perfil buscado
- Apresente os candidatos como aderentes ao contexto da posição
- Destaque os principais pontos fortes de cada perfil
- Utilize linguagem consultiva e profissional (nível consultoria: Accenture, Deloitte)
- Transmita segurança e curadoria (evite parecer apenas envio de CV)
- Seja objetiva, clara e fluida
- NÃO mencione pontos negativos, gaps ou ausência de experiência
- Caso exista alguma limitação, reformule de forma positiva e estratégica
- Evite qualquer termo que gere dúvida ou insegurança
- Valorize o candidato e reforce aderência ao contexto da vaga
- Finalize incentivando retorno ou próximos passos

FORMATO:

Email profissional, pronto para envio ao cliente.
"""

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            timeout=20
        )

        return resposta.choices[0].message.content

    except Exception as e:
        import traceback
        traceback.print_exc()
        return None
    