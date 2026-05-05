import smtplib
from email.message import EmailMessage

EMAIL_REMETENTE = "seuemail@gmail.com"
SENHA_APP = "SENHA_DO_APP_GMAIL"

def enviar_email(destinatario, nome, vaga):

    msg = EmailMessage()
    msg["Subject"] = f"Oportunidade: {vaga}"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario

    msg.set_content(f"""
Olá {nome},

Seu perfil apresentou boa aderência à vaga "{vaga}".

Gostaria de conversar com você sobre a oportunidade.

Abraços,
Alessandra
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_REMETENTE, SENHA_APP)
        smtp.send_message(msg)