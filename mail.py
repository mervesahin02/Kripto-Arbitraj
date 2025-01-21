import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    """Kayıt işlemi sonrası şifreyi e-posta ile gönderir."""
    sender_email = "acysystems@gmail.com"  # Gönderici e-posta adresi
    sender_password = "afgjwtwjlihoupsk"  # Gönderici e-posta şifresi (Uygulama şifresi)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
        print(f"E-posta başarıyla gönderildi: {to_email}")
    except Exception as e:
        print(f"E-posta gönderim hatası: {e}")