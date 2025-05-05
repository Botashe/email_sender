# 📧 Aplicación de Escritorio para Envío de Correos Personalizados

## 🧩 Propósito

Aplicación de escritorio en Python para enviar correos electrónicos personalizados a contactos usando plantillas. Incluye gestión de usuarios, contactos, plantillas y registro de correos enviados.

---

## ⚙️ Tecnologías Utilizadas

- **Python** con **Tkinter** para la interfaz gráfica.
- **MySQL** para la base de datos.
- **PyMySQL** para la conexión a MySQL.
- **bcrypt** para hashing seguro de contraseñas.
- **smtplib** para el envío de correos vía SMTP (Gmail).

---

## 🗃️ Estructura de la Base de Datos (`database_setup.sql`)

- `users`: usuarios con credenciales y datos personales.
- `contacts`: contactos asociados a cada usuario.
- `templates`: plantillas de correo personalizables.
- `sent_emails`: historial de correos enviados con detalles.

---

## ✨ Funcionalidades Principales

- Registro e inicio de sesión con seguridad (hashing de contraseñas).
- Gestión de contactos: agregar, editar, eliminar, buscar y ordenar.
- Gestión de plantillas:
  - Crear, editar, borrar.
  - Autocompletado de variables dinámicas.
  - Previsualización del contenido.
- Envío de correos con:
  - Selección de contacto(s).
  - Plantillas personalizadas.
  - Archivos adjuntos múltiples.
- Registro automático de correos enviados en la base de datos.
- Configuración de cuenta:
  - Cambiar datos personales.
  - Actualizar contraseña.
- Interfaz gráfica clara con navegación intuitiva.

---

## 🛠️ Preparación del Ambiente de Trabajo

1. Instalar **MySQL** y crear la base de datos ejecutando:
   ```
   mysql -u root -p < database_setup.sql
   ```

2. Crear un entorno virtual de Python:
   ```
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno para el correo remitente:
   - `EMAIL_USER`
   - `EMAIL_PASS`

5. Ejecutar la aplicación:
   ```
   python email_sender_app/app.py
   ```

---

## 📁 Archivos Clave

| Archivo                         | Descripción                                        |
|--------------------------------|----------------------------------------------------|
| `app.py`                       | Punto de entrada y lógica de autenticación         |
| `main_interface.py`            | Interfaz principal de la aplicación                |
| `contact_manager.py`           | Lógica de gestión de contactos                     |
| `contact_manager_ui.py`        | Interfaz de gestión de contactos                   |
| `template_manager_ui.py`       | Interfaz para plantillas de correo                 |
| `send_email.py`                | Lógica para enviar correos y registrar historial   |
| `configuration.py`             | Configuración del usuario                          |
| `configuration_ui.py`          | Interfaz para cambiar datos y contraseña           |
| `database_setup.sql`           | Script de creación de la base de datos             |

---

## 🧩 Características Clave

- Diseño modular y escalable.
- Enfoque en seguridad y facilidad de uso.
- Flujo intuitivo para gestión y envío de correos personalizados.

---

Este proyecto está diseñado para facilitar el envío profesional de correos electrónicos a través de una experiencia gráfica accesible, segura y completa.

---

¡Gracias por usar esta aplicación! Para contribuciones o mejoras, no dudes en crear un issue o pull request.
