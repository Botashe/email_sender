# Email_Sender

Aplicación de escritorio para gestión de usuarios y envío de correos electrónicos con funcionalidades de registro, login y administración de contactos.

## Descripción

**Email Sender Application** es una aplicación de escritorio desarrollada en Python que permite gestionar usuarios y enviar correos electrónicos de manera sencilla y segura. Incluye funcionalidades de registro, inicio de sesión, administración de contactos y validaciones de seguridad.

## Características

- Registro de usuarios con validación de email y fortaleza de contraseña.
- Inicio de sesión seguro con hashing de contraseñas usando `bcrypt`.
- Gestión de contactos: agregar, editar y eliminar contactos.
- Pruebas unitarias para funciones críticas de autenticación.

## Requisitos

- Python 3.x
- MySQL Server
- Paquetes Python requeridos:
  - `mysql-connector-python`
  - `bcrypt`
  - `tkinter` (incluido en la instalación estándar de Python)

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/email_sender.git
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Configura la base de datos MySQL ejecutando el script `database_setup.sql`.

## Uso

Para ejecutar la aplicación principal:

```bash
python email_sender_app/app.py
```

## Pruebas

Para ejecutar los tests unitarios:

```bash
python -m unittest discover db_script
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para sugerir mejoras o reportar errores.

## Licencia

Este proyecto está bajo la licencia MIT.
