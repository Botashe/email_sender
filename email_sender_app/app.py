from flask import Flask
import tkinter as tk
from tkinter import messagebox
import pymysql
from pymysql import err as pymysql_err
import bcrypt
from register import show_register_window
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.header import Header

app = Flask(__name__)

def connect_db():
    try:
        print("Intentando conectar a la base de datos...")
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="email_sender",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Conexión a la base de datos exitosa.")
        return conn
    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print(f"Error en conexión a base de datos:\n{error_message}")  # Log en consola
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{error_message}")
        print("Presiona Enter para cerrar...")
        try:
            input()
        except EOFError:
            pass
        import time
        time.sleep(10)  # Mantener la consola abierta 10 segundos antes de cerrar

def login_user(username, password, root):
    if not username or not password:
        messagebox.showwarning("Advertencia", "Por favor ingrese usuario y contraseña")
        return False

    db = connect_db()
    if db is None:
        return False

    cursor = db.cursor()
    try:
        cursor.execute("SELECT id, email, password FROM users WHERE username = %s OR email = %s", (username, username))
        user = cursor.fetchone()
        
        if user:
            user_id = user['id']
            user_email = user['email']
            db_password = user['password']
            # Convertir a bytes si es string
            if isinstance(db_password, str):
                db_password = db_password.encode('utf-8')

            # Verificar la contraseña usando bcrypt (sin salt personalizado)
            if bcrypt.checkpw(password.encode('utf-8'), db_password):
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
                root.destroy()  # Cerrar ventana de login
                from main_interface import show_main_interface
                show_main_interface(user_id, user_email, login_user)  # Pasar ID de usuario, correo y callback login_user
                return True
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
                return False
        else:
            messagebox.showerror("Error", "Usuario no encontrado")
            return False
            
    except pymysql_err.MySQLError as e:
        messagebox.showerror("Error", f"Error al iniciar sesión: {e}")
        return False
    finally:
        cursor.close()
        db.close()

from assets.login_ui import show_login_window

def main():
    show_login_window(login_user)

if __name__ == "__main__":
    main()
