import smtplib
from email.message import EmailMessage
import os

import os

def send_email_logic(recipients, template_content, attachments, sender_email=None, sender_password=None):
    """
    Envía un correo a los destinatarios con el contenido de la plantilla y archivos adjuntos.

    :param recipients: lista de correos electrónicos destinatarios
    :param template_content: contenido del correo (HTML o texto)
    :param attachments: lista de rutas de archivos a adjuntar
    :param sender_email: correo remitente
    :param sender_password: contraseña del correo remitente
    :return: (success: bool, error_message: str)
    """
    # Eliminar el botón "Variables disponibles" no aplica aquí, ya que este archivo no contiene interfaz gráfica.
    # Si deseas eliminar alguna funcionalidad relacionada con variables disponibles en el envío de correo,
    # por favor especifica qué parte del código modificar.

    import smtplib
    from email.message import EmailMessage
    import os

    try:
        msg = EmailMessage()
        msg['Subject'] = 'Correo desde la aplicación'
        if sender_email is None:
            sender_email = os.getenv('EMAIL_SENDER', 'tu_correo@gmail.com')  # Cambiar por variable de entorno o valor por defecto
        if sender_password is None:
            sender_password = os.getenv('EMAIL_PASSWORD', 'tu_contraseña')  # Cambiar por variable de entorno o valor por defecto
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipients)
        msg.set_content(template_content, subtype='html')

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

        return True, None
    except Exception as e:
        return False, str(e)
