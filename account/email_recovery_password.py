import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .templates.account import recuperation


def email_sender(sender: str, receiver: str, objet: str, url: dict):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = objet
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Récupération de mot de passe</title>
    </head>
    <body>
    <h2>Récupération de mot de passe</h2>
    <p>Bonjour,</p>
    <p>
        Vous avez demandé une récupération de mot de passe pour votre compte.<br>
        Cliquez sur le bouton ci-dessous pour réinitialiser votre mot de passe :
    </p>
    <a href="http://{list(url.values())[0]}/update_password/{list(url.values())[1]}/{list(url.values())[2]}">
        <button style="background-color: #0b2fe0;
      border-radius: 10px;
      color: white;
      padding: 8px 8px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      margin: 4px 2px;
      cursor: pointer;">Réinitialiser mon mot de passe
        </button>
    </a>
    <p>Si vous n'avez pas demandé de récupération de mot de passe, veuillez ignorer cet email.</p>
    <p>Cordialement,</p>
    <p>L'équipe de support</p>
    </body>
    </html>
    """
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login('elkanan10@gmail.com', recuperation.recup)
    smtp_server.send_message(message)
    smtp_server.quit()