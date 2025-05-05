import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'email_sender_app')))

from email_templates import connect_db
from tkinter import messagebox

def check_templates_for_user(user_id):
    db = connect_db()
    if db is None:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos para verificar plantillas.")
        return []
    try:
        cursor = db.cursor()
        cursor.execute("SELECT id, name, subject, created_at FROM templates WHERE user_id = %s", (user_id,))
        templates = cursor.fetchall()
        cursor.close()
        return templates
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener plantillas para el usuario: {e}")
        return []
    finally:
        db.close()

if __name__ == "__main__":
    user_id = 2
    templates = check_templates_for_user(user_id)
    print(f"Templates for user {user_id}: {templates}")
