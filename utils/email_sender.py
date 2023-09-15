import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, content, email_addresses):
    # Configuration du serveur SMTP factice (localhost, port 1025)
    smtp_server = 'localhost'
    smtp_port = 1025

    # Boucle sur les adresses e-mail
    for email_address in email_addresses:
        try:
            # Créez une connexion SMTP
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                # Créez un objet MIMEMultipart pour l'e-mail
                message = MIMEMultipart()
                message['From'] = 'contact@toukoulpaddleclub.fr'
                message['To'] = email_address
                message['Subject'] = subject

                # Ajoutez le contenu de l'e-mail au format texte UTF-8
                message.attach(MIMEText(content, 'plain', 'utf-8'))

                # Envoyez l'e-mail
                server.sendmail('contact@toukoulpaddleclub.fr', [email_address], message.as_string())
            print(f"E-mail envoyé à : {email_address}")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'e-mail à {email_address}: {str(e)}")
