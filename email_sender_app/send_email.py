import smtplib
from email.message import EmailMessage
import os
import pymysql
from pymysql import err as pymysql_err

def connect_db():
    try:
        return pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="email_sender",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql_err.MySQLError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def send_email_logic(recipients, template_content, attachments, sender_email=None, sender_password=None, user_id=None, template_id=None, subject=None, body=None):
    """
    Envía un correo a los destinatarios con el contenido de la plantilla y archivos adjuntos.
    Registra el correo enviado en la base de datos.

    :param recipients: lista de correos electrónicos destinatarios
    :param template_content: contenido del correo (HTML o texto)
    :param attachments: lista de rutas de archivos a adjuntar
    :param sender_email: correo remitente
    :param sender_password: contraseña del correo remitente
    :param user_id: id del usuario que envía el correo
    :param template_id: id de la plantilla usada
    :param subject: asunto del correo
    :param body: cuerpo del correo
    :return: (success: bool, error_message: str)
    """
    try:
        if not template_id:
            print("Advertencia: template_id no proporcionado, se usará NULL en la base de datos")
        msg = EmailMessage()
        msg['Subject'] = subject if subject else 'Correo desde la aplicación'
        if sender_email is None or sender_email.strip() == '':
            sender_email = os.getenv('EMAIL_SENDER', 'tu_correo@gmail.com')  # Cambiar por variable de entorno o valor por defecto
        if sender_password is None or sender_password.strip() == '':
            sender_password = os.getenv('EMAIL_PASSWORD', 'tu_contraseña')  # Cambiar por variable de entorno o valor por defecto
        print(f"Enviando correo desde: {sender_email}")  # Log para debug
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipients)
        # Convertir saltos de línea en etiquetas <br> para HTML
        html_content = template_content.replace('\n', '<br>\n')
        msg.set_content(html_content, subtype='html')

        # Adjuntar archivos
        for filepath in attachments:
            if not os.path.isfile(filepath):
                continue
            with open(filepath, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(filepath)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # Configurar servidor SMTP de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        # Registrar en la base de datos el correo enviado
        if user_id and recipients and subject and body:
            db = connect_db()
            if db:
                try:
                    cursor = db.cursor()
                    for recipient_email in recipients:
                        cursor.execute(
                            "INSERT INTO sent_emails (user_id, template_id, recipient_email, subject, body) VALUES (%s, %s, %s, %s, %s)",
                            (user_id, template_id if template_id else None, recipient_email, subject, body)
                        )
                    db.commit()
                    cursor.close()
                except Exception as e:
                    print(f"Error al registrar correo enviado: {e}")
                finally:
                    db.close()

        return True, None
    except Exception as e:
        return False, str(e)
