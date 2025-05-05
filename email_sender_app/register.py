import tkinter as tk
from tkinter import messagebox
import pymysql
from pymysql import err as pymysql_err
import re  # Para validación de email
import bcrypt  # Para hashing de contraseñas
import time  # Para generación de salt único

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
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def register_user(username, email, password, confirm_password, register_window):
    if not username or not email or not password or not confirm_password:
        messagebox.showwarning("Advertencia", "Por favor complete todos los campos")
        return
        
    if not validate_email(email):
        messagebox.showwarning("Error", "Por favor ingrese un email válido")
        return
        
    if not validate_password(password, confirm_password):
        return
        
    db = connect_db()
    if db is None:
        return

    cursor = db.cursor()
    try:
        # Hash de la contraseña usando bcrypt (bcrypt maneja el salt internamente)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                      (username, email, hashed_password))
        db.commit()
        messagebox.showinfo("Éxito", "¡Registro exitoso!\nAhora puedes iniciar sesión con tus credenciales")
        register_window.destroy()
    except pymysql_err.MySQLError as e:
        if "Duplicate entry" in str(e):
            if "'username'" in str(e):
                messagebox.showerror("Error", f"El nombre de usuario '{username}' ya está en uso")
            else:
                messagebox.showerror("Error", f"El email '{email}' ya está registrado")
        else:
            messagebox.showerror("Error", f"Error al registrar usuario: {e}")
        return
    finally:
        cursor.close()
        db.close()

def validate_password(password, confirm_password):
    if password != confirm_password:
        messagebox.showwarning("Error", "Las contraseñas no coinciden")
        return False
    
    if len(password) < 8:
        messagebox.showwarning("Error", "La contraseña debe tener al menos 8 caracteres")
        return False
    
    if not any(char.isdigit() for char in password):
        messagebox.showwarning("Error", "La contraseña debe contener al menos un número")
        return False
        
    if not any(char.isupper() for char in password):
        messagebox.showwarning("Error", "La contraseña debe contener al menos una mayúscula")
        return False
        
    return True

from assets.register_ui import show_register_window as show_register_window_ui

def show_register_window():
    show_register_window_ui(register_user)
