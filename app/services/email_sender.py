import smtplib
from email.mime.text import MIMEText

EMAIL_REMETENTE = "alefreitas2011@gmail.com"
SENHA_APP = "nrfi uhhk udrk ntif"

def enviar_email(destinatario, assunto, corpo):

    msg = MIMEText(corpo, "plain", "utf-8")
    msg["Subject"] = assunto
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_APP)

        servidor.sendmail(
            EMAIL_REMETENTE,
            destinatario,
            msg.as_string()
        )

        servidor.quit()

        print("📤 Email enviado com sucesso!")

    except Exception as e:
        print("❌ Erro ao enviar email:", e)