import smtpd
import asyncore


class FakeSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(f"Reçu un e-mail de : {mailfrom}")
        print(f"Destinataires : {rcpttos}")
        print(f"Message : {data}")


if __name__ == '__main__':
    server = FakeSMTPServer(('127.0.0.1', 1025), None)
    print("Serveur SMTP factice en écoute sur le port 1025...")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        server.close()
